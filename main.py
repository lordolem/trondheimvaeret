#!/usr/bin/env python3

import datetime
import weather

# ↓ Remove when testing ↓

import tokens
import tweepy
from time import sleep

# Authenticate to Twitter
auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
auth.set_access_token(tokens.access_token, tokens.access_token_secret)
api = tweepy.API(auth)

# ↑ Remove when testing ↑

# Find the best clock emoji for the current time
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

# Make the tweet pretty
def make_tweet(time):
    output = []
    temp = weather.get_temp();
    emoji = weather.get_emoji();
    wind_speed = weather.get_wind_speed();
    gust_speed = weather.get_gust_speed();
    wind_dir = weather.get_wind_dir();
    precipitation_min, precipitation_max, precipitation = weather.get_precipitation();
    
    output.append(f"📍 Akkurat nå er det {temp}°C {emoji} i Trondheim!")
    output.append(f"💨 {wind_speed}({gust_speed}) m/s 🧭 {wind_dir}")
    
    if precipitation > 0.0:
        output.append(f"🌧 {precipitation_min} - {precipitation_max} mm")

    output.append(f"{get_clock_emoji(time)} Oppdatert: {time}")
    output.append("📖 Kilde: YR")

    return "\n".join(output)

publish_times = ["06:00", "10:00", "14:00", "18:00", "21:00", "00:00"]

if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M")

        print(f"Running... {now}")

        if time in publish_times:
            tweet = make_tweet(time)
            api.update_status(tweet)
            print(tweet)
            sleep(360)

        sleep(10)