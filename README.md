# 🛡️ FrauDTect

**Hybrid AI-Powered Real-Time Scam Detection System**

---

## 📄 Abstract

FrauDTect AI is a hybrid AI-powered real-time scam detection platform that analyzes suspicious text, URLs, and screenshots to identify fraudulent content. The system combines rule-based keyword risk scoring with supervised Machine Learning (TF-IDF + Logistic Regression) and an AI-powered explainability engine to deliver accurate, interpretable verdicts. It integrates OSINT sources including WHOIS lookups, VirusTotal, and URLScan for deep domain analysis. Built with Python and Streamlit, FrauDTect AI provides a clean, interactive interface for cybersecurity research, fraud detection demonstrations, and intelligent scam analysis. It is designed as an academic mini project suitable for demonstration in 5–10 minutes.

---

## 🧩 Problem Statement

Online scams are becoming increasingly sophisticated — from phishing emails and crypto fraud to fake banking alerts. Traditional detection methods rely on either static keyword matching (prone to false positives) or pure ML models (lacking interpretability). There is a need for a **hybrid system** that combines statistical robustness with deterministic red-flag detection while providing **human-readable explanations** for its verdicts.

---

## 💡 Proposed Solution

FrauDTect AI provides a multi-layered detection approach in a single, interactive platform:

1. **Text & Screenshot Analyzer** — Hybrid ML + rule-based scam detection with confidence scoring
2. **URL Analyzer** — Domain validation, WHOIS lookup, and optional deep OSINT scanning
3. **Explainability Engine** — Human-readable reasoning combining ML features and keyword signals

All analysis is designed to be transparent, interpretable, and research-friendly.

---

## 🔍 How the Hybrid Model Works

Instead of relying on a single detection method, FrauDTect AI combines two approaches:

1. **ML Probability** — TF-IDF vectorization + Calibrated Logistic Regression produces a scam probability score
2. **Keyword Risk Score** — Weighted keyword matching across scam categories (crypto, banking, urgency, phishing)
3. **Final score is a weighted blend** of both signals

```
Final Risk Score = 0.6 × ML Probability + 0.4 × (Keyword Weighted Score × 5)
```

This ensures:
- **Statistical robustness** from the ML model
- **Deterministic red-flag detection** from keyword rules
- **Reduced false positives** through hybrid scoring

---

## 📊 How the Explainability Engine Works

### Feature Extraction
- Top influential TF-IDF features are extracted from the ML model
- Matched scam keywords are identified with their categories and weights

### Reasoning Generation
- Combines ML probability + keyword signals into a structured explanation
- Produces a human-readable summary of why content was flagged
- Displays scam category breakdown (crypto, bank fraud, urgency, phishing, etc.)

This ensures that every verdict is **transparent and auditable**.

---

## 🛡️ Security & Analysis Capabilities

| Capability | Implementation |
|-----------|---------------|
| Text Analysis | TF-IDF + Logistic Regression + keyword scoring |
| Screenshot Analysis | OCR text extraction + hybrid analysis pipeline |
| URL Validation | DNS resolution + suspicious TLD detection |
| Domain Intelligence | WHOIS lookup for domain age verification |
| Deep OSINT | VirusTotal + URLScan API integrations |
| Explainability | ML feature extraction + structured reasoning |

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.10+ |
| Frontend | Streamlit |
| ML Pipeline | Scikit-learn, TF-IDF Vectorization |
| Classifier | Logistic Regression (CalibratedClassifierCV) |
| OCR | Pillow / Tesseract compatible |
| OSINT | WHOIS, VirusTotal API, URLScan API |

---

## 🚀 Setup & Run

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/aryanshu1911/FrauDTect-AI.git
cd FrauDTect-AI

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```
VT_API_Key=your_virustotal_api_key
URLSCAN_API_Key=your_urlscan_api_key
```

> **Note:** OSINT features (VirusTotal, URLScan) are optional. The app functions without API keys but with limited URL analysis.

---

## 🧪 Testing

### Sample Test Inputs

| Input Type | Sample | Expected Result |
|-----------|--------|-----------------|
| Scam Text | "Congratulations! You've won $1000. Click here to claim" | High Risk — Urgency + Prize scam |
| Phishing | "Your bank account has been locked. Verify immediately" | High Risk — Banking fraud |
| Safe Text | "Meeting scheduled for tomorrow at 3 PM" | Low Risk — No scam indicators |
| Suspicious URL | `http://free-prizes-now.xyz` | High Risk — Suspicious TLD |
| Safe URL | `https://google.com` | Low Risk — Established domain |

### Edge Cases

- Empty input → Graceful error handling
- Non-English text → Limited detection (English-trained model)
- Shortened URLs → Domain normalization handles redirects
- Screenshot with no text → OCR returns empty, low confidence

---

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | ~99% |
| Training | Balanced dataset |
| Classifier | Calibrated Logistic Regression |
| Features | TF-IDF (1–3 n-grams, max 20,000) |

> **Note:** Performance depends on training data distribution and may vary with real-world inputs.

---

## 🎯 Use Cases

- Scam message detection
- Crypto fraud identification
- Phishing detection
- Suspicious domain evaluation
- Cybersecurity research demos
- AI explainability demonstrations

---

## ⚠️ Limitations

- English-language scam detection only
- OCR accuracy depends on image quality
- OSINT APIs require valid API keys for full functionality
- ML model accuracy depends on training data distribution
- No real-time URL crawling or sandbox analysis

---

## 🔮 Future Enhancements

- **Multi-language support** — Expand detection beyond English
- **Deep learning models** — BERT/transformer-based classification
- **Real-time URL sandboxing** — Dynamic page analysis
- **Browser extension** — Real-time scam detection while browsing
- **Automated retraining pipeline** — Continuous model improvement
- **User feedback loop** — Community-driven scam reporting

---

## 📜 License

This project is open-source under the MIT License.

---
