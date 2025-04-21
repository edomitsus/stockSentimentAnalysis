import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime

name = "META"

st.write("Here's our first attempt at using data to create a table:")
dfStock = pd.read_csv(f"{name}_stock_data.csv")

dfStock = dfStock.drop([0, 1])

# Replace the first header (modify column names)
new_header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']  # Example new header
dfStock.columns = new_header  # Set the new header to the DataFrame


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

# Load CSV
dfSentiment = pd.read_csv("meta zuckerberg_monthly_sentiment.csv", parse_dates=["Date"])

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

# buying the stocks
budget = st.text_input("Enter your budget: ")
shares = 0
for i in range(12):
    date = dfSentiment["Date"][i].strftime("%Y-%m-%d")
    result = dfStock[dfStock["Date"] == date]
    st.write(result)
    # st.write(dfStock['Date'])