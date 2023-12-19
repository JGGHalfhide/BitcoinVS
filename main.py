from datetime import datetime, timedelta
from flask import Flask, render_template, request
import requests
import os
from functions import search_companies, get_stock_data, format_stock_data, dca_return, lump_sum

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
one_month_ago = current_date - timedelta(days=14)
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


@app.route('/', methods=['GET', 'POST'])
def home():
    search_results = None  # Initialize search results
    result_message = None  # Initialize the result of DCA

    if request.method == 'POST':
        search_term = request.form.get('searchTerm')
        if search_term:
            search_results = search_companies('static/csv/stocks.csv', search_term)
        else:
            start_date_str = request.form.get('inputValue5')
            end_date_str = request.form.get('inputValue6')
            # Format dates to "yyyy-mm-dd"
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            invested_amount = int(request.form.get('inputValue7'))
            investment_frequency = request.form.get('selectedOption')
            daily_data = get_stock_data(start_date, end_date, ticker="BTC-USD", interval='1d')
            daily_data_dict = format_stock_data(daily_data)
            weekly_data = get_stock_data(start_date, end_date, ticker="BTC-USD", interval='1wk')
            weekly_data_dict = format_stock_data(weekly_data)
            monthly_data = get_stock_data(start_date, end_date, ticker="BTC-USD", interval='1mo')
            monthly_data_dict = format_stock_data(monthly_data)
            if investment_frequency == 'lump':
                final_dollar_value, gain_or_loss, roi, shares_purchased = lump_sum(daily_data_dict, invested_amount)
                result_message = f"Final dollar value: ${final_dollar_value} | USD return: ${gain_or_loss} | Total BTC: {round(shares_purchased, 6)} | ROI: {roi}%"
            elif investment_frequency == '1d':
                shares_purchased, final_dollar_value, final_gain_or_loss, roi = dca_return(daily_data_dict, invested_amount)
                result_message = f"Final dollar value: ${final_dollar_value} | USD return: ${final_gain_or_loss} | Total BTC: {round(shares_purchased, 6)} | ROI: {roi}%"
            elif investment_frequency == '1wk':
                shares_purchased, final_dollar_value, final_gain_or_loss, roi = dca_return(weekly_data_dict, invested_amount)
                result_message = f"Final dollar value: ${final_dollar_value} | USD return: ${final_gain_or_loss} | Total BTC: {round(shares_purchased, 6)} | ROI: {roi}%"
            elif investment_frequency == '1mo':
                shares_purchased, final_dollar_value, final_gain_or_loss, roi = dca_return(monthly_data_dict, invested_amount)
                result_message = f"Final dollar value: ${final_dollar_value} | USD return: ${final_gain_or_loss} | Total BTC: {round(shares_purchased, 6)} | ROI: {roi}%"

    return render_template("index.html", current_price=formatted_price, articles=article_list, search_results=search_results, get_stock_data=get_stock_data, result_message=result_message)


if __name__ == "__main__":
    app.run(debug=True)
