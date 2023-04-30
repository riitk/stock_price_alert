import requests
import smtplib

##Email constants
MY_EMAIL = "ritiksuniljain@gmail.com"
PASSWORD = "fjiqjihbqojanzbq"
RECEVIVER_EMAIL = "ritikjain7350@gmail.com"


## STOCK CONSTANTS
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "IM7KP9WKXM2EW5YH"
AVA_ENDPOINT = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    # "interval": "60min",
    "apikey": STOCK_API_KEY,
}

## NEWS CONSTANTS
NEWS_API_KEY = "f2afce7041774fbf9744e84c8415b567"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_params = {
    "q": COMPANY_NAME,
    "sortBy": "top",
    "language": "en",
    "apiKey": NEWS_API_KEY,
}


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_response = requests.get(AVA_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
yesterday_price = float(stock_data["Time Series (Daily)"][list(stock_data["Time Series (Daily)"].keys())[0]]['4. close'])
before_yesterday_price = float(stock_data["Time Series (Daily)"][list(stock_data["Time Series (Daily)"].keys())[1]]['4. close'])
difference = abs(before_yesterday_price-yesterday_price)



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if before_yesterday_price*0.05 <= difference:
    percentage_change = int((difference * 100) / before_yesterday_price)
    if before_yesterday_price - yesterday_price > 0:
        stock_symbol = f"UP {percentage_change}%"
    else:
        stock_symbol = f"DOWN {percentage_change}%"
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()['articles']
    # headlines coleection

    news_headline1 = articles[0]['title']
    news_brief1 = articles[0]['description']
    news_headline2 = articles[1]['title']
    news_brief2 = articles[1]['description']
    news_headline3 = articles[2]['title']
    news_brief3 = articles[2]['description']


    with smtplib.SMTP("smtp.gmail.com") as connection:
        msg = f"Subject: Stock Price Alert\n\n{STOCK} {stock_symbol}\n\nHeadline: {news_headline1}\nBrief: {news_brief1}\n\nHeadline: {news_headline2}\nBrief: {news_brief2}\n\nHeadline: {news_headline3}\nBrief: {news_brief3}"
        encoded_msg = msg.encode('utf-8')
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=RECEVIVER_EMAIL,
                            msg= encoded_msg)
        connection.close()
