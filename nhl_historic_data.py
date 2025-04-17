from enum import Enum
import json
import os
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, timedelta, timezone

class ServerEnvironment(Enum):
  LOCAL = {"name": "local", "url": "http://127.0.0.1:3000"}
  TEST = {"name": "test", "url": "https://sportsdataapi.onrender.com"}
  PRODUCTION = {"name": "production", "url": "https://sportsdataapi-frankfurt-region.onrender.com"}


def path(file_name):
    return os.path.join(output_dir, file_name)

def get_match_player_data(matchId):
    url = f'https://api-web.nhle.com/v1/gamecenter/{matchId}/boxscore'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.nhl.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.nhl.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url)
    match_player_data = response.json()
    return match_player_data
    
    
    

def get_matchs_data(from_date,to_date):
    from_date_str = from_date
    current_from_date_str = from_date
    to_date_str = to_date
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    #Tue, Oct 10, 2023 – Mon, Jun 24, 2024
    print(from_date)
    match_data = [] 
    time_to_break = False
    while from_date < to_date:
        url = f'https://api-web.nhle.com/v1/schedule/{current_from_date_str}'
        print(url)
        #url = f'https://api-web.nhle.com/v1/schedule-calendar/{current_from_date_str}'
        if time_to_break:
            break
        response = requests.get(url)
        matches_data = response.json()
        


        #print(matches_data)
        for games in matches_data['gameWeek']:
            print("gameWeek")
            #print(games['name']['default'])
            # print(games['games'][0])
            if time_to_break:
                break

            for match_day in games['games']:
                print(match_day['id'])
                match_start_time = datetime.strptime(match_day['startTimeUTC'], '%Y-%m-%dT%H:%M:%SZ')
                
                # print(match_start_time)
                # print(to_date_dt)
                
                if match_start_time > to_date:
                    time_to_break = True
                    print(match_start_time > to_date)
                    break
                
                current_match_data = {
                    'id': match_day['id'],
                    'startTimeUTC': match_day['startTimeUTC'],
                    'game_page_card_data': match_day,
                    'box_score_page_data': get_match_player_data(match_day['id'])
                }
                match_data.append((current_match_data['id'], current_match_data['startTimeUTC'], json.dumps(current_match_data['game_page_card_data']), json.dumps(current_match_data['box_score_page_data'])))
            #from_date = from_date + timedelta(days=7)
            #print(match_data)
            current_from_date_str = matches_data.get('nextStartDate')
            if current_from_date_str is None:
                time_to_break = True
                break
            from_date = datetime.strptime(current_from_date_str, '%Y-%m-%d')
        
    with open(path(f'nhl_match_data_{from_date_str}_to_{to_date_str}.csv'), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        if file.tell() == 0:
            writer.writerow(['Game ID', 'Date Time', 'Game Page Card data', 'Box Score Page Data'])

        for match in match_data:
            writer.writerow(match)

    # Send the file to the server
    post_url = server_env.value['url'] + '/nhl-data/players/match-stats'
    try:
        with open(path(f'nhl_match_data_{from_date_str}_to_{to_date_str}.csv'), 'rb') as f:
            response = requests.post(post_url, files={'file': f})
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("An error occurred while sending the file:", e)
    finally:
        os.remove(path(f'nhl_match_data_{from_date_str}_to_{to_date_str}.csv'))
        print("File successfully sent and deleted.")

        
    # with open(path()'nhl_matches_data.csv'), mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     # Write headers
    #     writer.writerow(['DATA'])
        
    #     for match in matches_data:
    #         writer.writerow([json.dumps(match)])

def get_teams(from_date,to_date):
    url = 'https://api-web.nhle.com/v1/schedule-calendar/2025-03-06'
    response = requests.get(url)
    teams_data = response.json()
    #print(teams_data)

    from_date_str = from_date
    current_from_date_str = from_date
    to_date_str = to_date
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    #Tue, Oct 10, 2023 – Mon, Jun 24, 2024
    print(from_date)
    match_data = [] 
    already_teams_entered = []
    while from_date < to_date:
        url = f'https://api-web.nhle.com/v1/schedule-calendar/{current_from_date_str}'

        response = requests.get(url)
        
        matches_data = response.json()
        print(matches_data)

        time_to_break = False
        #print(matches_data)
        for games in matches_data['teams']:
            print("gameWeek")
            print(games['name']['default'])
            # print(games['games'][0])
            if time_to_break:
                break


            for match_day in range(1):
                break
                print(match_day['id'])
                match_start_time = datetime.strptime(match_day['startTimeUTC'], '%Y-%m-%dT%H:%M:%SZ')
                
                # print(match_start_time)
                # print(to_date_dt)
                
                if match_start_time > to_date:
                    time_to_break = True
                    print(match_start_time > to_date)
                    break
                
                current_match_data = {
                    'id': match_day['id'],
                    'startTimeUTC': match_day['startTimeUTC'],
                    'game_page_card_data': match_day,
                    'box_score_page_data': get_match_player_data(match_day['id'])
                }
            if games['id'] not in already_teams_entered:
                match_data.append(games)
                already_teams_entered.append(games['id'])
            #from_date = from_date + timedelta(days=7)
            current_from_date_str = matches_data['nextStartDate']
            from_date = datetime.strptime(current_from_date_str, '%Y-%m-%d')
        
    with open(path(f'nhl_teams_{from_date_str}_to_{to_date_str}.csv'), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        #writer.writerow(['Game ID','Date','Box Score Link', 'Game Page Card data ','Box Score Page Data'])
        if file.tell() == 0:
            writer.writerow(['DATA'])
            #writer.writerow(['Game ID', 'Date Time' 'Game Page Card data', 'Box Score Page Data'])

        for match in match_data:
            writer.writerow([json.dumps(match)])
    # with open(path()'nhl_matches_data.csv'), mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     # Write headers
    #     writer.writerow(['DATA'])
        
    #     for match in matches_data:
    #         writer.writerow([json.dumps(match)])
    # with open('nhl_teams_data.csv', mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     # Write headers
    #     writer.writerow(['DATA'])
        
    #     for team in teams_data:
    #         writer.writerow([json.dumps(team)])

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
        print("No match's data today")
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
    
    url = 'https://search.d3.nhle.com/api/v1/search/player?culture=en-us&limit=10000&q=%2A&active=true'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.nhl.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.nhl.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    players_data = response.json()

    with open(path('nhl_players_data.csv'), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for player in players_data:
            writer.writerow([json.dumps(player)])
    post_url =  server_env.value['url'] + '/nhl-data/players/dump'
    try:
        with open(path('nhl_players_data.csv'), 'rb') as f:
            response = requests.post(post_url, files={'file': f})
            
        # Check the response
        print("Status Code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        os.remove(path('nhl_players_data.csv'))
        print("File successfully sent and deleted.")
        
          
def get_day_match_data(yesterday_str =None):
    if yesterday_str is None:
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d") #"2025-01-29"
    print(yesterday_str)
    get_players()
    get_match_data( yesterday_str)
    # Close the driver
    post_url = server_env.value['url'] + '/nhl-data/players/match-stats'
    try:
        if os.path.exists(f'match_data{yesterday_str}.csv'):
            with open(f'match_data{yesterday_str}.csv', 'rb') as f:
                response = requests.post(post_url, files={'file': f})
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            #os.remove(f'match_data{yesterday_str}.csv')
            print("File successfully sent and deleted.")
    except Exception as e:
        print("An error occurred:", e)

header = True

def main():
    get_players()
    #get_teams('2023-10-10', '2024-06-24')
    #get_matchs_data('2024-10-04', '2024-10-14')
    #get_matchs_data('2025-04-04', '2025-04-12')
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    
    yesterday_str = yesterday.strftime("%Y-%m-%d") #"2025-01-29"
    get_matchs_data(yesterday_str, datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    return
    url = f'https://api-web.nhle.com/v1/schedule/2025-03-07'
    response = requests.get(url).json()
    print(response['nextStartDate'])
    print(response['previousStartDate']) 
    
if __name__ == "__main__":
    global server_env

    server_env = ServerEnvironment.PRODUCTION
    output_dir = os.path.join(os.path.dirname(__file__), 'nhl_files')
    os.makedirs(output_dir, exist_ok=True)
    main()
    # start_date = datetime(2025, 1, 1)
    # end_date = datetime(2025, 1, 2)
    # current_date = start_date

    # while current_date <= end_date:
    #     date_str = current_date.strftime("%Y-%m-%d")
    #     get_day_match_data(date_str)
    #     current_date += timedelta(days=1)
    # Ensure the directory exists
