import streamlit as st
from scoring import (
    calculate_simplified_final_score,
    content_and_structure_score,
    speech_rate_score,
    language_and_grammar_score,
    clarity_score,
    engagement_score
)

st.set_page_config(page_title="Speech Evaluation Tool", layout="centered")

st.title("🗣️ Speech Evaluation Tool")
st.write("Paste your speech transcript below and click **Evaluate**.")

# Custom focus color
st.markdown("""
<style>
textarea:focus {
    border-color: #1E90FF !important;
    box-shadow: 0 0 0 2px #1E90FF !important;
}
</style>
""", unsafe_allow_html=True)

text = st.text_area("Enter transcript:", height=250)

if st.button("Evaluate"):
    if not text.strip():
        st.error("Please enter some text!")
    else:
        final_score = calculate_simplified_final_score(text)
        cs = content_and_structure_score(text)
        sr = speech_rate_score(text)
        lg = language_and_grammar_score(text)
        cl = clarity_score(text)
        eg = engagement_score(text)

        st.subheader("🎯 Final Score")
        st.metric("Overall Score (out of 100)", final_score)

        st.subheader("📊 Score Breakdown")
        st.write(f"**Content & Structure:** {cs} / 40")
        st.write(f"**Sentence Flow:** {sr} / 10")
        st.write(f"**Language & Grammar:** {lg} / 20")
        st.write(f"**Clarity:** {cl} / 15")
        st.write(f"**Engagement:** {eg} / 15")

        st.success("Evaluation complete!")
