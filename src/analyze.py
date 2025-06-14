import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from pathlib import Path
from collections import Counter
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def basic_stats(df):
    df["clean_text"] = df["risk_factors"].apply(clean_text)
    df["word_count"] = df["clean_text"].apply(lambda x: len(x.split()))
    print(df[["filename", "word_count"]])

    # Plot word count per filing
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x="filename", y="word_count")
    plt.xticks(rotation=45)
    plt.title("Word Count per Risk Factor Section")
    plt.tight_layout()
    plt.savefig("data/processed/risk_factor_word_counts.png")
    print("📊 Saved plot to data/processed/risk_factor_word_counts.png")

def top_keywords(df, n=20):
    all_words = " ".join(df["clean_text"]).split()
    most_common = Counter(all_words).most_common(n)
    print("🧠 Top Keywords:")
    for word, count in most_common:
        print(f"{word}: {count}")

    # Wordcloud
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(all_words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Top Keywords in Risk Factors")
    plt.tight_layout()
    plt.savefig("data/processed/risk_factor_wordcloud.png")
    print("☁️ Saved wordcloud to data/processed/risk_factor_wordcloud.png")

def compare_similarity(df):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["clean_text"])
    similarity = cosine_similarity(tfidf_matrix)

    # Display similarity matrix
    sim_df = pd.DataFrame(similarity, index=df["filename"], columns=df["filename"])
    print("\n🔍 Cosine Similarity Matrix:")
    print(sim_df.round(2))

    # Save heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(sim_df, annot=True, cmap="Blues", fmt=".2f")
    plt.title("Cosine Similarity of Risk Factor Texts")
    plt.tight_layout()
    plt.savefig("data/processed/risk_factor_similarity.png")
    print("🧯 Saved similarity heatmap to data/processed/risk_factor_similarity.png")

def main():
    input_csv = Path("data/processed/risk_factors.csv")
    df = pd.read_csv(input_csv)

    basic_stats(df)
    top_keywords(df)
    compare_similarity(df)

if __name__ == "__main__":
    main()