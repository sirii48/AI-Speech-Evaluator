import streamlit as st
from scoring import (
    calculate_simplified_final_score,
    content_and_structure_score,
    speech_rate_score,
    language_and_grammar_score,
    clarity_score,
    engagement_score
)

st.set_page_config(page_title="Speech Evaluator", page_icon="🎤")

st.title("🎤 Speech Evaluation Tool")

# Professional Styling
st.markdown("""
    <style>
        .stTextArea textarea:focus { border-color: #1E90FF !important; }
        .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.write("Paste any text—be it a personal intro or a news article—to evaluate its quality as a speech.")

text = st.text_area("Enter transcript:", height=250, placeholder="Paste text here...")

if st.button("Evaluate"):
    if not text.strip():
        st.error("Please enter some text!")
    else:
        # Scoring Logic
        f_score = calculate_simplified_final_score(text)
        cs = content_and_structure_score(text)
        sr = speech_rate_score(text)
        lg = language_and_grammar_score(text)
        cl = clarity_score(text)
        eg = engagement_score(text)

        st.divider()
        
        # Display Final Score
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("🎯 Overall Score")
            st.metric("", f"{f_score:.1f}/100")
        
        with col2:
            st.subheader("📊 Breakdown")
            
            st.write(f"Content & Structure ({cs}/40)")
            st.progress(cs / 40)
            
            st.write(f"Speech Rate Flow ({sr}/10)")
            st.progress(sr / 10)
            
            st.write(f"Language & Vocabulary ({lg}/20)")
            st.progress(lg / 20)
            
            st.write(f"Clarity ({cl}/15)")
            st.progress(cl / 15)
            
            st.write(f"Engagement/Sentiment ({eg}/15)")
            st.progress(eg / 15)

        st.success("Evaluation complete! Wikipedia text will now score much higher in structure and language.")
