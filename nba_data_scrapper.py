import json
import os
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, timedelta, timezone



def get_match_player_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the script tag with the JSON data
    script = soup.find('script', id='__NEXT_DATA__')

    # Get the content of the script tag (which is typically JSON)
    script_content = script.string

    # Parse the JSON content
    data = json.loads(script_content)
    return data['props']['pageProps']['game']



def get_match_data(date):
    print(date)
    url = f"https://www.nba.com/games?date={date}"  # Replace with your actual endpoint
    #url = "https://www.nba.com/games?date=2025-01-19"  # Replace with your actual endpoint
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find(id="__NEXT_DATA__")
    script_content = script.string

    # Parse the JSON content
    data = json.loads(script_content)

    # Now you can access the data like a regular Python dictionary
    # print(data['props']['pageProps']['players'])
    if len(data['props']['pageProps']['gameCardFeed']['modules']) > 0:
        cards = data['props']['pageProps']['gameCardFeed']['modules'][0]['cards']
    else:
        print("No matchs data today")
        return
    matches = []
    print("have match cards data")
    for card in cards:
        try:
            match = {}
            match['game_page_card_data'] = card['cardData']
            match['id'] = card['cardData']['gameId']
            actions = card['cardData']['actions']
            for action in actions:
                if action['title'] == 'Box Score':
                    match['box_score_link'] = action['resourceLocator']['resourceUrl']
                    print(match['box_score_link'])
                    break
            # print(match)
            match['box_score_page_data'] = get_match_player_data("https://www.nba.com/" + match['box_score_link'])
            print("have match data")
            matches.append(match)
        except Exception as e:
            print(f"not data for {card['cardData']['gameId']}",)
            print(f"An error occurred while processing match data: {e}")
    with open(f'match_data{date}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        #writer.writerow(['Game ID','Date','Box Score Link', 'Game Page Card data ','Box Score Page Data'])
        if file.tell() == 0:
            writer.writerow(['Game ID', 'Date', 'Box Score Link', 'Game Page Card data', 'Box Score Page Data'])

        for match in matches:
            writer.writerow([match['id'], date,match['box_score_link'], json.dumps(match['game_page_card_data']), json.dumps(match['box_score_page_data'])])
    print("successfully written")
def get_players():
    url = "https://www.nba.com/players"  # Replace with your actual endpoint
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find(id="__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    #script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script.string)

    # Now you can access the data like a regular Python dictionary
    # print(data['props']['pageProps']['players'])
    data['props']['pageProps']['players']
    players_data = []
    for player in data['props']['pageProps']['players']:
        
        print(player['PLAYER_SLUG'])
        print(player)
        # player_data = get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
        
        # player_data = player_data['props']['pageProps']['player']['info']
        player_data = {
        'PERSON_ID': player['PERSON_ID'],
        'PLAYER_FIRST_NAME': player["PLAYER_FIRST_NAME"],
        'PLAYER_LAST_NAME': player["PLAYER_LAST_NAME"],
        'PLAYER_SLUG': player['PLAYER_SLUG'],
        'TEAM_ID': player.get("TEAM_ID", ''),
        'TEAM_NAME': player.get("TEAM_NAME", ''),
        'TEAM_SLUG': player.get("TEAM_SLUG", ''),
        'TEAM_CITY': player.get("TEAM_CITY", ''),
        'TEAM_ABBREVIATION': player.get("TEAM_ABBREVIATION", ''),
        'JERSEY_NUMBER': player.get("JERSEY_NUMBER", ''),
        'POSITION': player.get("POSITION", ''),
        'HEIGHT': player.get("HEIGHT", ''),
        'WEIGHT': player.get("WEIGHT", ''),
        'COLLAGE': player.get("COLLAGE", ''),#--------
        'SCHOOL': player.get("SCHOOL", ''),#--------
        'COUNTRY': player.get("COUNTRY", ''),
        'IS_DEFUNCT': player.get("IS_DEFUNCT", '') }
                
        players_data.append(player_data)
        

    with open('players_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for player in players_data:
            writer.writerow([json.dumps(player)])
    post_url = 'https://sportsdataapi-frankfurt-region.onrender.com/nba-data/players/dump'
    try:
        with open(f'players_data.csv', 'rb') as f:
            response = requests.post(post_url, files={'file': f})
            
        # Check the response
        print("Status Code:", response.status_code)
        

        os.remove(f'players_data.csv')
        print("File successfully sent and deleted.")
    except Exception as e:
        print("An error occurred:", e)
        
          
def get_day_match_data(yesterday_str =None):
    if yesterday_str is None:
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d") #"2025-01-29"
    print(yesterday_str)
    get_players()
    get_match_data( yesterday_str)
    # Close the driver
    post_url = 'https://sportsdataapi-frankfurt-region.onrender.com/nba-data/players/match-stats'
    try:
        if os.path.exists(f'match_data{yesterday_str}.csv'):
            with open(f'match_data{yesterday_str}.csv', 'rb') as f:
                response = requests.post(post_url, files={'file': f})
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            os.remove(f'match_data{yesterday_str}.csv')
            print("File successfully sent and deleted.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    get_day_match_data()
