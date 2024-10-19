import requests
import json
import pandas as pd
import csv
import io
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
csv_lock = threading.Lock()

def fetch_nse_stock_symbols():
    url = 'https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'nsearchives.nseindia.com',
        'Priority': 'u=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0'
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise error for bad responses

        df = pd.read_csv(io.StringIO(response.text))

        # Extract symbols from the first column
        symbols = df.iloc[:, 0].tolist()

        return symbols

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return []
    



def api(session, symbol):
    url = f'https://www.nseindia.com/api/quote-equity?symbol={symbol}'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.nseindia.com',
        'Priority': 'u=1',
        'TE': 'trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0'
    }
    response = session.get(url)
    
    try:
        data = response.json()
        return data
    except json.JSONDecodeError:
        print(f"Failed to fetch data for {symbol}: Response is not JSON")
        print(response.text)


def csv(data):

    try:
        # Initialize default values for keys that might be missing
        symbol = data.get("info", {}).get("symbol", None)
        open_price = data.get("priceInfo", {}).get("open", None)
        intra_day_high = data.get("priceInfo", {}).get("intraDayHighLow", {}).get("max", None)
        intra_day_low = data.get("priceInfo", {}).get("intraDayHighLow", {}).get("min", None)
        close_price = data.get("priceInfo", {}).get("close", None)
        last_price = data.get("priceInfo", {}).get("lastPrice", None)
        total_volume = data.get("preOpenMarket", {}).get("totalTradedVolume", None)
        company_name = data.get("info", {}).get("companyName", None)
        industry = f"{data['industryInfo'].get('industry', 'Unknown')} - {data['industryInfo'].get('basicIndustry', 'Unknown')}"
        pd_symbol_pe = data.get("metadata", {}).get("pdSymbolPe", None)
        face_value = data.get("securityInfo", {}).get("faceValue", None)
        sector = data.get("industryInfo", {}).get("sector", None)
        issued_size = data.get("securityInfo", {}).get("issuedSize", None)

        # Combine data into dictionaries
        technical_data = {
            "symbol": symbol,
            "open": open_price,
            "high": intra_day_high,
            "low": intra_day_low,
            "close": close_price,
            "lastPrice": last_price,
            "volume": total_volume
        }

        fundamental_data = {
            "symbol": symbol,
            "companyName": company_name,
            "industry": industry,
            "pdSymbolPe": pd_symbol_pe,
            "faceValue": face_value
        }

        company_details = {
            "symbol": symbol,
            "companyName": company_name,
            "industry": industry,
            "sector": sector,
            "faceValue": face_value,
            "issuedSize": issued_size
        }

        # Convert dictionaries to DataFrames
        fundamentals_and_pricing_df = pd.DataFrame([technical_data])
        company_details_df = pd.DataFrame([company_details])

        # Write to CSV files, appending data and handling headers
        write_header1 = not os.path.exists('fundamentals_and_pricing.csv')
        write_header2 = not os.path.exists('company_details.csv')
        with csv_lock:
            fundamentals_and_pricing_df.to_csv('fundamentals_and_pricing.csv', mode='a', index=False, header=write_header1)
            company_details_df.to_csv('company_details.csv', mode='a', index=False, header=write_header2)

    except KeyError as e:
        print(f"KeyError: {e} not found in data. Skipping entry.")
    except Exception as ex:
        print(f"Error: {ex}")



def process_symbols(symbols, headers):
    with requests.Session() as session:
        session.headers.update(headers)
        homepage_response = session.get('https://www.nseindia.com')

        futures = []
        for symbol in symbols:
            futures.append(executor.submit(api, session, symbol))

        for future in as_completed(futures):
            data = future.result()
            if data:
                csv(data)




if __name__ == "__main__":
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.nseindia.com',
        'Priority': 'u=1',
        'TE': 'trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0'
    }
    list = fetch_nse_stock_symbols()
    filetd1 = 'fundamentals_and_pricing.csv'
    if os.path.exists(filetd1):
        os.remove(filetd1)
    filetd2 = 'company_details.csv'
    if os.path.exists(filetd2):
        os.remove(filetd2)


    max_workers = 10
    executor = ThreadPoolExecutor(max_workers=max_workers)
    batch_size = 50
    for i in range(0, len(list), batch_size):
        batch_symbols = list[i:i + batch_size]
        process_symbols(batch_symbols, headers)