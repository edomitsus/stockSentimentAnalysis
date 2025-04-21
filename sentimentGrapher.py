import pandas as pd
import matplotlib.pyplot as plt

def plotSentiment(name):
    # Load CSV
    df = pd.read_csv(f"{name}_monthly_sentiment.csv", parse_dates=["Date"])

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["Sentiment"], marker="o", linestyle="-")
    plt.title("Daily Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plotSentiment("elon musk")