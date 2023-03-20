STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY = "KH7ZIQ5J3YE7AM09"
NEWS_API_KEY = "b38498e4ff7e445bb6e0cc4bd9157ad5"
TWILLIO_SID = "AC673c559dd5a1868e1e832019a80c73ac"
TWILLIO_AUTH_TOKEN = "bc8e0a9453be5b6d0d5d738e7067738e"

import requests
import datetime as dt
from twilio.rest import Client

stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": ALPHA_API_KEY,
}

account_sid = TWILLIO_SID
auth_token = TWILLIO_AUTH_TOKEN

client = Client(account_sid, auth_token)



## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

response_stock = requests.get("https://www.alphavantage.co/query", params=stock_params)
hourly_price = response_stock.json()["Time Series (60min)"]



today = dt.datetime.now()
est_time = today - dt.timedelta(hours=14)

news_params = {
    "q": "Tesla",
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY,
}

response_news = requests.get("https://newsapi.org/v2/everything", params=news_params)
response_news.raise_for_status()

print(response_news.json())

# tesla_news_titles = [response_news.json()["articles"][n]["title"] for n in range(3) ]
# tesla_news_contents = [response_news.json()["articles"][n]["description"] for n in range(3) ]

# zip_news = zip(tesla_news_titles, tesla_news_contents)

def tesla_news_title(number):
    tesla_news_titles = [response_news.json()["articles"][n]["title"] for n in range(3)]
    return  tesla_news_titles[number]

def tesla_news_contents(number):
    tesla_news_contents = [response_news.json()["articles"][n]["description"] for n in range(3)]
    return  tesla_news_contents[number]

# tesla_news = [{"Headline": key, "Brief": value} for (key, value) in zip_news]



def target_price_data(day):
    target_time = ""
    day_subtraction = est_time.day - day
    try:
        target_time = dt.datetime(year=est_time.year, month=est_time.month, day=day_subtraction, hour=20)
    except:
        if est_time.month == 3:
            day_subtraction += 28
            target_time = dt.datetime(year=est_time.year, month=2, day=day_subtraction, hour=20)
        else:
            day_subtraction += 30
            target_time = dt.datetime(year=est_time.year, month=est_time.month-1, day=day_subtraction, hour=20)

    else:
        return float(hourly_price[str(target_time)]["4. close"])

    finally:

        try:
            return float(hourly_price[str(target_time)]["4. close"])
        except KeyError:
            print(target_time.weekday())
            return 0


def calc_fluctuation():
    if target_price_data(1) == 0:
        return 999
    else:
        if int(target_price_data(2)) > int(target_price_data(1)):
            return int(abs(((target_price_data(1) - target_price_data(2)) / target_price_data(1)) * 100))
        else:
            return int(abs(((target_price_data(1) - target_price_data(2)) / target_price_data(1)) * 100))

def get_news():
    if calc_fluctuation() == 999:
        print("It was weekend. Market did not open")
    elif calc_fluctuation() > 5:
        if calc_fluctuation() > 0:
            print(f"TSLA: 🔺{calc_fluctuation()}%")
            print(f"Headline = {tesla_news_title(0)}")
            print(f"Brief = {tesla_news_contents(0)}")
        else:
            print(f"TSLA: 🔻{calc_fluctuation()}%")
            print(f"Headline = {tesla_news_title(0)}")
            print(f"Brief = {tesla_news_contents(0)}")
    else:
        if calc_fluctuation() > 0:
            message = client.messages \
                .create(
                body=f"TSLA: +{calc_fluctuation()}%\nHeadline = {tesla_news_title(0)}\nBrief = {tesla_news_contents(0)}",
                from_='+15673716735',
                to='+821094395262'
            )
            print(message.sid)
        else:
            message = client.messages \
                .create(
                body=f"TSLA: -{calc_fluctuation()}%\nHeadline = {tesla_news_title(0)}\nBrief = {tesla_news_contents(0)}",
                from_='+15673716735',
                to='+821094395262'
            )
            print(message.sid)

        # print("It's normal price action")

get_news()




## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this:




"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

