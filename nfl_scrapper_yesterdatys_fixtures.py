import re
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone, date, timedelta
from enum import Enum
from nfl_scrapper_players import update_nfl_players

class ServerEnvironment(Enum):
  LOCAL = {"name": "local", "url": "http://127.0.0.1:3000"}
  TEST = {"name": "test", "url": "https://sportsdataapi.onrender.com"}
  PRODUCTION_TEST = {"name": "production_test", "url": "https://sportsdataapi-frankfurt-region.onrender.com"}
  PRODUCTION = {"name": "production", "url": "https://sportsdataapi-5l8y.onrender.com"}

# NFL season configuration
seasons = [
    {"seasonType": "1", "name": "pre", "start": date(2025, 7, 31), "weeks": 4},
    {"seasonType": "2", "name": "main", "start": date(2025, 9, 4), "weeks": 18},
    {"seasonType": "3", "name": "post", "start": date(2026, 1, 8), "weeks": 5},
]

year = "2025"
my_dict =[ {
    "seasonType": "1",
    "range": 5,
    "name": "pre"
},{
    "seasonType": "2",
    "range": 19,
    "name": "main"
},{
    "seasonType": "3",
    "range": 6,
    "name": "post"
}]

def get_yesterdays_data(date_data, server_env=ServerEnvironment.PRODUCTION):
    global file_flag
    week = date_data['week']
    season_type = date_data['seasonType']
    year = datetime.now().year
    url = f"https://www.espn.in/nfl/schedule/_/week/{week}/year/{year}/seasontype/{season_type}"
    headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        }
    cookies = {
            'edition': 'espn-en-gb',
            'country': 'gb',
            'region': 'unknown',
            '_dcf': '1',
            'SWID': '6552B2F4-DB9C-47B0-C7D2-71608C3C75CF',
            # Add other cookies as needed
        }
    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()  # Raise an error for bad status codes
    html_content = response.text
        # Write the HTML content to a file
    if file_flag:
        with open(f"files/week_{week}_page.html", "w", encoding="utf-8") as file:
            file.write(html_content)
            # Load HTML

    soup = BeautifulSoup(html_content, "html.parser")

        # Find the script containing window['__espnfitt__']
    script_tag = soup.find("script", string=re.compile(r"window\['__espnfitt__'\]"))
    if not script_tag:
        raise ValueError(f"Could not find script with window['__espnfitt__'] for week {week}")

    script_content = script_tag.string

        # Extract the JSON-like object
    match = re.search(r"window\['__espnfitt__'\]\s*=\s*({.*});", script_content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not extract __espnfitt__ JSON for week {week}")

    json_text = match.group(1)

        # ESPN often uses valid JSON here, so first try normal parsing
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"[WARNING] JSON decode failed for week {week}, cleaning text...")
            # If ESPN used single quotes or other JS-isms, clean them
        cleaned = json_text
        cleaned = cleaned.replace("'", '"')  # replace single with double quotes
        cleaned = re.sub(r",\s*}", "}", cleaned)  # remove trailing commas before }
        cleaned = re.sub(r",\s*]", "]", cleaned)  # remove trailing commas before ]
        cleaned = cleaned.replace("undefined", "null")
        data = json.loads(cleaned)

        # Save to JSON file
    if file_flag:
        with open(f"files/week_{week}_espnfitt.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"[INFO] Extracted JSON keys for week {week}:", list(data.keys())[:20])
        # Loop over the dictionary where each key is a date and value is a list of events
    final_data = []
    for date, events in data['page']['content']['events'].items():
        print(f"[INFO] Processing date: {date} for week {week}")
        if date != date_data['date_key']:
            print(f"[INFO] Skipping date: {date}, not matching target date: {date_data['date_key']}")
            continue
        final_data ={date: events}
        for event in events:
                # Call the API for each event
            event_id = event['id']  
            api_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={event_id}"
            response = requests.get(api_url)
            if response.status_code == 200:
                event_data = response.json()
                print(f"[INFO] Successfully fetched data for event: {event_id} in week {week}")
                    # Optionally save the event data to a file
                event['boxscore_api_data'] = event_data['boxscore']
            else:
                print(f"[ERROR] Failed to fetch data for event: {event_id} in week {week}, Status Code: {response.status_code}")
            '/mlb-data/players/match-stats'
        # Save the final data to a JSON file
        break       

    if file_flag:
        with open(f"files/{year}_seasonType{season_type}_week_{week}_final_data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
    # Send the final data to the specified API
    api_url = server_env.value['url'] + "/nfl-data/players/match-stats"
    try:
        response = requests.post(api_url, json=final_data)
        if response.status_code == 200:
            print(f"[INFO] Successfully sent data to API for week {week}")
        else:
            print(f"[ERROR] Failed to send data to API for week {week}, Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"[ERROR] Exception occurred while sending data to API for week {week}: {e}")


    print(f"[INFO] Final data for week {week} has been saved to nfl_espn/{year}_seasonType{season_type}_week_{week}_final_data.json")

# Function to determine current season and week
def get_nfl_week(current_date):
    for season in seasons:
        start = season["start"]
        total_days = (season["weeks"] * 7) - 1  # inclusive end
        end = start + timedelta(days=total_days)

        if start <= current_date <= end:
            # Find week number
            days_passed = (current_date - start).days
            week = (days_passed // 7) + 1
            return {
                "seasonType": season["seasonType"],
                "seasonName": season["name"],
                "week": week,
                "weekStart": start + timedelta(weeks=week - 1),
                "weekEnd": start + timedelta(weeks=week) - timedelta(days=1),
            }
    return None  # Not within any season

# Example: Test with today's date
today = (datetime.now(timezone.utc).date() - timedelta(days=1))
print("Today's date:", today)
result = get_nfl_week(today)
result['date'] = today
result['date_key'] = today.strftime("%Y%m%d")

global file_flag
file_flag = False 
# Call the function regardless of the flag
update_nfl_players(server_env=ServerEnvironment.PRODUCTION,file_flag=file_flag)
get_yesterdays_data(result)

if not file_flag:
    print("[INFO] File saving is disabled. Files will not be saved.")