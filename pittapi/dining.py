"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import requests
import json
from datetime import datetime
from typing import Any

REQUEST_HEADERS = {"User-Agent": "Chrome/103.0.5026.0"}

LOCATIONS = {
    "ETHEL'S",
    "THE EATERY",
    "PANERA BREAD",
    "TRUE BURGER",
    "THE PERCH",
    "FORBES STREET MARKET",
    "BUNSEN BREWER",
    "WICKED PIE",
    "SMOKELAND BBQ AT THE PETERSEN EVENTS CENTER",
    "THE MARKET AT TOWERS",
    "THE DELICATESSEN",
    "CAMPUS COFFEE & TEA CO - TOWERS",
    "PA TACO CO.",
    "FT. PITT SUBS",
    "CREATE",
    "POM & HONEY",
    "THE ROOST",
    "CATHEDRAL SUSHI",
    "BURRITO BOWL",
    "CHICK-FIL-A",
    "SHAKE SMART",
    "STEEL CITY KITCHEN",
    "SMOKELAND BBQ FOOD TRUCK",
    "CAMPUS COFFEE & TEA CO - SUTHERLAND",
    "THE MARKET AT SUTHERLAND",
    "PLATE TO PLATE AT SUTHERLAND MARKET",
    "EINSTEIN BROS. BAGELS - POSVAR",
    "EINSTEIN BROS. BAGELS - BENEDUM",
    "BOTTOM LINE BISTRO",
    "CAFE VICTORIA",
    "CAFE 1787",
    "CAMPUS COFFEE & TEA CO - PUBLIC HEALTH",
    "RXPRESSO",
    "SIDEBAR CAFE",
    "CAFE 1923",
}


def get_locations() -> dict[str, Any]:
    """Gets data about all dining locations"""

    url = "https://api.dineoncampus.com/v1/locations/status?site_id=5e6fcc641ca48e0cacd93b04&platform="

    resp = requests.get(
        url,
        headers=REQUEST_HEADERS,
    )

    locations = json.loads(resp.content)["locations"]

    dining_locations = {location["name"].upper(): location for location in locations}

    return dining_locations


def get_location_hours(location_name: str, date: datetime) -> dict[str, Any]:
    """Returns dictionary containing Opening and Closing times of locations open on date.
    -Ex:{'The Eatery': [{'start_hour': 7, 'start_minutes': 0, 'end_hour': 0, 'end_minutes': 0}]}
    - if location_name is None, returns times for all locations
    - date must be in YYYY,MM,DD format, will return data on current day if None
    """

    if location_name != None and location_name.upper() not in LOCATIONS:
        raise ValueError("Invalid Dining Location")

    if date == None:
        date = datetime.now()

    date_str = date.strftime("%Y-%m-%d")

    url = f"https://api.dineoncampus.com/v1/locations/weekly_schedule?site_id=5e6fcc641ca48e0cacd93b04&date=%22{date_str}%22"

    resp = requests.get(url, headers=REQUEST_HEADERS)

    if resp.status_code == 502:
        raise ValueError("Invalid Date")

    locations = json.loads(resp.content)["the_locations"]

    hours = {}

    if location_name == None:
        for location in locations:
            for day in location["week"]:
                if day["date"] == date_str:
                    hours[location["name"]] = day["hours"]
    else:
        for location in locations:
            if location["name"].upper() == location_name.upper():
                for day in location["week"]:
                    if day["date"] == date_str:
                        hours[location["name"]] = day["hours"]
                break

    return hours


def get_location_menu(location: str, date: datetime, period_name: str):
    """Returns menu data for given dining location on given day/period
    -period_name used for locations with different serving periods(i.e. 'Breakfast','Lunch','Dinner','Late Night')
        - None -> Returns menu for first(or only) period at location"""

    if location.upper() not in LOCATIONS:
        raise ValueError("Invalid Dining Location")

    if date == None:
        date = datetime.today()

    date_str = date.strftime("%y-%m-%d")

    location_id = get_locations()[location.upper()]["id"]

    periods_url = f"https://api.dineoncampus.com/v1/location/{location_id}/periods?platform=0&date={date_str}"

    periods_resp = requests.get(periods_url, headers=REQUEST_HEADERS)

    if periods_resp.status_code == 502:
        raise ValueError("Invalid Date")

    periods = json.loads(periods_resp.content)["periods"]

    if period_name == None or len(periods) == 1:
        period_id = periods[0]["id"]
    else:
        for period in periods:
            if period["name"].lower() == period_name.lower():
                period_id = period["id"]

    menu_url = f"https://api.dineoncampus.com/v1/location/{location_id}/periods/{period_id}?platform=0&date={date_str}"

    menu_resp = requests.get(menu_url, headers=REQUEST_HEADERS)

    menu = json.loads(menu_resp.content)["menu"]

    return menu
