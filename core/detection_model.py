"""
detection_model.py

Trains scam detection model and saves:
- scam_model.pkl
- vectorizer.pkl

This version uses project-root based paths (portable & clean).
"""

import pandas as pd
import re
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.utils import resample

# ==========================================================
# 📁 PROJECT PATH SETUP (ROOT-BASED)
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "datasets"
MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(exist_ok=True)

SPAM_PATH = DATA_DIR / "spam.csv"
WHATSAPP_PATH = DATA_DIR / "whatsapp_scam_dataset.csv"

# ==========================================================
# 🧹 TEXT CLEANER
# ==========================================================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ==========================================================
# 📥 LOAD DATASETS
# ==========================================================

print("📥 Loading datasets...")

# --- spam.csv ---
spam_df = pd.read_csv(SPAM_PATH, encoding="latin1")

if "v1" in spam_df.columns:
    spam_df = spam_df.rename(columns={"v1": "label", "v2": "text"})

spam_df = spam_df[["text", "label"]]
spam_df["label"] = spam_df["label"].map({"ham": 0, "spam": 1})
spam_df.dropna(subset=["text"], inplace=True)
spam_df["text"] = spam_df["text"].apply(clean_text)

print(f"✅ Loaded spam.csv → {spam_df.shape}")

# --- WhatsApp dataset ---
wa_df = pd.read_csv(WHATSAPP_PATH)

if "message" not in wa_df.columns:
    raise ValueError("❌ whatsapp_scam_dataset.csv must contain 'message' column.")

wa_df = wa_df[["message"]].rename(columns={"message": "text"})
wa_df["label"] = 1  # all are scams
wa_df["text"] = wa_df["text"].apply(clean_text)

print(f"✅ Loaded whatsapp_scam_dataset.csv → {wa_df.shape}")

# ==========================================================
# 🧩 MERGE & BALANCE DATA
# ==========================================================

combined_df = pd.concat([spam_df, wa_df], ignore_index=True)
combined_df.dropna(subset=["text"], inplace=True)

print(f"🧩 Combined dataset size: {combined_df.shape}")

scam_df = combined_df[combined_df["label"] == 1]
legit_df = combined_df[combined_df["label"] == 0]

min_samples = min(len(scam_df), len(legit_df))

scam_df = resample(scam_df, replace=False, n_samples=min_samples, random_state=42)
legit_df = resample(legit_df, replace=False, n_samples=min_samples, random_state=42)

balanced_df = pd.concat([scam_df, legit_df])
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"⚖️ Balanced dataset size: {balanced_df.shape}")

# ==========================================================
# ✂ TRAIN-TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    balanced_df["text"],
    balanced_df["label"],
    test_size=0.2,
    stratify=balanced_df["label"],
    random_state=42
)

# ==========================================================
# 🔎 TF-IDF VECTORIZATION
# ==========================================================

vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 3),
    sublinear_tf=True,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# ==========================================================
# 🤖 MODEL TRAINING
# ==========================================================

print("🤖 Training Logistic Regression...")

base_model = LogisticRegression(
    max_iter=3000,
    C=2.0,
    class_weight="balanced",
    solver="lbfgs"
)

base_model.fit(X_train_tfidf, y_train)

# Calibrate probabilities
model = CalibratedClassifierCV(base_model, cv="prefit", method="sigmoid")
model.fit(X_train_tfidf, y_train)

# ==========================================================
# 📊 EVALUATION
# ==========================================================

y_pred = model.predict(X_test_tfidf)
y_prob = model.predict_proba(X_test_tfidf)[:, 1]

print("\n✅ Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n📄 Classification Report:\n", classification_report(y_test, y_pred))

# ==========================================================
# 💾 SAVE MODEL
# ==========================================================

joblib.dump(model, MODELS_DIR / "scam_model.pkl")
joblib.dump(vectorizer, MODELS_DIR / "vectorizer.pkl")

print("\n✅ Model and vectorizer saved in root 'models/' folder!")

# ==========================================================
# 🔎 HELPER FUNCTION (OPTIONAL)
# ==========================================================

def predict_scam(text):
    text_clean = clean_text(text)
    X = vectorizer.transform([text_clean])
    prob = model.predict_proba(X)[0][1] * 100
    pred = "Scam" if prob >= 50 else "Legit"
    return pred, round(prob, 2)
