# 10-K Risk Factor Explorer

A dashboard application that parses, analyzes, and visualizes risk factor disclosures from 10-K filings using data sourced from the SEC EDGAR system. This project is part of a broader alternative data pipeline for investment research and portfolio risk assessment.

## Features

- Visual interface to explore 10-K risk factor sections
- Automatic text summarization using extractive NLP techniques
- Sentiment analysis using VADER
- Word frequency analysis and bar chart visualization

## How It Works

1. **Preprocessed Data**: A `risk_factors.csv` file is created from scraped and parsed 10-K filings.
2. **App Interface**: A Dash web application loads the risk factor texts and allows users to:
   - Select a specific filing
   - Adjust summary length
   - View sentiment metrics
   - Explore word frequency distribution

## Technologies

- Python
- Dash (Plotly)
- NLTK (VADER, stopwords)
- Summa (TextRank-based summarization)
- Pandas
- Plotly

## File Structure

```
src/
├── app.py                   # Main Dash application
├── analyze.py               # Text analysis helper functions
├── extract_risk_factors.py  # Parsing 10-K HTML and extracting text
data/
├── raw/                     # Raw downloaded HTML files
├── processed/               # CSV files and visualizations
notebooks/                   # Exploration and helper notebooks
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rwn1v/edgar-altdata-pipeline.git
   cd edgar-altdata-pipeline
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python src/app.py
   ```

## Future Enhancements

- Live data pull using EDGAR API by ticker
- Topic modeling for deeper NLP insights
- Cross-year risk factor similarity
- Support for 10-Q and international filings

## Author

Erwin Villarreal — [LinkedIn](https://www.linkedin.com/in/erwin-villarreal)
