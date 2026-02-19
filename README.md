# 🛡️ FrauDTect AI  
### Hybrid AI-Powered Real-Time Scam Detection System

FrauDTect AI is a real-time scam detection platform that analyzes suspicious text, URLs, and screenshots using a hybrid approach combining:

- Rule-based keyword risk scoring
- Supervised Machine Learning (TF-IDF + Logistic Regression)
- AI-powered explainability engine
- OSINT integrations (WHOIS, VirusTotal, URLScan)

Designed for cybersecurity research, fraud detection, and intelligent scam analysis.

---

## 🚀 Features

### 📝 Text & Screenshot Analysis
- Weighted scam keyword detection
- TF-IDF + Logistic Regression classifier
- Hybrid risk scoring engine
- Confidence score calculation
- Scam category detection (crypto, bank fraud, urgency, phishing, etc.)
- Structured AI-generated explanation of verdict

### 🌐 URL Analysis
- Domain normalization
- DNS resolution validation
- Suspicious TLD detection
- Domain age via WHOIS lookup
- Optional deep OSINT scan:
  - VirusTotal API integration
  - URLScan API integration
- Risk scoring with explanation

### 📊 Explainability Engine
- Extracts top influential features from ML model
- Generates human-readable reasoning summary
- Combines ML probability + keyword signals

---

## 🧠 Architecture Overview

Hybrid Decision Model:

Final Risk Score =
0.6 × ML Probability + 0.4 × (Keyword Weighted Score × 5)

This ensures:
- Statistical robustness (ML)
- Deterministic red-flag detection (rules)
- Reduced false positives

---

## 🏗️ Project Structure


This ensures:
- Statistical robustness (ML)
- Deterministic red-flag detection (rules)
- Reduced false positives

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression (CalibratedClassifierCV)
- OCR (Pillow / Tesseract compatible)
- WHOIS Lookup
- VirusTotal API
- URLScan API

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/aryanshu1911/FrauDTect-AI.git
cd FrauDTect-AI

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Application
streamlit run app.py

🔐 Environment Variables

Create a .env file in the root directory:

VT_API_Key=your_virustotal_api_key
URLSCAN_API_Key=your_urlscan_api_key

📈 Current Model Performance

Accuracy: ~99%

Balanced dataset training

Calibrated Logistic Regression

TF-IDF (1–3 n-grams, max 20,000 features)

Note: Performance depends on training data distribution.

🎯 Use Cases

Scam message detection

Crypto fraud identification

Phishing detection

Suspicious domain evaluation

Cybersecurity research demos

AI explainability demonstrations

⚠️ Disclaimer

This tool is built for educational and research purposes.
It does not guarantee 100% fraud detection accuracy.