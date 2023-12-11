from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# get current BTC price
COIN_KEY = os.environ.get("COIN_KEY")
url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
headers = {
    "X-CoinAPI-Key": f'{COIN_KEY}'
}
response = requests.get(url, headers=headers)
current_price = round(response.json()['rate'], 2)
formatted_price = "{:,.2f}".format(current_price)


@app.route("/")
def home():
    return render_template("index.html", current_price=formatted_price)


""" Note: in chrome developer tools, use: Console > document.body.contentEditable=true 
to be able to edit the webpage in the browser! """

if __name__ == "__main__":
    app.run(debug=True)
