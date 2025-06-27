import streamlit as st
from langdetect import detect_langs, DetectorFactory, LangDetectException
import pandas as pd
from datetime import datetime

# Fix randomness
DetectorFactory.seed = 0

LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ru': 'Russian',
    # Add more if needed
}

def get_language_name(lang_code):
    return LANGUAGES.get(lang_code, "Unknown")

def detect_language(text, confidence_threshold=0.90):
    try:
        langs = detect_langs(text)
        top_lang = langs[0]
        lang_code = top_lang.lang
        prob = top_lang.prob

        status = "✅ High Confidence" if prob >= confidence_threshold else "⚠️ Low Confidence"

        return {
            "language_code": lang_code,
            "language_name": get_language_name(lang_code),
            "confidence": prob,
            "status": status,
            "all_langs": langs
        }
    except LangDetectException:
        return {
            "language_code": None,
            "language_name": "Detection Failed",
            "confidence": None,
            "status": "❌ Detection Failed",
            "all_langs": []
        }

# --- Streamlit UI ---
st.set_page_config(page_title="🌐 Advanced Language Detector", layout="centered")
st.title("🌐 Advanced Language Detection App")
st.write("Detect the language of any text with confidence score and probability rankings.")

# User input
user_input = st.text_area("✏️ Enter text here:", height=150, placeholder="Type or paste your text...")

# Threshold slider
confidence_threshold = st.slider("🎯 Confidence Threshold", 0.0, 1.0, 0.90, 0.01)

# Process on click
if st.button("🔍 Detect Language"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        result = detect_language(user_input, confidence_threshold)

        st.success("✅ Language detection completed.")
        st.markdown(f"**🗣️ Detected Language:** `{result['language_name']}` ({result['language_code']})")
        if result["confidence"] is not None:
            st.markdown(f"**📈 Confidence Score:** `{result['confidence']:.2f}`")
        st.markdown(f"**🔎 Detection Status:** {result['status']}")

        # Show top probable languages
        if result["all_langs"]:
            st.markdown("### 🔝 Top Probable Languages")
            langs_data = [
                {
                    "Language Code": lang.lang,
                    "Language Name": get_language_name(lang.lang),
                    "Probability": f"{lang.prob:.2f}"
                } for lang in result["all_langs"][:5]
            ]
            df = pd.DataFrame(langs_data)
            st.table(df)

            # Save results as CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Language Report (CSV)", csv, "language_report.csv", "text/csv")


