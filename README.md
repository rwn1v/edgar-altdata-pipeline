# 10-K Risk Factor Explorer

A dashboard application that parses, analyzes, and visualizes risk factor disclosures from SEC 10-K filings. This project is part of a broader alternative data pipeline for investment research and portfolio risk assessment.

Powered by:
- SEC EDGAR data
- Snowflake as the cloud data warehouse
- Dash for the interactive front end
- NLP techniques (TextRank summarization, VADER sentiment)

---

## Features

- Explore 10-K risk factor sections via dropdown
- Automatic text summarization using extractive NLP
- Sentiment analysis with VADER
- Word frequency analysis and bar chart visualization
- Connected to a Snowflake backend — no local CSVs needed

---

## How It Works

### 1. Data Ingestion
Filings are downloaded from EDGAR and parsed using Python scripts. Extracted risk factors are uploaded to Snowflake.

### 2. Dashboard Interface
The Dash app queries Snowflake directly and lets users:
- Select a specific filing
- Adjust summary length
- View sentiment metrics
- Visualize top words

---

## Technologies

- Python
- Dash (Plotly)
- Snowflake (`snowflake-connector-python`)
- NLTK (VADER, stopwords)
- Summa (TextRank summarization)
- Pandas

---

## File Structure

```
src/
├── app.py                   # Dash app UI and callbacks
├── analyze.py               # Text processing utilities
├── extract_risk_factors.py  # EDGAR parser
├── snowflake_query.py       # Upload CSV to Snowflake
├── snowflake_upload.py      # Snowflake connection test
data/
├── raw/                     # Raw EDGAR filings (optional)
├── processed/               # Parsed and cleaned output
notebooks/                   # Jupyter notebooks for exploration
```

---

## Setup

```bash
git clone https://github.com/rwn1v/edgar-altdata-pipeline.git
cd edgar-altdata-pipeline
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file at the project root (see `env.example`) and populate it with your Snowflake credentials.

Run the app:

```bash
python src/app.py
```

Then open [http://127.0.0.1:8050/](http://127.0.0.1:8050/) in your browser.

---

## Future Enhancements

- Live EDGAR data pull by ticker
- Topic modeling for deeper NLP insights
- Cross-year risk factor comparison
- Upload support for local 10-Ks
- Support for 10-Q and international filings

---

## Author

Erwin Villarreal — [LinkedIn](https://www.linkedin.com/in/erwin-villarreal/)
