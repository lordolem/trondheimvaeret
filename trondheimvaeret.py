#!/usr/bin/python3

import tweepy
from yr.libyr import Yr
import datetime
from time import sleep
import tokens

# Authenticate to Twitter
auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
auth.set_access_token(tokens.access_token, tokens.access_token_secret)

# Create API object
api = tweepy.API(auth)

print("Program started")

def get_weather(time):
    weather = Yr(location_name='Norge/Trøndelag/Trondheim/Trondheim')
    data = weather.dictionary

    city = data["weatherdata"]["location"]["name"]
    temp = data["weatherdata"]["forecast"]["tabular"]["time"][0]["temperature"]["@value"]
    
    if time == "21:00":
        extra = " God natt! "
    elif time == "08:00":
        extra = " God morgen! "
    else:
        extra = " "

    return f"#TrondheimVaeret Temperaturen i {city} er: {temp}°C. Kl {time}.{extra}Kilde: YR"

while True:
    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
   
    print("Running: ", time)

    if time == "08:00" or time == "12:00" or time == "16:00" or time == "18:00" or time == "21:00":
        api.update_status(get_weather(time))
        print("Tweet published")
        sleep(360)
    
    sleep(10)
