# Nirmaan Education - Speech Evaluation Tool

The tool evaluates a text and generates a final score along with a breakdown.

---

## 🚀 Features

- Takes transcript text as input  
- Uses rule-based and NLP-based techniques  
- Generates:
  - Final score (0–100)
  - Content & Structure score
  - Speech rate score
  - Language & Grammar score
  - Clarity score
  - Engagement score
- Simple and user-friendly Streamlit UI

---

## 🧠 Scoring Rubric (Simplified)

| Criterion               | Maximum  |
|-------------------------|----------|
| Content & Structure     | 40       |
| Speech Rate             | 10       |
| Language & Grammar      | 20       |
| Clarity                 | 15       |
| Engagement              | 15       |
| **Total**               | **100**  |

The complete scoring logic is implemented inside **`scoring.py`**.

---

## 🛠️ Installation

### 1. Clone the repo (after uploading to GitHub)

```bash
git clone https://github.com/sirii48/AI-Speech-Evaluator
cd AI-Speech-Evaluator
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Download NLTK data (first-time only)

```python
import nltk
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
```

---

## ▶️ Running the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Your browser will open automatically.

---

## 📂 Project Structure

```
├── app.py               # Streamlit UI
├── scoring.py           # Scoring logic
├── requirements.txt     # Required libraries
└── README.md            # Project documentation
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push this project to GitHub  
2. Go to **https://share.streamlit.io**  
3. Log in with GitHub  
4. Select your repository  
5. Choose `app.py` as the entry point  
6. Click **Deploy**  

Your app will receive a public link.

---

