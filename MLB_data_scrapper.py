import json
import os
import requests
import threading
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from enum import Enum
import csv
import time
import random

class ServerEnvironment(Enum):
  LOCAL = {"name": "local", "url": "http://127.0.0.1:3000"}
  TEST = {"name": "test", "url": "https://sportsdataapi.onrender.com"}
  PRODUCTION_TEST = {"name": "production_test", "url": "https://sportsdataapi-frankfurt-region.onrender.com"}
  PRODUCTION = {"name": "production", "url": "https://sportsdataapi-5l8y.onrender.com"}


def path(file_name):
    return os.path.join(output_dir, file_name)

def fetch_player_data(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
    params = {
        "hydrate": "currentTeam,team,stats(group=[pitching],type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats],team(league),leagueListId=mlb_hist)",
        "site": "en"
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.mlb.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mlb.com/player/andrew-abbott-671096",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    # Generate a random IP address
    random_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    headers["X-Forwarded-For"] = random_ip  # Add the random IP to the headers

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    


def fetch_all_players(season):
    url = f"https://statsapi.mlb.com/api/v1/sports/1/players"
    params = {
        "fields": "people,fullName,lastName,nameSlug",
        "season": season
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.mlb.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mlb.com/players",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch players. Status code: {response.status_code}")
        return None





def fetch_schedule(start_date, end_date):
    print("Fetching schedule data...")
    print(f"Start date: {start_date}, End date: {end_date}")
    url = "https://statsapi.mlb.com/api/v1/schedule"
    params = {
        "sportId": "1,51,21",
        "startDate": start_date,
        "endDate": end_date,
        # "timeZone": "America/New_York",
        # "gameType": "E,S,R,F,D,L,W,A",
        # "language": "en",
        # "leagueId": "104,103,160,590,426,427,428,429,430,431,432",
        # "sortBy": "gameDate,gameType",
        # "hydrate": "team,linescore(matchup,runners),xrefId,flags,statusFlags,broadcasts(all),venue(location),decisions,person,probablePitcher,stats,game(content(media(epg),summary),tickets),seriesStatus(useOverride=true)"
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.mlb.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mlb.com/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("Schedule data fetched successfully.")
        return response.json()
    else:
        print(f"Failed to fetch schedule. Status code: {response.status_code}")
        return None




def fetch_live_game_feed(game_id):
    print(f"Game ID: {game_id}")
    url = f"https://ws.statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
    params = {
        "language": "en"
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.mlb.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mlb.com/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch live game feed. Status code: {response.status_code}")
        return None




# response = fetch_live_game_feed("715882")  # Example game ID, replace with actual game ID
# if response:
#     with open("live_game_feed.json", "w") as file:
#         json.dump(response, file, indent=4)
#     print("Response saved to live_game_feed.json")











def players():
    current_year = datetime.now().year
    current_month = datetime.now().month

    # MLB season typically starts in April and ends in October
    if current_month >= 4:
        season = current_year
    else:
        season = current_year - 1
    response = fetch_all_players(season)
    if response and "people" in response:
        players_data = []
        
        def process_player(player, players_data):
            time.sleep(random.uniform(0, 4))
            print(f"Processing player: {player.get('fullName', 'Unknown')}")
            player_id = None
            name_slug = player.get("nameSlug")
            if name_slug:
                player_id = name_slug.split("-")[-1]
            if player_id:
                print(f"Fetching data for player ID: {player_id}")
                player_data = fetch_player_data(player_id)
            if player_data:
                print(f"Fetched data for player ID: {player_id}")
                players_data.append(player_data['people'][0])

        threads = []
        players_data = []

        for player in response["people"]:
            thread = threading.Thread(target=process_player, args=(player, players_data))
            threads.append(thread)
            thread.start()

            # Wait for threads to complete after every 100 threads
            if len(threads) % 100 == 0:
                print("Waiting for threads to complete...")
                time.sleep(random.uniform(3, 8))
                for thread in threads:
                    thread.join()
                threads = []

        for thread in threads:
            thread.join()


    with open(path('mlb_players_data.csv'), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for data in players_data:
            output = {
            "source_player_id": data.get("id"),
            "first_name": data.get("firstName"),
            "last_name": data.get("lastName"),
            "full_name": data.get("fullName"),
            "player_slug": data.get("nameSlug"),
            "source_team_id": data.get("currentTeam", {}).get("id"),
            "team_name": data.get("currentTeam", {}).get("name"),
            "team_slug": data.get("currentTeam", {}).get("fileCode"),
            "team_city": data.get("currentTeam", {}).get("locationName"),
            "team_abbreviation": data.get("currentTeam", {}).get("abbreviation"),
            "jersey_number": data.get("primaryNumber"),
            "position": data.get("primaryPosition", {}).get("abbreviation"),
            "position_name": data.get("primaryPosition", {}).get("name"),
            "position_code": data.get("primaryPosition", {}).get("code"),
            "height": data.get("height"),
            "weight": data.get("weight"),
            "college": None,  # Not present in data
            "country": data.get("birthCountry"),
            "date_of_birth": data.get("birthDate"),
            "active":  data.get("active")
            }
            writer.writerow([json.dumps(output)])
    post_url =  server_env.value['url'] + '/mlb-data/players/dump'
    try:
        with open(path('mlb_players_data.csv'), 'rb') as f:
            response = requests.post(post_url, files={'file': f})
            
        # Check the response
        print("Status Code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        #os.remove(path('mlb_players_data.csv'))
        print("File successfully sent and deleted.")


        with open(path("players_detailed_data.json"), "w") as file:
            json.dump(players_data, file, indent=4)
        print("Detailed player data saved to players_detailed_data.json")

def get_match_data(start_date=None, end_date=None):
    print("Fetching match data...")
    response = fetch_schedule(start_date, end_date)
    with open(path('mlb_schedule_response.json'), 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=4, default=str)
    if response and "dates" in response:
        matches_data = []
        for date_info in response["dates"]:
            for game in date_info.get("games", []):
                game_id = game.get("gamePk")
                if game_id:
                    live_game_data = fetch_live_game_feed(game_id)
                    if live_game_data:
                        boxscore = live_game_data['liveData']['boxscore']
                        for key,team in boxscore['teams'].items():
                            team['players'] = {
                               key: {
                                    "person": {
                                        "id": player['person']['id'],
                                    },
                                    "position": {
                                        "abbreviation": player['position']['abbreviation'],
                                    },
                                    "stats": player['stats'],
                                    "gameStatus":player['gameStatus'],
                                    
                                }
                                for key, player in team['players'].items()
                            }

                current_match_data = {
                    'id': game_id,
                    'startTimeUTC': datetime.fromisoformat(game['gameDate']).astimezone(timezone.utc),
                    'game_page_card_data': game,
                    'box_score_page_data': boxscore
                }
                matches_data.append((current_match_data['id'], current_match_data['startTimeUTC'], json.dumps(current_match_data['box_score_page_data'])))
        file_name = f"mlb_match_data_{start_date}_to_{end_date}.csv"
        with open(path(file_name), mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write headers
            if file.tell() == 0:
                writer.writerow(['Game ID', 'Date Time', 'Box Score Page Data'])

            for match in matches_data:
                writer.writerow(match)
    
        print("Match data saved to matches_data.json")


        post_url = server_env.value['url'] + '/mlb-data/players/match-stats'
        try:
            if os.path.exists(path(file_name)):
                with open(path(file_name), 'rb') as f:
                    response = requests.post(post_url, files={'file': f})
                print("Status Code:", response.status_code)
                print("Response:", response.text)
                os.remove(f'mlb_match_data_{start_date}_to_{end_date}.csv')
                print("File successfully sent and deleted.")
        except Exception as e:
            print("An error occurred:", e)


def fetch_team_data():
    response = requests.get("https://www.mlb.com/team")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the script tag with the JSON data
    script = soup.find('script', id='__NEXT_DATA__')

    # Get the content of the script tag (which is typically JSON)
    script_content = script.string

    # Parse the JSON content
    data = json.loads(script_content)
    with open(path("mlb_team_data.json"), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    with open(path('mlb_team_data.csv'), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        for player in data['props']['pageProps']['initialState']['page']['statsapiData']['teams']:
            writer.writerow([json.dumps(player)])
    print("Team data saved to team_data.json")
    return data['props']['pageProps']['game']


def main():
    today = datetime.now()
    start_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    get_match_data(start_date, start_date)
    # start_date = "2025-03-18" 
    # start_date = "2025-04-17"
    # end_date = "2025-05-15" 
    players()
    # Call get_match_data for each 10-day interval between start_date and end_date
    # current_start = datetime.strptime(start_date, "%Y-%m-%d")
    # final_end = datetime.strptime(end_date, "%Y-%m-%d")
    # while current_start < final_end:
    #     current_end = min(current_start + timedelta(days=9), final_end)
    #     print(f"Fetching match data from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}")
    #     get_match_data(current_start.strftime("%Y-%m-%d"), current_end.strftime("%Y-%m-%d"))
    #     current_start = current_end + timedelta(days=1)
    #fetch_team_data()
    
if __name__ == "__main__":
    global server_env
    server_env = ServerEnvironment.PRODUCTION
    output_dir = os.path.join(os.path.dirname(__file__), 'mlb_files')
    os.makedirs(output_dir, exist_ok=True)
    main()







