import streamlit as st
import json
import os
from PIL import Image

from core.scam_detection import analyze_text
from core.url_analysis import analyze_url
from core.ocr_engine import extract_text_from_image
from core.logger import log_analysis

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="FrauDTect",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================================
# SIDEBAR STYLING
# ==========================================================

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #1b1f2a !important;
}

div[data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stButton"] > button {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;

    width: 100% !important;
    height: 42px !important;
    padding: 0 14px !important;

    background-color: transparent !important;
    border: none !important;
    border-left: 4px solid transparent !important;
    box-sizing: border-box !important;

    text-align: left !important;
    font-size: 15px !important;
    color: #e0e6ed !important;

    border-radius: 8px !important;
    transition: background-color 0.15s ease !important;
}

div[data-testid="stButton"] > button:hover {
    background-color: #252a38 !important;
    color: white !important;
}

div[data-testid="stButton"] > button:focus {
    background-color: #21263a !important;
    border-left: 4px solid #4dabf7 !important;
    font-weight: 600 !important;
}

button:focus {
    outline: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

st.sidebar.title("🛡️ FrauDTect")

if "menu" not in st.session_state:
    st.session_state.menu = "new_scan"

def nav_button(label, key, icon):
    if st.sidebar.button(f"{icon} {label}", key=key):
        st.session_state.menu = key

nav_button("New Scan", "new_scan", "🔍")
nav_button("Scan History", "history", "📜")
nav_button("Settings", "settings", "⚙️")

menu = st.session_state.menu

# ==========================================================
# NEW SCAN
# ==========================================================

if menu == "new_scan":

    st.title("🛡️ FrauDTect AI Dashboard")

    tab1, tab2, tab3 = st.tabs([
        "📝 Text Analysis",
        "🌐 URL Analysis",
        "🖼️ Screenshot Analysis"
    ])

    # ===============================
    # TEXT ANALYSIS
    # ===============================
    with tab1:
        st.subheader("Analyze Suspicious Text")

        text_input = st.text_area(
            "Enter suspicious message",
            placeholder="Example: Urgent! Verify your bank account to avoid suspension."
        )

        if st.button("Analyze Text", type="primary"):

            if text_input.strip():

                result = analyze_text(text_input)

                # If model failed
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result.get("verdict", "Analysis Complete"))

                    st.markdown("### 📊 Analysis Details")
                    st.write(f"**Risk Score:** {result.get('risk_score', 0)}%")
                    st.write(
                        f"**ML Prediction:** {result.get('ml_prediction', 'N/A')} "
                        f"({result.get('ml_probability', 0)}%)"
                    )
                    st.write(
                        f"**Confidence Level:** {result.get('confidence_score', 0)}%"
                    )
                    st.write(
                        f"**Matched Keywords:** "
                        f"{', '.join(result.get('matched_keywords', [])) or 'None'}"
                    )
                    st.write(
                        f"**Scam Category:** {result.get('scam_category', 'Unknown')}"
                    )

                    st.markdown("### 🧠 AI Explanation")
                    st.markdown(result.get("ai_explanation", "Explanation unavailable."))

                    log_analysis({
                        "type": "text",
                        "input": text_input[:200],
                        "risk_score": result.get("risk_score", 0),
                        "verdict": result.get("verdict", "")
                    })

            else:
                st.warning("Please enter text")

    # ===============================
    # URL ANALYSIS
    # ===============================
    with tab2:
        st.subheader("Analyze Suspicious URL")

        url_input = st.text_input(
            "Enter URL",
            placeholder="example.com/login"
        )

        col1, col2 = st.columns(2)
        analyze_clicked = col1.button("Quick Scan", type="primary")
        osint_clicked = col2.button("Deep OSINT Scan", type="secondary")

        if analyze_clicked or osint_clicked:

            if url_input.strip():

                with st.spinner("Analyzing URL..."):
                    result = analyze_url(url_input, deep_scan=osint_clicked)

                st.success(result.get("verdict", "Analysis Complete"))

                st.markdown("### 📊 URL Analysis")
                st.write(f"**Risk Score:** {result.get('risk_score', 0)}%")
                st.write(f"**Domain:** {result.get('domain', 'Unknown')}")
                st.write(
                    f"**Domain Age:** {result.get('domain_age_days', 'Unknown')}"
                )

                st.markdown(result.get("explanation", ""))

                if osint_clicked and result.get("osint"):
                    with st.expander("OSINT Details"):
                        st.json(result["osint"])

                log_analysis({
                    "type": "url",
                    "input": url_input,
                    "risk_score": result.get("risk_score", 0),
                    "verdict": result.get("verdict", "")
                })

            else:
                st.warning("Please enter URL")

    # ===============================
    # IMAGE ANALYSIS
    # ===============================
    with tab3:
        st.subheader("Analyze Screenshot")

        uploaded_file = st.file_uploader(
            "Upload screenshot",
            type=["png", "jpg", "jpeg"]
        )

        if st.button("Analyze Image", type="primary"):

            if uploaded_file is not None:

                image = Image.open(uploaded_file).convert("RGB")
                extracted_text = extract_text_from_image(image)

                st.text_area("Extracted Text", extracted_text, height=150)

                result = analyze_text(extracted_text)

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result.get("verdict", "Analysis Complete"))

                    st.markdown("### 📊 Analysis Details")
                    st.write(f"**Risk Score:** {result.get('risk_score', 0)}%")
                    st.write(
                        f"**ML Prediction:** {result.get('ml_prediction', 'N/A')} "
                        f"({result.get('ml_probability', 0)}%)"
                    )
                    st.write(
                        f"**Confidence Level:** {result.get('confidence_score', 0)}%"
                    )
                    st.write(
                        f"**Scam Category:** {result.get('scam_category', 'Unknown')}"
                    )

                    st.markdown("### 🧠 AI Explanation")
                    st.markdown(result.get("ai_explanation", "Explanation unavailable."))

                    log_analysis({
                        "type": "image",
                        "input": "screenshot",
                        "risk_score": result.get("risk_score", 0),
                        "verdict": result.get("verdict", "")
                    })

            else:
                st.warning("Upload an image first")

# ==========================================================
# SCAN HISTORY
# ==========================================================

elif menu == "history":

    st.title("📜 Scan History")

    history_file = "logs/history.json"

    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                history = json.loads(content) if content else []
        except:
            history = []
    else:
        history = []

    if history:
        st.dataframe(history[::-1], use_container_width=True)
    else:
        st.info("No scans yet.")

# ==========================================================
# SETTINGS
# ==========================================================

elif menu == "settings":

    st.title("⚙️ Settings")
    st.info("Settings panel coming soon.")
