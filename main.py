from datetime import datetime, timedelta
from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# get current BTC price for top of page
COIN_KEY = os.environ.get("COIN_KEY")
url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
headers = {
    "X-CoinAPI-Key": f'{COIN_KEY}'
}
response = requests.get(url, headers=headers)
current_price = round(response.json()['rate'], 2)
formatted_price = "{:,.2f}".format(current_price)


# get 3 bitcoin articles from the last 30 days
current_date = datetime.now()
one_month_ago = current_date - timedelta(days=30)
formatted_date = one_month_ago.strftime('%Y-%m-%d')
NEWS_KEY = os.environ.get("NEWS_KEY")
news_url = f"https://api.marketaux.com/v1/news/all?search=bitcoin&filter_entities=true&published_after={formatted_date}&language=en&api_token={NEWS_KEY}"
news_request = requests.get(url=news_url)
news_data = news_request.json()
article_list = []
for article in news_data['data']:
    article_dict = {
        'title': article['title'],
        'description': article['description'],
        'link': article['url']
    }
    article_list.append(article_dict)

@app.route("/")
def home():
    return render_template("index.html", current_price=formatted_price, articles=article_list)


""" Note: in chrome developer tools, use: Console > document.body.contentEditable=true 
to be able to edit the webpage in the browser! """

if __name__ == "__main__":
    app.run(debug=True)
