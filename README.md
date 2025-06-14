
# 10-K Risk Factor Explorer

This interactive Dash web app lets you explore and analyze the "Risk Factors" section from 10-K filings.

## 🔍 Features

- **Dropdown menu** to select a company filing from a dataset.
- **Automatic text summarization** using the TextRank algorithm.
- **Sentiment analysis** using VADER (NLTK).
- **Top keywords** bar chart based on word frequency.
- Adjustable **summary length** via slider.
- Display of full **Risk Factors** text.

## 🗂 Data Source

The data comes from pre-parsed 10-K filings stored in `data/processed/risk_factors.csv`. Each row includes:
- `filename`: Unique identifier for the filing.
- `risk_factors`: Extracted text content from the Risk Factors section.

## ▶️ How to Run

1. **Install dependencies** (preferably in a virtual environment):

```bash
pip install dash pandas plotly nltk summa
```

2. **Download NLTK data** (first time only):

```python
import nltk
nltk.download("stopwords")
nltk.download("vader_lexicon")
```

3. **Run the app**:

```bash
python app.py
```

4. Open your browser and go to `http://127.0.0.1:8050/`.

## 📁 Folder Structure

```
10k-risk-explorer/
├── data/
│   └── processed/
│       └── risk_factors.csv
├── app.py
└── README.md
```

## 📌 Future Ideas

- Upload and parse a custom 10-K.
- Add named entity recognition (NER) for companies, risks, etc.
- Support EDGAR live lookup by ticker.

---

Built with 💻 for educational and portfolio purposes.
