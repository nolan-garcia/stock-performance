import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Function to fetch company data from Yahoo Finance
def get_company_data(ticker):
    company = yf.Ticker(ticker)
    
    # Fetching key financials and info
    try:
        company_info = company.info
        financials = company.financials
        cash_flow = company.cashflow
        balance_sheet = company.balance_sheet
        historical_data = company.history(period="5y")  # Get 5 years of historical data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None, None, None, None, None, None
    
    return company_info, financials, cash_flow, balance_sheet, historical_data

# Function to get S&P 500 data
def get_sp500_data():
    # Get historical data for the S&P 500
    sp500 = yf.Ticker("^GSPC")  # S&P 500 symbol
    sp500_data = sp500.history(period="5y")['Close']  # Get last 5 years of closing prices
    return sp500_data

# Function to calculate annual percentage returns
def calculate_annual_percentage_returns(data):
    # Resample the data to get the first and last price for each year
    yearly_data = data.resample('Y').agg(['first', 'last'])

    # Flatten the multi-level columns
    yearly_data.columns = ['first', 'last']

    # Calculate the percentage return for each year
    pct_return = ((yearly_data['last'] - yearly_data['first']) / yearly_data['first']) * 100
    return pct_return

# Function to plot stock performance vs S&P 500 using Plotly (annual percentage returns)
def plot_stock_vs_sp500(historical_data, sp500_data, ticker):
    # Calculate annual percentage returns for the stock (Apple)
    stock_pct_return = calculate_annual_percentage_returns(historical_data['Close'])
    
    # Calculate annual percentage returns for S&P 500
    sp500_pct_return = calculate_annual_percentage_returns(sp500_data)
    
    # Create a Plotly line chart for the stock and S&P 500 performance
    st.subheader(f"Annual Stock Performance vs S&P 500 (Percentage Returns) for {ticker}")
    
    fig = go.Figure()

    # Add stock performance (percentage return) to the plot
    fig.add_trace(go.Scatter(x=stock_pct_return.index, 
                             y=stock_pct_return, 
                             mode='lines', 
                             name=f"{ticker} Performance",  # Dynamically set the stock ticker name here
                             line=dict(color='blue')))
    
    # Add S&P 500 performance (percentage return) to the plot
    fig.add_trace(go.Scatter(x=sp500_pct_return.index, 
                             y=sp500_pct_return, 
                             mode='lines', 
                             name="S&P 500 Performance",  # Static name for S&P 500
                             line=dict(color='green')))
    
    # Update layout for hover info
    fig.update_layout(
        title="Annual Stock Returns vs S&P 500 (Percentage Return)",
        xaxis_title="Year",
        yaxis_title="Percentage Return",
        hovermode="x unified",  # Show hover info on hover along the x-axis
        template="plotly_dark"
    )

    st.plotly_chart(fig)

# Streamlit App
def main():
    st.title('Stock Data Dashboard')

    # Input section: Get company ticker
    ticker = st.text_input("Enter Stock Ticker (e.g. AAPL)", 'AAPL')

    if ticker:
        st.markdown(f"### Displaying Data for **{ticker}**")

        # Fetch company data
        company_info, financials, cash_flow, balance_sheet, historical_data = get_company_data(ticker)

        if company_info:
            # Display Company Information in a more readable format
            st.markdown(f"### Company Information for **{ticker}**")

            # Display company info as key-value pairs
            info_dict = {
                "Company Name": company_info.get("shortName", "N/A"),
                "Industry": company_info.get("industry", "N/A"),
                "Sector": company_info.get("sector", "N/A"),
                "Country": company_info.get("country", "N/A"),
                "Market Cap": f"${company_info.get('marketCap', 0):,.0f}",
            }

            # Create a nice table format for company details
            st.table(info_dict)

            # Display Company’s Business Summary (formatted as text)
            st.markdown(f"**Business Summary:** {company_info['longBusinessSummary']}")

            # Display Financial Statements: Income Statement, Balance Sheet, and Cash Flow
            st.markdown("### Income Statement")
            st.dataframe(financials)

            st.markdown("### Balance Sheet")
            st.dataframe(balance_sheet)

            st.markdown("### Cash Flow Statement")
            st.dataframe(cash_flow)

            # Get S&P 500 data
            sp500_data = get_sp500_data()

            # Plot stock performance vs S&P 500 returns for the past 5 years
            plot_stock_vs_sp500(historical_data, sp500_data, ticker)

if __name__ == "__main__":
    main()
