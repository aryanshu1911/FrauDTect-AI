🛡️ FrauDTect AI
Hybrid AI-Powered Real-Time Scam Detection System

FrauDTect AI is a real-time scam detection platform that analyzes suspicious text, URLs, and screenshots using a hybrid approach combining:

Rule-based keyword risk scoring

Supervised Machine Learning (TF-IDF + Logistic Regression)

AI-powered explainability engine

OSINT integrations (WHOIS, VirusTotal, URLScan)

Designed for cybersecurity research, fraud detection, and intelligent scam analysis.

🚀 Features
📝 Text & Screenshot Analysis

Weighted scam keyword detection

TF-IDF + Logistic Regression classifier

Hybrid risk scoring engine

Confidence score calculation

Scam category detection (crypto, bank fraud, urgency, phishing, etc.)

Structured AI-generated explanation of verdict

🌐 URL Analysis

Domain normalization

DNS resolution validation

Suspicious TLD detection

Domain age via WHOIS lookup

Optional deep OSINT scan:

VirusTotal API

URLScan API

Risk scoring with explanation

📊 Explainability Engine

Extracts top influential features from ML model

Generates human-readable reasoning summary

Combines ML probability + keyword signals

🧠 Architecture Overview

Hybrid Decision Model:

Final Risk Score =
0.6 × ML Probability + 0.4 × Keyword Weighted Score

This ensures:

Statistical robustness (ML)

Deterministic red-flag detection (rules)

Reduced false positives

🏗️ Project Structure
FrauDTect-AI/
│
├── core/
│   ├── scam_detection.py
│   ├── detection_model.py
│   ├── explainability.py
│   ├── keywords.py
│   ├── url_analysis.py
│   ├── ocr_engine.py
│   └── logger.py
│
├── models/
│   ├── scam_model.pkl
│   └── vectorizer.pkl
│
├── app.py
├── requirements.txt
└── .gitignore

🛠️ Technologies Used

Python

Streamlit

Scikit-learn

TF-IDF Vectorization

Logistic Regression (Calibrated)

OCR (Pillow / Tesseract compatible)

WHOIS Lookup

VirusTotal API

URLScan API

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/aryanshu1911/FrauDTect-AI.git
cd FrauDTect-AI

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Application
streamlit run app.py

🔐 Environment Variables

Create a .env file in root directory:

VT_API_Key=your_virustotal_api_key
URLSCAN_API_Key=your_urlscan_api_key

📦 Training the Model (Optional)

Datasets are excluded from the repository.

To retrain:

Place datasets inside data/datasets/

Run:

python core/detection_model.py


This will regenerate:

scam_model.pkl

vectorizer.pkl

📈 Current Model Performance

Accuracy: ~99%
Balanced Dataset
Calibrated Logistic Regression

(Performance depends on training data distribution.)

🎯 Use Cases

Scam message detection

Crypto fraud detection

Phishing identification

Suspicious domain evaluation

Cybersecurity demo projects

Educational AI explainability demo

⚠️ Disclaimer

This tool is built for educational and research purposes.
It does not guarantee 100% fraud detection accuracy.
