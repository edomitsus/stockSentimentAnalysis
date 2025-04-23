import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the stock ticker symbol (e.g., "AAPL" for Apple)
stock_symbol = "^GSPC"

# Set the date range for the data you want (e.g., from 2020-01-01 to 2024-01-01)
start_date = "2024-04-08"
end_date = "2025-04-08"

# Download stock data using yfinance
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Save the data to a CSV file
stock_data.to_csv(f"{stock_symbol}_stock_data.csv")

df = pd.read_csv(f"{stock_symbol}_stock_data.csv")
df = df.drop([0, 1])
print(df.head())

# Step 3: Replace the first header (modify column names)
new_header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']  # Example new header
df.columns = new_header  # Set the new header to the DataFrame

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()