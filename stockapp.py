import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
from pathlib import Path
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from dateutil.relativedelta import relativedelta
import time

# load google news up here
googlenews = GoogleNews()

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def searchDay(keyword, date):
    # googlenews = GoogleNews(start=startDate,end=endDate)
    # googlenews.set_time_range('01/01/2025', '01/01/2025')
    # googlenews = GoogleNews()
    d = datetime.strptime(date, "%Y-%m-%d")
    nextd = d + timedelta(days=1)
    nextDay = nextd.strftime("%Y-%m-%d")
    print(date)
    # search for stock keyword 
    googlenews.search(f"{keyword} after:{date} before:{nextDay}")
    total = 0
    googlenews.getpage(1)
    numArticles = 0
    for result in googlenews.results():
        total += sentimentVADER(result['title'])
        numArticles += 1
    print(total/numArticles)
    return total/numArticles

def sentimentVADER(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract the cleaned text (optional: you can process it more thoroughly with spaCy if needed)
    cleaned_text = " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])

    # Perform sentiment analysis with VADER
    vader_score = analyzer.polarity_scores(cleaned_text)['compound']

    return vader_score

def dailySentiment(keyword, startDate, endDate):
    sentimentList = []
    startd = datetime.strptime(startDate, "%Y-%m-%d")
    endd = datetime.strptime(endDate, "%Y-%m-%d")
    totalDays = (endd - startd).days + 1
    for i in range(totalDays):
        date = ( startd + timedelta(days=i) ).strftime("%Y-%m-%d")
        sentimentList.append([date, searchDay(keyword, date)])

    df = pd.DataFrame(sentimentList, columns=["Date", "Sentiment"])
    df.to_csv(f"{keyword}_daily_sentiment.csv", index=False)

def monthlySentiment(keyword, startDate, endDate):
    progress_text = "Searching articles..."
    my_bar = st.progress(0, progress_text)
    sentimentList = []
    startd = datetime.strptime(startDate, "%Y-%m-%d")
    endd = datetime.strptime(endDate, "%Y-%m-%d")
    totalMonths = (endd - startd).days + 1
    for i in range(0, totalMonths, 30):
        date = ( startd + timedelta(days=i) ).strftime("%Y-%m-%d")
        sentimentList.append([date, searchDay(keyword, date)])
        my_bar.progress(i/totalMonths, progress_text)
    my_bar.progress(100, "Search complete")

    df = pd.DataFrame(sentimentList, columns=["Date", "Sentiment"])
    df.to_csv(f"{keyword}_monthly_sentiment.csv", index=False)

st.header("Buying stocks over one year using sentiment analysis of articles")
# ask for budget, set placeholder to 0 or else error occurs
budget = int(st.text_input("Budget ($)", value=0))
stockCode = st.text_input("Stock code: ")
querry = st.text_input("Article search word: ")

if st.button("Submit", key="submit1"):
    stockFile = Path(f"{stockCode}_stock_data.csv")
    querryFile = Path(f"{querry}_monthly_sentiment.csv")

    # Set the date range for the data you want (e.g., from 2020-01-01 to 2024-01-01)
    start_date = "2024-04-08"
    end_date = "2025-04-08"

    if not stockFile.exists():

        # Download stock data using yfinance: 05/10 CHANGED ARGUMENT auto_adgjust default to true
        stock_data = yf.download(stockCode, start=start_date, end=end_date, auto_adjust=False)

        # Save the data to a CSV file
        stock_data.to_csv(f"{stockCode}_stock_data.csv")

    # check if data has already been recorded
    if not querryFile.exists():

        monthlySentiment(querry, start_date, end_date)
    else:
        # make loading bar for here too??
        progress_text = "Searching Articles..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.03)
            my_bar.progress(percent_complete + 1, text=progress_text)

    dfStock = pd.read_csv(f"{stockCode}_stock_data.csv")

    dfStock = dfStock.drop([0, 1])

    # Replace the first header (modify column names)
    new_header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']  # Example new header
    dfStock.columns = new_header  # Set the new header to the DataFrame


    # Load CSV
    dfSentiment = pd.read_csv(f"{querry}_monthly_sentiment.csv", parse_dates=["Date"])


    # buying the stocks
    # budget = st.number_input("Enter your budget: ")
    # budget = 100000
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

    # CHANGE COLOR OF TEXT DEPENDING ON GAIN/LOSS

    # remember to round portfolio value to 2 decimals
    if portfolio >= budget:
        st.header(f"Portfolio Value: :green[${round(portfolio, 2)}]")
        st.header(f"Gains: :green[+{round((portfolio - budget) / budget * 100, 2)} %]")
    else:
        st.header(f"Portfolio Value: :red[${round(portfolio, 2)}]")
        st.header(f"Gains: :red[{round((portfolio - budget) / budget * 100, 2)} %]") #dont need the - sign for negative, its already there



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