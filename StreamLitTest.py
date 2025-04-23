import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

stockCode = st.text_input("Stock code: ")
querry = st.text_input("Article search word: ")

dfStock = pd.read_csv(f"{stockCode}_stock_data.csv")

dfStock = dfStock.drop([0, 1])

# Replace the first header (modify column names)
new_header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']  # Example new header
dfStock.columns = new_header  # Set the new header to the DataFrame


# Load CSV
dfSentiment = pd.read_csv(f"{querry}_monthly_sentiment.csv", parse_dates=["Date"])


# buying the stocks
# budget = st.number_input("Enter your budget: ")
budget = 100000
balance = budget
portfolio = budget
shares = 0
for i in range(1, 12):
    date = dfSentiment["Date"][i].strftime("%Y-%m-%d")
    result = dfStock[dfStock["Date"] == date]
    if result.empty:
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date + timedelta(days=2)
        date = date.strftime("%Y-%m-%d")
        result = dfStock[dfStock["Date"] == date]
    # forgot to convert this to float
    price = float(result["Open"])
    if i != 0:
        sentimentSlope = dfSentiment["Sentiment"][i] - dfSentiment["Sentiment"][i - 1]
        # sentimentSlope = dfSentiment["Sentiment"][i]
        #  st.write(sentimentSlope)
        factor = 5
        buyShares = balance / price * sentimentSlope * factor
        shares += buyShares
        balance -= buyShares * price
        portfolio = balance + shares * price
        # if sentimentSlope > 0:
        #     st.write("Shares bought: ", buyShares, "Portfolio Value: ", portfolio, "Balance: ", balance)
        # else:
        #     st.write("Shares sold: ", buyShares, "Portfolio Value: ", portfolio, "Balance: ", balance)
    lastSentiment = dfSentiment["Sentiment"][i]

st.write("Portfolio Value: ", portfolio, "Gains: ", (portfolio - budget) / budget * 100, "%")



# plot
fig = go.Figure(data=[go.Candlestick(
    x=dfStock['Date'],
    open=dfStock['Open'],
    high=dfStock['High'],
    low=dfStock['Low'],
    close=dfStock['Close']
)])

fig.update_layout(title="Sample Candlestick Chart", xaxis_title="Date", yaxis_title="Price")

# Show in Streamlit
st.plotly_chart(fig)

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(dfSentiment["Date"], dfSentiment["Sentiment"], marker="o", linestyle="-")
ax.set_title("Daily Sentiment Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Sentiment Score")
ax.grid(True)
ax.tick_params(axis="x", rotation=45)

# Show the plot in Streamlit
st.pyplot(fig)