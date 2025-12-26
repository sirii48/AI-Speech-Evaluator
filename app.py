import streamlit as st
from scoring import (
    calculate_simplified_final_score,
    content_and_structure_score,
    speech_rate_score,
    language_and_grammar_score,
    clarity_score,
    engagement_score
)

st.title(" Speech Evaluation Tool ")

# Add custom CSS to change text area focus border color
st.markdown("""
    <style>
        textarea:focus, textarea.form-control:focus, textarea:active {
            border-color: #1E90FF !important;
            box-shadow: 0 0 0 2px #1E90FF !important;
            outline: 0 !important;
        }
        .stTextArea > div > div > div > textarea:focus {
            border-color: #1E90FF !important;
            box-shadow: 0 0 0 2px #1E90FF !important;
            outline: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.write("Paste your speech transcript below and click **Evaluate**.")

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
        st.metric("Overall Score (out of 100)", f"{final_score:.2f}")

        st.subheader("📊 Breakdown")
        st.write(f"**Content & Structure:** {cs}/40")
        st.write(f"**Speech Rate:** {sr}/10")
        st.write(f"**Language & Grammar:** {lg}/20")
        st.write(f"**Clarity:** {cl}/15")
        st.write(f"**Engagement:** {eg}/15")

        st.success("Evaluation complete!")
