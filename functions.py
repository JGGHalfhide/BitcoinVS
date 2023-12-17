import csv


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

