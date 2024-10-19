# 📊 autonse


This project is a Python-based automation script that collects real-time stock data from the National Stock Exchange of India (NSE) and saves it into CSV files for further analysis. The data includes technical and fundamental stock details such as stock prices, volumes, company information, and more.

## 📋 Project Overview

This script uses multithreading to improve performance by making API calls concurrently for multiple stock symbols. It significantly reduces the time required to collect stock data.

The collected data is stored in two separate CSV files:
- **fundamentals_and_pricing.csv** - Contains stock prices and volume details.
- **company_details.csv** - Contains company-specific details like industry and sector information.

### Key Features

- 🧵 **Multithreading**: Fetch stock data faster by using concurrent API requests.
- 📁 **CSV Output**: Save the data into easy-to-read CSV files.
- 🔍 **NSE Stock Data**: Get detailed stock prices, company information, and more directly from NSE.
- 🛠️ **Error Handling**: Robust error handling for missing or invalid data.

## 🏗️ Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:chiragsingla014/autonse.git
    cd autonse
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 How to Use

1. Run the script:
    ```bash
    python main.py
    ```

2. The script fetches data from NSE, and the results will be saved in `fundamentals_and_pricing.csv` and `company_details.csv`.

3. You can adjust the `batch_size` and `max_workers` in the script to optimize for your machine’s performance.

## 🗂️ Files

- **main.py** - Main script for fetching stock data.
- **requirements.txt** - List of required Python packages.
- **fundamentals_and_pricing.csv** - Output file with stock prices and technical data.
- **company_details.csv** - Output file with company details and fundamentals.

## 🧰 Technologies Used

- **Python 🐍**
- **Requests** for API calls 🌐
- **Pandas** for CSV data handling 📊
- **ThreadPoolExecutor** for multithreading 🧵

## 🤝 Contributing

Contributions are welcome! If you would like to contribute, feel free to open an issue or a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

