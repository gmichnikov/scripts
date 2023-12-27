import sys
import os

# Append the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import requests
from credentials import SEATGEEK_CLIENT_ID
from tabulate import tabulate

def get_events(client_id):
    base_url = "https://api.seatgeek.com/2/events"
    params = {
        'client_id': client_id,
        'per_page': 5,
        # 'venue.name': 'Prudential Center',
        # 'venue.name': 'MetLife Stadium',
        # 'venue.name': 'Madison Square Garden',
        # 'venue.name': 'Barclays Center',
        # 'taxonomies.name': 'ncaa_basketball',
        'taxonomies.name': 'sports',
        # 'taxonomies.name': 'basketball',
        # 'taxonomies.name': 'concert',
        'geoip': '07928',
        # 'performers.slug': 'new-york-knicks'
        # 'venue.city': 'New York'
        # 'venue.state': 'AK',
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        events = response.json().get('events', [])
        print("200")
        return [(event['id'], event['type'], event['title'], event['datetime_local'], event['venue']['name'],event['venue']['display_location'], event['stats']['listing_count'], event['stats']['lowest_price'], event['stats']['highest_price'], event['stats']['median_price']) for event in events]
        # event['url']
    else:
        print("error")
        return f"Error: {response.status_code}"

events = get_events(SEATGEEK_CLIENT_ID)
for event in events:
    # print(event)
    pass

headerArray = ["ID", "Type", "Title", "Date", "Venue", "Location", "ListCount", "LowPrice", "HighPrice", "MedianPrice"]
# print(tabulate(events, headers=headerArray, tablefmt="grid"))
# print(tabulate(events, headers=headerArray, tablefmt="plain"))
print(tabulate(events, headers=headerArray, tablefmt="pipe"))
# print(tabulate(events, headers=headerArray, tablefmt="simple"))


# https://api.seatgeek.com/2/events?client_id=
# https://api.seatgeek.com/2/events?geoip=07928&client_id=
# https://api.seatgeek.com/2/events?geoip=07928&per_page=25&client_id=

# https://api.seatgeek.com/2/taxonomies?client_id=
# https://api.seatgeek.com/2/performers?taxonomies.name=nfl&per_page=50&client_id=
