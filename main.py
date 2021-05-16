import requests
from twilio.rest import Client

account_sid = 'YOUR_ID'
auth_token = 'YOUR_TOKEN'

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "YOUR_STOCK_API_KEY"
STOCK_URL = "https://www.alphavantage.co/query"

NEWS_API_KEY = "YOUR_NEWS_API_KEY"
NEWS_URL = "https://newsapi.org/v2/everything"

news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "5min",
    "apikey": STOCK_API_KEY,
}

news_response = requests.get(url=NEWS_URL, params=news_parameters)
news_article = news_response.json()["articles"]

titles = [news_article[i]['title'] for i in range(3)]
descriptions = [news_article[i]['description'] for i in range(3)]

response = requests.get(url=STOCK_URL, params=stock_parameters)
data = response.json()['Time Series (Daily)']

yesterday = list(response.json()['Time Series (Daily)'].keys())[0]
day_before_yesterday = list(response.json()['Time Series (Daily)'].keys())[1]
yesterday_close = data[yesterday]['4. close']
day_before_yesterday_close = data[day_before_yesterday]['4. close']

percentage = (float(yesterday_close) - float(day_before_yesterday_close))/float(yesterday_close) * 100


if percentage > 0 or percentage < 0:
    for i in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"TSLA: {'🔺' if percentage>0 else '🔻'}{round(abs(percentage))}%\nHeadline: {titles[i]}\nBrief: {descriptions[i]}",
            from_='Registered_number',
            to='Your_number'
        )
        print(message.status)
