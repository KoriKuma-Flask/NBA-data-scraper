from enum import Enum
import re
import json
from bs4 import BeautifulSoup
import requests

class ServerEnvironment(Enum):
  LOCAL = {"name": "local", "url": "http://127.0.0.1:3000"}
  TEST = {"name": "test", "url": "https://sportsdataapi.onrender.com"}
  PRODUCTION_TEST = {"name": "production_test", "url": "https://sportsdataapi-frankfurt-region.onrender.com"}
  PRODUCTION = {"name": "production", "url": "https://sportsdataapi-5l8y.onrender.com"}

def update_nfl_players(server_env=ServerEnvironment.PRODUCTION,file_flag=False):
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
    teams = [
        'https://www.espn.in/nfl/team/roster/_/name/buf/buffalo-bills',
        'https://www.espn.in/nfl/team/roster/_/name/mia/miami-dolphins',
        'https://www.espn.in/nfl/team/roster/_/name/ne/new-england-patriots',
        'https://www.espn.in/nfl/team/roster/_/name/nyj/new-york-jets',
        'https://www.espn.in/nfl/team/roster/_/name/cin/cincinnati-bengals',
        'https://www.espn.in/nfl/team/roster/_/name/cle/cleveland-browns',
        'https://www.espn.in/nfl/team/roster/_/name/pit/pittsburgh-steelers',
        'https://www.espn.in/nfl/team/roster/_/name/bal/baltimore-ravens',
        'https://www.espn.in/nfl/team/roster/_/name/ind/indianapolis-colts',
        'https://www.espn.in/nfl/team/roster/_/name/ten/tennessee-titans',
        'https://www.espn.in/nfl/team/roster/_/name/jax/jacksonville-jaguars',
        'https://www.espn.in/nfl/team/roster/_/name/hou/houston-texans',
        'https://www.espn.in/nfl/team/roster/_/name/kc/kansas-city-chiefs',
        'https://www.espn.in/nfl/team/roster/_/name/lv/las-vegas-raiders',
        'https://www.espn.in/nfl/team/roster/_/name/lac/los-angeles-chargers',
        'https://www.espn.in/nfl/team/roster/_/name/den/denver-broncos',
        'https://www.espn.in/nfl/team/roster/_/name/dal/dallas-cowboys',
        'https://www.espn.in/nfl/team/roster/_/name/phi/philadelphia-eagles',
        'https://www.espn.in/nfl/team/roster/_/name/nyg/new-york-giants',
        'https://www.espn.in/nfl/team/roster/_/name/wsh/washington-commanders',
        'https://www.espn.in/nfl/team/roster/_/name/min/minnesota-vikings',
        'https://www.espn.in/nfl/team/roster/_/name/gb/green-bay-packers',
        'https://www.espn.in/nfl/team/roster/_/name/det/detroit-lions',
        'https://www.espn.in/nfl/team/roster/_/name/chi/chicago-bears',
        'https://www.espn.in/nfl/team/roster/_/name/tb/tampa-bay-buccaneers',
        'https://www.espn.in/nfl/team/roster/_/name/no/new-orleans-saints',
        'https://www.espn.in/nfl/team/roster/_/name/car/carolina-panthers',
        'https://www.espn.in/nfl/team/roster/_/name/atl/atlanta-falcons',
        'https://www.espn.in/nfl/team/roster/_/name/sf/san-francisco-49ers',
        'https://www.espn.in/nfl/team/roster/_/name/sea/seattle-seahawks',
        'https://www.espn.in/nfl/team/roster/_/name/lar/los-angeles-rams',
        'https://www.espn.in/nfl/team/roster/_/name/ari/arizona-cardinals'
    ]
    #teams = [ 'https://www.espn.in/nfl/team/roster/_/name/ari/arizona-cardinals']
    players = []
    for team in teams:
        url = team
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

        soup = BeautifulSoup(html_content, "html.parser")

        # Find the script containing window['__espnfitt__']
        script_tag = soup.find("script", string=re.compile(r"window\['__espnfitt__'\]"))
        if not script_tag:
            raise ValueError(f"Could not find script with window['__espnfitt__']")

        script_content = script_tag.string

        # Extract the JSON-like object
        match = re.search(r"window\['__espnfitt__'\]\s*=\s*({.*});", script_content, re.DOTALL)
        if not match:
            raise ValueError(f"Could not extract __espnfitt__ JSON")

        json_text = match.group(1)

        # ESPN often uses valid JSON here, so first try normal parsing
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"[WARNING] JSON decode failed for week, cleaning text...")
        # If ESPN used single quotes or other JS-isms, clean them
            cleaned = json_text
            cleaned = cleaned.replace("'", '"')  # replace single with double quotes
            cleaned = re.sub(r",\s*}", "}", cleaned)  # remove trailing commas before }
            cleaned = re.sub(r",\s*]", "]", cleaned)  # remove trailing commas before ]
            cleaned = cleaned.replace("undefined", "null")
            data = json.loads(cleaned)

        final_data = {"team":data['page']['content']['roster']['team'],'players':data['page']['content']['roster']['groups']}
        players.append(final_data)

        print(f"[INFO] Final data for team {team.split('/')[-1]} has been saved {team.split('/')[-1]}")
    if file_flag:
        with open("files/players/nfl_players.json", "w") as outfile:
            json.dump({"players": players}, outfile, indent=4)

    post_url =  server_env.value['url'] + '/nfl-data/players/dump'
    try:
        response = requests.post(post_url, json={"players": players})

        response.raise_for_status()  # Raise an error for bad status codes
        print(f"[INFO] Successfully sent NFL players data to {post_url}")
    except Exception as e:
        print(f"[ERROR] Exception occurred while sending NFL players data: {e}")
