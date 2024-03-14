# BitcoinVS Flask Web Application
![Screenshot 2023-12-26 at 8 07 09 PM](https://github.com/JGGHalfhide/BitcoinVS/assets/141737227/a14b986b-e87b-4ad0-a6ca-ea6ca4155018)
BitcoinVS is a comprehensive web application built with Flask for backend operations and Bootstrap, HTML, CSS, and JavaScript for frontend development. The primary goal of the application is to provide users with insights into Bitcoin price trends, stock comparisons, investment scenarios, and the latest Bitcoin-related news. Visit the live website at <https://BitcoinVS.onrender.com>. Please note, render's free hosting tier disables the site when not accessed for 15 or more minutes. Therefore, if your request times out, please simply refresh the page and allow it to load.

## Features:

1. **Price Charts**: Users can visualize Bitcoin price trends over various time spans using charts generated with Plotly.
  
2. **Stock Comparison**: Search for stock tickers and compare their performance with Bitcoin's price over specified time intervals. Stock data is fetched using the Yahoo Finance Python library and processed with Pandas.

3. **Investment Scenarios**: Run dollar-cost averaging simulations for daily, weekly, monthly, or lump sum investments. Users can analyze performance metrics based on historical data dating back up to 10 years.

4. **Latest News**: Retrieve the most recent Bitcoin-related news articles via the News API, providing users with insights and direct links for further reading.

## Technologies Used:

- **Backend**: Python with Flask framework
- **Frontend**: Bootstrap, HTML, CSS, JavaScript
- **Data Visualization**: Plotly for generating interactive charts
- **Data Processing**: Pandas for data manipulation and analysis
- **External APIs**: Yahoo Finance for stock data, News API for news articles

## Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/JGGHalfhide/BitcoinVS.git
   ```

2. Navigate to the project directory:
   ```bash
   cd BitcoinVS
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

## Usage:

1.	Access the live application through the URL BitcoinVS.onrender.com. Please note, render's free hosting tier disables the site when not accessed for 15 or more minutes. Therefore, if your request times out, please simply refresh the page and allow it to load. 
2.	Navigate through the various sections to explore Bitcoin price trends, stock comparisons, investment scenarios, and the latest news.
3.	Follow on-screen instructions and prompts to interact with different features and functionalities of the hosted application.

## Contributing:

Contributions are welcome! Please fork the repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss potential updates or modifications.

## License:

This project is licensed under the MIT License.
