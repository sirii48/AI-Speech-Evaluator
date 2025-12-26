# app.py
import streamlit as st
from scoring import calculate_improved_score

st.title("Speech Evaluation Tool")

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
        final_score, breakdown = calculate_improved_score(text)

        st.subheader("🎯 Final Score")
        st.metric("Overall Score (out of 100)", f"{final_score:.2f}")

        st.subheader("📊 Breakdown")
        for category, score in breakdown.items():
            max_score = "10" if category in ['Grammar', 'Vocabulary', 'Sentence Complexity', 'Coherence'] else "15" if category in ['Clarity', 'Engagement'] else "20"
            st.write(f"**{category}:** {score:.1f}/{max_score}")

        # Add qualitative feedback
        st.subheader("💬 Feedback")
        if final_score >= 80:
            st.success("Excellent speech! Well-structured and engaging.")
        elif final_score >= 60:
            st.info("Good speech with room for improvement in some areas.")
        elif final_score >= 40:
            st.warning("Fair speech. Consider working on structure and clarity.")
        else:
            st.error("The speech needs significant improvement in multiple areas.")
