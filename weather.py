#!/usr/bin/env python3

import requests
import datetime
import xml.etree.ElementTree as ET

yr_headers = {
    'User-Agent': '@trondheimvaeret github.com/omfj/trondheimvaeret',
}

# 63.4245, 10.4174
yr_params = (
    ('lat', '63.4245'),
    ('lon', '10.4174'),
    ('altitude', '10'),
)

xml_headers = {
    'User-Agent': '@trondheimvaeret github.com/omfj/trondheimvaeret',
}


response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/', headers=yr_headers, params=yr_params)
data = response.json()

correct_index = 0

base_path = data["properties"]["timeseries"][correct_index]["data"]
instant = base_path["instant"]["details"]
one_hour = base_path["next_1_hours"]["details"]


# Get the time for sunrise and sunset
def get_sunrise_sunset():
    # Format the date
    today = datetime.date.today()
    today_date = today.strftime("%Y-%m-%d")

    # Add the date to the params
    xml_params = (
        ('lat', '63.422'),
        ('lon', '10.412'),
        ('date', f'{today_date}'),
        ('offset', ' 01:00'),
    )

    # Get the data
    response = requests.get('https://api.met.no/weatherapi/sunrise/2.0', headers=xml_headers, params=xml_params)
    # Something make it readable https://docs.python.org/3/library/xml.etree.elementtree.html
    xml_tree = ET.fromstring(response.content)
    # Remove unwanted characters
    sunrise = xml_tree[1][0][5].attrib["time"].split("T")[1].split("+")[0]
    sunset = xml_tree[1][0][8].attrib["time"].split("T")[1].split("+")[0]

    return str(sunrise), str(sunset)


def get_wind_dir():
    deg = float(instant["wind_from_direction"])
    if 337.5 > deg <= 22.5:
        return "N"
    elif 22.5 < deg <= 67.5:
        return "NØ"
    elif 67.5 < deg <= 112.5:
        return "Ø"
    elif 112.5 < deg <= 157.5:
        return "SØ"
    elif 157.5 < deg <= 202.5:
        return "S"
    elif 202.5 < deg <= 247.5:
        return "SV"
    elif 247.5 < deg <= 292.5:
        return "V"
    elif 292.5 < deg <= 337.5:
        return "NV"
    else:
        return "404"

def get_temp():
    return str(instant["air_temperature"])

def get_precipitation():
    return str(one_hour["precipitation_amount"])

def get_wind_speed():
    return str(instant["wind_speed"])

def get_gust_speed():
    return str(instant["wind_speed_of_gust"])


wind_dir = get_wind_dir()
temp = get_temp()
precipitation = get_precipitation()
wind_speed = get_wind_speed()
gust_speed = get_gust_speed()