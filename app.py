from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

BITCOIN_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=true&include_last_updated_at=false"
BITCOIN_GAS_API_URL = "https://mempool.space/api/v1/fees/mempool-blocks"
ETHEREUM_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=true&include_last_updated_at=false"
ETHEREUM_GAS_API_URL = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=761AJ5NJ93VZPZ96PFD3QBWBMJMEAZ5SB5"
BITCOIN_DOMINANCE_API_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=125&page=1&sparkline=false"
FEAR_GREED_API_URL = "https://api.alternative.me/fng/"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/bitcoin")
def bitcoin_price():
    try:
        response = requests.get(BITCOIN_API_URL, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request to {BITCOIN_API_URL} failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500


@app.route("/bitcoin_gas")
def bitcoin_gas():
    try:
        response = requests.get(BITCOIN_GAS_API_URL, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request to {BITCOIN_GAS_API_URL} failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500


@app.route("/ethereum")
def ethereum_price():
    try:
        response = requests.get(ETHEREUM_API_URL, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request to {ETHEREUM_API_URL} failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500


@app.route("/ethereum_gas")
def ethereum_gas_price():
    try:
        response = requests.get(ETHEREUM_GAS_API_URL, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request to {ETHEREUM_GAS_API_URL} failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500


@app.route("/btc_dominance")
def btc_dominance():
    try:
        response = requests.get(BITCOIN_DOMINANCE_API_URL, timeout=60)
        response.raise_for_status()

        # Parse the JSON content from the response
        data = response.json()

        # Initialize altCap
        altCap = 0

        # Iterate through the parsed data
        for x in data:
            if x["id"] == "bitcoin":
                BTCCap = x["market_cap"]
            altCap += x["market_cap"]

        dominance = (BTCCap / altCap) * 100
        return jsonify({"data": [{"value": dominance}]})

    except requests.exceptions.RequestException as e:
        print(f"Request to {BITCOIN_DOMINANCE_API_URL} failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500


@app.route("/fear_greed")
def fear_greed():
    try:
        response = requests.get(FEAR_GREED_API_URL, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request to {FEAR_GREED_API_URL} failed: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500


if __name__ == "__main__":
    app.run(debug=True)
