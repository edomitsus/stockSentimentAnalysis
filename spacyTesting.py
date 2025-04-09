import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from duckduckgo_search import DDGS
ddgs = DDGS()
from GoogleNews import GoogleNews
from datetime import datetime, timedelta
import pandas
from dateutil.relativedelta import relativedelta

# load google news up here
googlenews = GoogleNews()

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def searchDDGS(keyword):
    results = ddgs.text(keywords=keyword, region='wt-wt', safesearch='Off', timelimit='d')
    for r in results:
        sentimentVADER(r["title"])

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

def sentimentBLOB(text):
    # Load the spaCy model
    nlp = spacy.load('en_core_web_sm')

    # Add the spacytextblob pipeline component to the spaCy model
    nlp.add_pipe('spacytextblob')

    # Process the text with spaCy
    doc = nlp(text)

    polarity = doc._.blob.polarity
    subjectivity = doc._.blob.subjectivity

    # Print results
    print("Text:", text)
    print("Polarity:", polarity)
    print("Subjectivity:", subjectivity)

    # Optional: Interpret sentiment
    if polarity > 0:
        print("→ Positive sentiment")
    elif polarity < 0:
        print("→ Negative sentiment")
    else:
        print("→ Neutral sentiment")


def sentimentVADER(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract the cleaned text (optional: you can process it more thoroughly with spaCy if needed)
    cleaned_text = " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])

    # Perform sentiment analysis with VADER
    vader_score = analyzer.polarity_scores(cleaned_text)['compound']

    # print("Title: ", text)
    # print(vader_score)

    return vader_score

    # # print the text
    # print("Title: ", text)

    # # Print the sentiment score
    # print(f"VADER Sentiment Score: {vader_score}")
    # if vader_score > 0:
    #     print("→ Positive sentiment")
    # elif vader_score < 0:
    #     print("→ Negative sentiment")
    # else:
    #     print("→ Neutral sentiment")


# searchDay("tesla", '2024-12-31')

def dailySentiment(keyword, startDate, endDate):
    sentimentList = []
    startd = datetime.strptime(startDate, "%Y-%m-%d")
    endd = datetime.strptime(endDate, "%Y-%m-%d")
    totalDays = (endd - startd).days + 1
    for i in range(totalDays):
        date = ( startd + timedelta(days=i) ).strftime("%Y-%m-%d")
        sentimentList.append([date, searchDay(keyword, date)])
    # print(sentimentList)

    pd = pandas.DataFrame(sentimentList, columns=["Date", "Sentiment"])
    pd.to_csv(f"{keyword}_daily_sentiment.csv", index=False)

def monthlySentiment(keyword, startDate, endDate):
    sentimentList = []
    startd = datetime.strptime(startDate, "%Y-%m-%d")
    endd = datetime.strptime(endDate, "%Y-%m-%d")
    totalMonths = (endd - startd).days + 1
    for i in range(0, totalMonths, 30):
        date = ( startd + timedelta(days=i) ).strftime("%Y-%m-%d")
        sentimentList.append([date, searchDay(keyword, date)])

    pd = pandas.DataFrame(sentimentList, columns=["Date", "Sentiment"])
    pd.to_csv(f"{keyword}_monthly_sentiment.csv", index=False)

# dailySentiment("elon musk", "2025-03-08", "2025-04-08")
monthlySentiment("economy", "2024-04-08", "2025-04-08")

# COMMIT COMMIT

# searchDay("tesla", "2020-01-01")


# sentimentList = [["2025-01-01", -0.1], ["2025-01-02", -0.4]]
# pd = pandas.DataFrame(sentimentList, columns=["Date", "Sentiment"])
# pd.to_csv("test_month_sentiment.csv", index=False)