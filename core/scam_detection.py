import re
import joblib
from pathlib import Path
from core.keywords import keyword_weights, scam_categories
from core.explainability import ExplainabilityEngine

# ===============================
# 📦 1. Safe Model & Vectorizer Load
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "scam_model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "vectorizer.pkl"

model = None
vectorizer = None

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception as e:
    print(f"[WARNING] ML model load failed: {e}")

# Initialize Explainability Engine
explainer_engine = ExplainabilityEngine(model, vectorizer)


# ===============================
# 🔍 2. Keyword-Based Detection
# ===============================
def detect_scam_keywords(text: str):
    text_lower = text.lower()
    return [
        kw for kw in keyword_weights
        if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)
    ]


def calculate_risk_score(keywords):
    return sum(keyword_weights.get(kw, 0) for kw in keywords)


# ===============================
# 📂 Scam Category Detection
# ===============================
def detect_scam_category(matched_keywords):
    category_scores = {}

    for category, keywords in scam_categories.items():
        count = len(set(matched_keywords) & set(keywords))
        if count > 0:
            category_scores[category] = count

    if category_scores:
        return max(category_scores, key=category_scores.get)

    return "Uncategorized"


# ===============================
# 🤖 3. ML-Based Prediction
# ===============================
def predict_scam(text: str):

    if model is None or vectorizer is None:
        return "Model Unavailable", 0

    try:
        X = vectorizer.transform([text])
        prob = model.predict_proba(X)[0][1] * 100
        pred = "Scam" if prob >= 50 else "Legit"
        return pred, round(prob, 2)

    except Exception as e:
        print(f"[ERROR] ML prediction failed: {e}")
        return "Prediction Error", 0


# ===============================
# 🧠 4. Hybrid Decision Engine
# ===============================
def generate_combined_verdict(keyword_score: int, ml_prob: float):

    final_score = (0.6 * ml_prob) + (0.4 * (keyword_score * 5))
    final_score = min(100, max(0, final_score))

    if final_score >= 65:
        return "🛑 Confirmed Scam"
    elif final_score >= 45:
        return "🚨 Likely Scam"
    elif final_score >= 20:
        return "⚠️ Suspicious"
    else:
        return "✅ Legitimate"


# ===============================
# 🚀 5. FULL TEXT ANALYSIS PIPELINE
# ===============================
def analyze_text(text: str):

    try:
        # -------- Keyword Analysis --------
        keywords = detect_scam_keywords(text)
        keyword_score = calculate_risk_score(keywords)

        # -------- ML Prediction --------
        ml_pred, ml_prob = predict_scam(text)

        # -------- Hybrid Risk Score --------
        hybrid_score = (0.6 * ml_prob) + (0.4 * (keyword_score * 5))
        hybrid_score = round(min(100, max(0, hybrid_score)), 2)

        final_verdict = generate_combined_verdict(keyword_score, ml_prob)

        # -------- Confidence Score --------
        confidence = abs(ml_prob - 50) * 2
        confidence = round(confidence, 2)

        # -------- Scam Category --------
        scam_category = detect_scam_category(keywords)

        # -------- AI Text Explanation (TEXT ONLY) --------
        ai_reasoning = explainer_engine.build_reasoning(
            keywords,
            keyword_score,
            ml_pred,
            ml_prob,
            hybrid_score,
            scam_category,
            confidence
        )

        return {
            "input_text": text[:500],
            "matched_keywords": keywords,
            "keyword_score": keyword_score,
            "ml_prediction": ml_pred,
            "ml_probability": ml_prob,
            "confidence_score": confidence,
            "scam_category": scam_category,
            "risk_score": hybrid_score,
            "verdict": final_verdict,
            "ai_explanation": ai_reasoning
        }

    except Exception as e:
        return {
            "error": str(e),
            "risk_score": 0,
            "verdict": "Error during analysis"
        }
