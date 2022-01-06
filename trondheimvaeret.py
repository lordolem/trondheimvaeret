#!/usr/bin/python3

import tweepy
from yr.libyr import Yr
import datetime
from time import sleep
import tokens

# Authenticate to Twitter
auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
auth.set_access_token(tokens.access_token, tokens.access_token_secret)
api = tweepy.API(auth)

print("Program started")

def get_weather():
    weather = Yr(location_name='Norge/Trøndelag/Trondheim/Trondheim')
    data_dict = weather.dictionary
    data_now = weather.now()

    sunrise = data_dict["weatherdata"]["sun"]["@rise"].split("T")[1]
    sunset = data_dict["weatherdata"]["sun"]["@set"].split("T")[1]
    temp = data_now["temperature"]["@value"]
    precipitation = data_now["precipitation"]["@value"]
    wind_speed = data_now["windSpeed"]["@mps"]
    wind_dir = data_now["windDirection"]["@code"]
    
    return (sunrise, sunset, temp, precipitation, wind_speed, wind_dir)

def get_clock_emoji(time):
    if time == "06:00" or time == "18:00":
        return "🕕"
    elif time == "10:00":
        return "🕙"
    elif time == "14:00":
        return "🕑"
    elif time == "21:00":
        return "🕘"
    elif time == "00:00":
        return "🕛"
    else:
        return "-"

def pretty(time):
    sunrise, sunset, temp, precipitation, wind_speed, wind_dir = get_weather()
    output = []
    output.append(f"📍 Akkurat nå er det {temp}° i Trondheim!\n#TrondheimVaeret")
    output.append(f"💨 {wind_speed} m/s {wind_dir}")
    output.append(f"🌧 {precipitation} mm")
    if time == "06:00":
        output.append("------")
        output.append(f"🌅 {sunrise}")
        output.append(f"🌇 {sunset}")
    output.append("------")
    output.append(f"{get_clock_emoji(time)} Oppdatert: {time}")
    output.append("📖 Kilde: YR")

    return "\n".join(output)

while True:
    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
   
    print("Running: ", time)

    if time == "06:00" or time == "10:00" or time == "14:00" or time == "18:00" or time == "21:00" or time == "00:00":
        api.update_status(pretty(time))
        print("Tweet published")
        sleep(360)
    
    sleep(10)