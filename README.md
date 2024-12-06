# Stock Performance Dashboard

## Overview

This project provides an interactive **Stock Performance Dashboard** that allows users to compare the **annual percentage returns** of a selected stock (e.g., Apple) with the **S&P 500 index**. The dashboard leverages **Yahoo Finance API** to fetch historical stock data and calculate the percentage returns for the last 5 years.

### Key Features:
- Display company information such as market cap, industry, and sector.
- Show financial statements including the income statement, balance sheet, and cash flow statement.
- Compare the **percentage returns** of the selected stock vs the **S&P 500** using a **line graph**.
- Allows users to hover over the graph for detailed information on percentage returns for each year.

## Requirements

Before running the app, ensure you have the following Python packages installed:

- `streamlit`: For creating the web app interface.
- `yfinance`: To fetch stock data from Yahoo Finance.
- `plotly`: For interactive graphing of stock performance.
- `pandas`: For handling data manipulation and analysis.

You can install the required packages using:

```bash
pip install streamlit yfinance plotly pandas
