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
    return fetch_price(symbol)

@app.route("/prices")
def get_prices():
    symbols = request.args.get("symbols", "")
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    results = {}

    for symbol in symbol_list:
        data = fetch_price_data(symbol)
        if data:
            results[symbol] = data

    return jsonify(results)

@app.route("/news")
def get_news():
    symbol = request.args.get("symbol")
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2025-04-01&to=2025-05-14&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    return jsonify(r[:5])

def fetch_price_data(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    if "c" in r:
        return {
            "price": r["c"],
            "change": r["d"],
            "percent_change": r["dp"]
        }
    return None

def fetch_price(symbol):
    data = fetch_price_data(symbol)
    if not data:
        return jsonify({"error": "Invalid symbol"}), 404
    return jsonify({
        "symbol": symbol,
        **data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
