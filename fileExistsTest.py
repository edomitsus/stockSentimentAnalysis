from pathlib import Path

stockCode = "AAPL"
querry = "apple"

stockFile = Path(f"{stockCode}_stock_data.csv")
querryFile = Path(f"{querry}_monthly_sentiment.csv")

print(stockFile.exists())
print(querryFile.exists())
