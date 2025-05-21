import csv
from datetime import datetime, timedelta
from enum import Enum
import json
import os
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import json
import re
import calendar


def get_game_data(game_box_score_url):




    response = requests.get(game_box_score_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    script_content = script.string
    data = json.loads(script_content)
    print(f'got data {game_box_score_url}')
    returnData= data['props']['pageProps']['postGameData']
    return returnData
    
def get_team(team_id):
    url = f'https://stats.wnba.com/team/{team_id}'
    print(url)
    response = requests.get(url)
    with open('team_page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', text=re.compile(r'window\.nbaStatsTeamInfo'))

    script_content = script_tag.string

    # Extract the JSON-like object using regex
    matches = re.findall(r'window\.(nbaStatsTeamInfo|nbaStatsTeamRanks|nbaStatsTeamSeasons)\s*=\s*({.*?});', script_content, re.DOTALL)
    if matches:
        return matches[0][1]
    return None
    
    
    return
    script = soup.find('script', id='__NEXT_DATA__')
    script_content = script.string
    data = json.loads(script_content)
    print(f'got data {url}')
    return data['props']['pageProps']['team']


def get_teams():
    url = 'https://www.wnba.com/teams/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    script_content = script.string
    data = json.loads(script_content)
    print(f'got data {url}')
    teams= data['props']['siteHeaderOptions']['teams']
    teams_data = []
    print(teams)
    for x in teams:
        team_data = get_team(x['tid'])
        
        print(team_data)
        if team_data:
            teams_data.append(json.loads(team_data))
    
    
    with open('wnba_teams_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for team in teams_data:
            writer.writerow([json.dumps(team)])

def get_games_until_date(schedule, param_date_str):
    param_date = datetime.strptime(param_date_str, "%Y-%m-%d")
    matching_games = []

    for game_day in schedule.get("leagueSchedule", {}).get("gameDates", []):
        for game in game_day.get("games", []):
            game_datetime_utc = datetime.strptime(game["gameDateTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
            if game_datetime_utc.date() == param_date.date():
                match = {}
                match['game_page_card_data'] = game
                match['id'] = game['gameId']
                match['dateTime'] = game['gameDateUTC']
                game_box_score_url = f"https://www.wnba.com/game/{game['gameId']}/{game['homeTeam']['teamTricode']}-vs-{game['homeTeam']['teamTricode']}/boxscore"
                match['box_score_page_data'] = get_game_data(game_box_score_url)
                matching_games.append(match)
            elif game_datetime_utc > param_date:
                # Stop collecting if the game's UTC datetime exceeds the param date
                return matching_games
    return matching_games


def get_historical_data(date):
    # date is in format 'YYYY-MM-DD'
    print(f'getting data for {date}')
    year, month, day = date.split('-')
    month_name = calendar.month_name[int(month)].lower()
    url = f'https://stats.wnba.com/stats/scheduleleaguev2?LeagueID=10&Season={year}&month={month_name}'

    headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wnba.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.wnba.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}



    response = requests.get(url, headers=headers).json()
    with open('wnba_historical_response.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=2)

    matches = get_games_until_date(response, date)
    
   
        #print(game['gameId'], game['gameUrlCode'], game['gameUrl'])
    with open(f'wnba_match_data_2025.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        #writer.writerow(['Game ID','Date','Box Score Link', 'Game Page Card data ','Box Score Page Data'])
        if file.tell() == 0:
            writer.writerow(['Game ID', 'DateTime', 'Game Page Card data', 'Box Score Page Data'])

        for match in matches:
            writer.writerow([match['id'], match['dateTime'], json.dumps(match['game_page_card_data']), json.dumps(match['box_score_page_data'])])           

# get_historical_data("2025-01-19")
    post_url = server_env.value['url'] + '/wnba-data/players/match-stats'
    try:
        with open(f'wnba_match_data_2025.csv', 'rb') as f:
            response = requests.post(post_url, files={'file': f})
        # print("Status Code:", response.status_code)
        # print("Response:", response.text)
        print("File successfully sent and deleted.")
    except Exception as e:
        print("An error occurred:", e)

def get_players():
    print('posting players')
    url = "https://www.wnba.com/players?team=all&position=all&show-historic-players=false"  # Replace with your actual endpoint
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find(id="__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    #script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script.string)

    # Now you can access the data like a regular Python dictionary
    # print(data['props']['pageProps']['players'])
    #data['props']['pageProps']['players']
    players_data = []
    for player in data['props']['pageProps']['allPlayersData']:
        
        # print(player['PLAYER_SLUG'])
        # print(player)
        # player_data = get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
        
        # player_data = player_data['props']['pageProps']['player']['info']

        player_data = {
            'PERSON_ID': player[0],
            'PLAYER_FIRST_NAME': player[2],
            'PLAYER_LAST_NAME': player[1],
            'PLAYER_SLUG': player[3],
            'TEAM_ID': player[4],
            'TEAM_NAME': player[7],
            'TEAM_SLUG': player[5],
            'TEAM_CITY': player[6],
            'TEAM_ABBREVIATION': player[8],
            'JERSEY_NUMBER': player[9],
            'POSITION': player[10],
            'HEIGHT': player[11],
            'WEIGHT': player[12],
            'COLLAGE': player[13],  # Keeping the incorrect key for consistency
            'SCHOOL': "",  # No equivalent value in the list, keeping as an empty string
            'COUNTRY': player[14],
            'IS_DEFUNCT': "",  # No equivalent value in the list, keeping as an empty string
        }
                
        players_data.append(player_data)
        

    with open('wnba_players_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for player in players_data:
            writer.writerow([json.dumps(player)])
    post_url = server_env.value['url']+'/wnba-data/players/dump'
    try:
        
        with open('wnba_players_data.csv', 'rb') as f:
            response = requests.post(post_url, files={'file': f})
            
        # Check the response
        print("Status Code:", response.status_code)
        os.remove('wnba_players_data.csv')
        print("File successfully sent and deleted.")
    except Exception as e:
        print("An error occurred:", e)

class ServerEnvironment(Enum):
  LOCAL = {"name": "local", "url": "http://127.0.0.1:3000"}
  TEST = {"name": "test", "url": "https://sportsdataapi.onrender.com"}
  PRODUCTION_TEST = {"name": "production_test", "url": "https://sportsdataapi-frankfurt-region.onrender.com"}
  PRODUCTION = {"name": "production", "url": "https://sportsdataapi-5l8y.onrender.com"}

global server_env
server_env = ServerEnvironment.PRODUCTION
today = datetime.now()
start_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
get_players()
get_historical_data(start_date)