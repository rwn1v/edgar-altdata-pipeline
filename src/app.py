import dash
from dash import dcc, html, Output, Input
import pandas as pd
from summa.summarizer import summarize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from collections import Counter
import plotly.graph_objs as go
import re

# --- Summarization Function ---
def summarize_text(text, ratio=0.03):
    try:
        summary = summarize(text, ratio=ratio)
        return summary if summary else "Summary too short to generate."
    except ValueError:
        return "Summary could not be generated for this text."

# --- Sentiment Analysis Function ---
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    return f"🟢 Positive: {scores['pos']:.2f} | 🔴 Negative: {scores['neg']:.2f} | 😐 Neutral: {scores['neu']:.2f} | 🧠 Compound: {scores['compound']:.2f}"

# --- Word Frequency Function ---
def compute_word_frequencies(text, top_n=20):
    words = re.findall(r'\b\w+\b', text.lower())
    words = [word for word in words if word not in stopwords.words("english")]
    freq = Counter(words).most_common(top_n)
    return freq

# --- Load CSV ---
df = pd.read_csv("data/processed/risk_factors.csv")

# --- Dash App ---
app = dash.Dash(__name__)
app.title = "10-K Risk Factor Explorer"

# --- Layout ---
app.layout = html.Div([
    html.H1("📄 10-K Risk Factor Explorer"),

    html.Label("Choose a Filing:"),
    dcc.Dropdown(
        id="file-dropdown",
        options=[{"label": f, "value": f} for f in df["filename"]],
        value=df["filename"].iloc[0]
    ),

    html.Label("Summary Length (lower = shorter):"),
    dcc.Slider(
        id="summary-ratio-slider",
        min=0.01,
        max=0.3,
        step=0.01,
        value=0.03,
        marks={0.01: "Short", 0.1: "Default", 0.3: "Long"}
    ),

    html.Hr(),

    html.H3("Sentiment Analysis"),
    html.Div(id="sentiment-output", style={
        "whiteSpace": "pre-wrap",
        "border": "1px solid #e0e0ff",
        "padding": "10px",
        "backgroundColor": "#f0f0ff"
    }),

    html.H3("Top Words"),
    dcc.Graph(id="word-frequency-graph"),

    html.H3("Summary"),
    html.Div(id="summary-output", style={
        "whiteSpace": "pre-wrap",
        "border": "1px solid #eee",
        "padding": "10px",
        "backgroundColor": "#f9f9f9"
    }),

    html.Hr(),

    html.H2("Risk Factors Text"),
    html.Div(id="risk-text-box", style={
        "whiteSpace": "pre-wrap",
        "border": "1px solid #ccc",
        "padding": "10px"
    })
])

# --- Callback ---
@app.callback(
    [Output("risk-text-box", "children"),
     Output("summary-output", "children"),
     Output("sentiment-output", "children"),
     Output("word-frequency-graph", "figure")],
    [Input("file-dropdown", "value"),
     Input("summary-ratio-slider", "value")]
)
def update_outputs(selected_file, ratio):
    risk_text = df[df["filename"] == selected_file]["risk_factors"].values[0]

    if risk_text and "⚠️" not in risk_text:
        summary = summarize_text(risk_text, ratio=ratio)
        sentiment = analyze_sentiment(risk_text)
        word_freq = compute_word_frequencies(risk_text)
        words, freqs = zip(*word_freq)
        fig = go.Figure([go.Bar(x=words, y=freqs)])
        fig.update_layout(title="Top 20 Words", xaxis_title="Word", yaxis_title="Frequency")
    else:
        summary = "No summary available."
        sentiment = "No sentiment analysis available."
        fig = go.Figure()

    return risk_text, summary, sentiment, fig

# --- Run App ---
if __name__ == "__main__":
    import nltk
    nltk.download("stopwords")
    nltk.download("vader_lexicon")
    app.run(debug=True)