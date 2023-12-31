import csv
import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go


# Get BTC articles from news API
def get_bitcoin_articles():
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=7)
    formatted_date = one_month_ago.strftime('%Y-%m-%d')

    NEWS_KEY = os.environ.get("NEWS_KEY")
    news_url = f"https://api.marketaux.com/v1/news/all?search=bitcoin&filter_entities=true&published_after={formatted_date}&language=en&api_token={NEWS_KEY}"

    news_request = requests.get(url=news_url)
    news_data = news_request.json()
    print(news_data)

    article_list = []

    # Check if 'data' key exists in the response
    if 'data' in news_data:
        for article in news_data['data']:
            article_dict = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'link': article.get('url', '')
            }
            article_list.append(article_dict)
    else:
        print("Data key not found in the API response.")

    return article_list

# Get BTC graph data function
def btc_data_to_graph(period="1d", interval="1m"):
    """Get BTC price data for given intervals"""
    data = yf.download(tickers="BTC-USD",
                       period=period,
                       interval=interval,
                       auto_adjust=True)
    stock_prices = data['High']
    return stock_prices


# Graph the BTC data
def btc_graph(stock_prices, period="1d"):
    """Take BTC data and plot it to a line graph with plotly based on desired time interval"""
    fig = go.Figure()
    if period == "1d":
        fig.add_trace(go.Scatter(x=stock_prices.index, y=stock_prices.values, mode='lines', name='BTC-USD Price'))
        # Update layout and format y-axis
        fig.update_layout(
            title="Today's Bitcoin Price (1-minute intervals)",
            xaxis_title='Time (GMT)',
            yaxis_title='Price (USD)',
            yaxis=dict(tickformat=",.2f")
        )
    elif period == "7d":
        fig.add_trace(
            go.Scatter(x=stock_prices.index, y=stock_prices.values, mode='lines+markers', name='BTC-USD Daily Price'))
        # Update layout and format y-axis
        fig.update_layout(
            title='Bitcoin Price (1 day intervals)',
            xaxis_title='Day',
            yaxis_title='Price (USD)',
            yaxis=dict(tickformat=",.2f")
        )
    elif period == "1y":
        fig.add_trace(
            go.Scatter(x=stock_prices.index, y=stock_prices.values, mode='lines+markers', name='BTC-USD Monthly Price'))
        # Update layout and format y-axis
        fig.update_layout(
            title='Bitcoin Price (1 month intervals)',
            xaxis_title='Month',
            yaxis_title='Price (USD)',
            yaxis=dict(tickformat=",.2f", ),
            xaxis=dict(
                tickmode='array',  # Set tick mode to array
                tickvals=stock_prices.index.tolist(),  # Explicitly set tick values to include all months
                ticktext=stock_prices.index.strftime('%B').tolist()  # Format tick labels to display month names
            )
        )
    elif period == "10y":
        fig.add_trace(go.Scatter(x=stock_prices.index, y=stock_prices.values, mode='lines+markers',
                                 name='BTC-USD 10-Year Price'))
        # Update layout and format y-axis
        fig.update_layout(
            title='Bitcoin Price (past 10 years)',
            xaxis_title='Year',
            yaxis_title='Price (USD)',
            yaxis=dict(tickformat=",.2f"),
            xaxis=dict(
                tickmode='array',  # Set tick mode to array
                tickvals=stock_prices.index[::12].tolist(),  # Set tick values to every 12th index to represent years
                ticktext=stock_prices.index[::12].strftime('%Y').tolist()  # Format tick labels to display years
            )
        )
    return fig


# Most recent price function
def current_price():
    """Get price data for each minute of today and return the latest one"""
    btc_data = yf.download(tickers="BTC-USD",
                           period="1d",
                           interval="1m",
                           auto_adjust=True)
    btc_prices = btc_data['High']
    last_price = btc_prices.iloc[-1]
    formatted_price = "{:,.2f}".format(last_price)

    return formatted_price


# ticker search bar function
def search_companies(csv_file, search_term):
    """Take a company name and search a csv of companies/tickers to return the ticker symbol"""
    results = []

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present

        for row in reader:
            ticker, company_name = row
            if search_term.lower() in company_name.lower():
                results.append({'Ticker': ticker, 'Company Name': company_name})
    return results


today_date = datetime.now().strftime('%Y-%m-%d')


# get stock prices function
def get_stock_data(start_date: str, end_date=today_date, ticker="BTC-USD", interval='1wk'):
    """input a stock ticker and start/stop date with an interval of 1d, 1wk, or 1mo to get price date"""
    # Download historical data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

    # Extract the 'High' column from the data
    stock_prices = data['High']

    return stock_prices


# format stock data into dictionary
def format_stock_data(stock_data):
    """Takes stock data and creates a dataframe before converting it into a dictionary"""
    # create a dataframe variable of the stock data
    df = pd.DataFrame(stock_data)
    my_data_dict = df.to_dict()

    # initialize a blank dictionary
    stock_dict = {}

    # create a dictionary with proper formatting
    for outer_key, inner_dict in my_data_dict.items():
        for timestamp, price in inner_dict.items():
            date_str = timestamp.strftime('%Y-%m-%d')  # Convert timestamp to string in the desired format
            stock_dict[date_str] = price

    return stock_dict


# calculate dca return function
def dca_return(stock_dict, investment_amount: int):
    """Calculates investing results for the given amount and time span"""
    # initializes invested amount and shares owned
    investment = 0
    shares_purchased = 0

    for date, price in stock_dict.items():
        # Calculate the number of shares that can be bought with dca amount
        shares_bought = investment_amount / price

        # Update investment and total shares
        investment += investment_amount
        shares_purchased += shares_bought

    final_dollar_value = round(list(stock_dict.values())[-1] * shares_purchased, 2)
    final_gain_or_loss = round(final_dollar_value - investment, 2)
    roi = round(((final_dollar_value - investment) / investment) * 100, 2)

    return shares_purchased, final_dollar_value, final_gain_or_loss, roi


# lump sum investment results function
def lump_sum(stock_dict, investment: int):
    """Calculates a lump sum investment's results for a given timespan"""
    shares_purchased = investment / list(stock_dict.values())[0]
    final_dollar_value = round(list(stock_dict.values())[-1] * shares_purchased, 2)
    formatted_final_dollar_value = f"-${abs(final_dollar_value)}" if final_dollar_value < 0 else f"${final_dollar_value}"
    gain_or_loss = round(final_dollar_value - investment, 2)
    formatted_gain_or_loss = f"-${abs(gain_or_loss)}" if gain_or_loss < 0 else f"${gain_or_loss}"
    roi = round(((final_dollar_value - investment) / investment) * 100, 2)

    return formatted_final_dollar_value, formatted_gain_or_loss, roi, shares_purchased
