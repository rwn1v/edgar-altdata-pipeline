from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_risk_factors_by_lines(text):
    # Clean and split lines
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    start_idx = end_idx = None

    # Find start of "Item 1A. Risk Factors"
    for i, line in enumerate(lines):
        if re.search(r"item\s*1a", line, re.IGNORECASE) and "risk factor" in line.lower():
            start_idx = i
            break

    # Find end of section (Item 1B or Item 2)
    if start_idx is not None:
        for j in range(start_idx + 1, len(lines)):
            if re.match(r"item\s+1b", lines[j], re.IGNORECASE) or re.match(r"item\s+2", lines[j], re.IGNORECASE):
                end_idx = j
                break

    if start_idx is not None and end_idx is not None:
        return "\n".join(lines[start_idx:end_idx])
    elif start_idx is not None:
        return "\n".join(lines[start_idx:])
    else:
        return None

def main():
    input_dir = Path("data/raw/10-K")
    output_csv = Path("data/processed/risk_factors.csv")
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    records = []

    for file in sorted(input_dir.glob("*.html")):
        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            raw_text = soup.get_text(separator="\n")
            risk_text = extract_risk_factors_by_lines(raw_text)

            records.append({
                "filename": file.name,
                "risk_factors": risk_text if risk_text else "⚠️ NOT FOUND"
            })

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {len(df)} records to {output_csv}")

if __name__ == "__main__":
    main()