from datetime import datetime, timedelta
from flask import Flask, render_template, request
import requests
import os
from functions import current_price, search_companies, get_stock_data, format_stock_data, dca_return, lump_sum

app = Flask(__name__)

# get current BTC price for top of page
current_price = current_price()


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
    btc_vs_results = None  # Initialize the result of BTC vs form
    dca_result_message = None  # Initialize the result of DCA

    if request.method == 'POST':
        if "searchTerm" in request.form:
            search_term = request.form.get('searchTerm')
            search_results = search_companies('static/csv/stocks.csv', search_term)
        elif "inputValue5" in request.form:
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
                formatted_final_dollar_value, formatted_gain_or_loss, roi, shares_purchased = lump_sum(daily_data_dict, invested_amount)
                dca_result_message = (
                    f"<strong>Final USD value:</strong> {formatted_final_dollar_value}<br>"
                    f"<strong>USD return:</strong> {formatted_gain_or_loss}<br>"
                    f"<strong>Total BTC:</strong> {round(shares_purchased, 6)}<br>"
                    f"<strong>ROI:</strong> {roi}%"
                )
            elif investment_frequency == '1d':
                shares_purchased, final_dollar_value, final_gain_or_loss, roi = dca_return(daily_data_dict, invested_amount)
                dca_result_message = (
                    f"<strong>Final USD value:</strong> ${final_dollar_value}<br>"
                    f"<strong>USD return:</strong> ${final_gain_or_loss}<br>"
                    f"<strong>Total BTC:</strong> {round(shares_purchased, 6)}<br>"
                    f"<strong>ROI:</strong> {roi}%"
                )
            elif investment_frequency == '1wk':
                shares_purchased, final_dollar_value, final_gain_or_loss, roi = dca_return(weekly_data_dict, invested_amount)
                dca_result_message = (
                    f"<strong>Final USD value:</strong> ${final_dollar_value}<br>"
                    f"<strong>USD return:</strong> ${final_gain_or_loss}<br>"
                    f"<strong>Total BTC:</strong> {round(shares_purchased, 6)}<br>"
                    f"<strong>ROI:</strong> {roi}%"
                )
            elif investment_frequency == '1mo':
                shares_purchased, final_dollar_value, final_gain_or_loss, roi = dca_return(monthly_data_dict, invested_amount)
                dca_result_message = (
                    f"<strong>Final USD value:</strong> ${final_dollar_value}<br>"
                    f"<strong>USD return:</strong> ${final_gain_or_loss}<br>"
                    f"<strong>Total BTC:</strong> {round(shares_purchased, 6)}<br>"
                    f"<strong>ROI:</strong> {roi}%"
                )
        elif "inputValue1" in request.form:
            ticker = request.form.get('inputValue1')
            stock_start_date_str = request.form.get('inputValue3')
            stock_end_date_str = request.form.get('inputValue4')
            # Format dates to "yyyy-mm-dd"
            stock_start_date_formatted = datetime.strptime(stock_start_date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            stock_end_date_formatted = datetime.strptime(stock_end_date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            # Get the investment amount and the stock price data for the given ticker
            investment = int(request.form.get('inputValue2'))
            stock_data = get_stock_data(stock_start_date_formatted, stock_end_date_formatted, ticker=ticker, interval='1d')
            stock_data_dict = format_stock_data(stock_data)
            # Run the stock through the lump sum function
            stock_results = lump_sum(stock_data_dict, investment)
            # Get the BTC results for the same time period and investment
            btc_data = get_stock_data(stock_start_date_formatted, stock_end_date_formatted, ticker="BTC-USD", interval='1d')
            btc_data_dict = format_stock_data(btc_data)
            btc_results = lump_sum(btc_data_dict, investment)
            # Use a list to store the stock and BTC results
            results = [stock_results, btc_results]
            btc_vs_results = (
                f"Bitcoin's <strong>USD return</strong> was {results[1][1]} vs {ticker}'s {results[0][1]}<br>"
                f"Bitcoin's <strong>ROI</strong> was {results[1][2]}% vs {ticker}'s {results[0][2]}%<br>"
                f"Bitcoin's <strong>final USD value</strong> was {results[1][0]} vs {ticker}'s {results[0][0]}"
            )

    return render_template("index.html", current_price=current_price, articles=article_list, search_results=search_results, get_stock_data=get_stock_data, dca_result_message=dca_result_message, btc_vs_results=btc_vs_results)


if __name__ == "__main__":
    app.run(debug=True)
