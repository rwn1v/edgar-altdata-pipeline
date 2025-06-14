import requests
from pathlib import Path
import time

def download_10k(ticker="MSFT", num_filings=3):
    cik_lookup_url = f"https://www.sec.gov/files/company_tickers.json"
    cik_response = requests.get(cik_lookup_url, headers={"User-Agent": "erwin.villarreal@gmail.com"})
    cik_data = cik_response.json()
    
    # Lookup CIK
    cik = None
    for _, company in cik_data.items():
        if company['ticker'].upper() == ticker.upper():
            cik = str(company['cik_str']).zfill(10)
            break
    if cik is None:
        print("CIK not found.")
        return

    print(f"CIK for {ticker} is {cik}")

    # Query 10-K filings
    filings_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    filings_response = requests.get(filings_url, headers={"User-Agent": "erwin.villarreal@gmail.com"})
    filings = filings_response.json()["filings"]["recent"]

    # Filter for 10-K filings
    paths = [filings["primaryDocument"][i] for i in range(len(filings["form"])) if filings["form"][i] == "10-K"]
    accession_numbers = [filings["accessionNumber"][i].replace("-", "") for i in range(len(filings["form"])) if filings["form"][i] == "10-K"]

    download_dir = Path("data/raw/10-K")
    download_dir.mkdir(parents=True, exist_ok=True)

    for i in range(min(num_filings, len(paths))):
        acc = accession_numbers[i]
        doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{paths[i]}"
        res = requests.get(doc_url, headers={"User-Agent": "erwin.villarreal@gmail.com"})
        with open(download_dir / f"{ticker}_10K_{i+1}.html", "w", encoding="utf-8") as f:
            f.write(res.text)
        print(f"Saved {paths[i]}")
        time.sleep(0.5)  # Be kind to SEC servers

if __name__ == "__main__":
    download_10k()