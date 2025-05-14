from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

@app.route("/")
def home():
    return "Portfolio Tracker API is running!"

@app.route("/price")
def get_price():
    symbol = request.args.get("symbol")
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    return jsonify({
        "symbol": symbol,
        "price": r.get("c"),
        "change": r.get("d"),
        "percent_change": r.get("dp")
    })

@app.route("/news")
def get_news():
    symbol = request.args.get("symbol")
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2025-04-01&to=2025-05-14&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    return jsonify(r[:5])

if __name__ == "__main__":
    app.run()
