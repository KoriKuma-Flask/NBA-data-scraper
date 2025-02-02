import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import csv
from datetime import datetime, timedelta
import os
# Configure Selenium

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service("/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/chromedriver-linux64/chromedriver")
#service = Service("C:\\Users\\sharj\\Documents\\Projects\\Data-Scraping\\NBA-stats\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)


# url = "https://www.nba.com/players"
# driver.get(url)
# Find the script tag with the id "__NEXT_DATA__"
# Open the webpage
def get_player_data(driver,id,slug_name):
    data = []

    try:
        url = f"https://www.nba.com/player/{id}/{slug_name}/profile"
        attempts = 0
        while attempts < 100:
            try:
                driver.get(url)
                break
            except Exception as e:
                if "ERR_INTERNET_DISCONNECTED" in str(e):
                    print(f"Internet disconnected while fetching data for player {slug_name}. Retrying in 0.5 seconds... (Attempt {attempts + 1}/100)")
                    time.sleep(0.5)
                    attempts += 1
                else:
                    raise e
        else:
            print(f"Failed to fetch data for player {slug_name} after 100 attempts due to internet disconnection.")

        script = driver.find_element(By.ID, "__NEXT_DATA__")
        
        script_content = script.get_attribute('innerHTML')

        # Parse the JSON content
        data = json.loads(script_content)
        return data

    except Exception as e:
        print(f"An error occurred while fetching data for player {slug_name}: {e}")

# Print results
    #return({'data':data,'PERSON_ID':id,'PLAYER_SLUG':slug_name})

    # print("Data:", data)



def get_match_data(driver,date):
    print(date)
    url = f"https://www.nba.com/games?date={date}"  # Replace with your actual endpoint
    #url = "https://www.nba.com/games?date=2025-01-19"  # Replace with your actual endpoint
    driver.get(url)
    script = driver.find_element(By.ID, "__NEXT_DATA__")
    
    script_content = script.get_attribute('innerHTML')

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
    print("have match data")
    for card in cards:
        try:
            match = {}
            match['game_page_card_data'] = card['cardData']
            match['id'] = card['cardData']['gameId']
            actions = card['cardData']['actions']
            for action in actions:
                if action['title'] == 'Box Score':
                    match['box_score_link'] = action['resourceLocator']['resourceUrl']
                    break
            # print(match)
            match['box_score_page_data'] = get_match_player_data(driver, "https://www.nba.com/" + match['box_score_link'])
            print("have player data")
            matches.append(match)
        except Exception as e:
            print(f"not data for {card['cardData']['gameId']}",)
            print(f"An error occurred while processing match data: {e}")
    with open(f'match_data{date}.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        #writer.writerow(['Game ID','Date','Box Score Link', 'Game Page Card data ','Box Score Page Data'])
        if file.tell() == 0:
            writer.writerow(['Game ID', 'Date', 'Box Score Link', 'Game Page Card data', 'Box Score Page Data'])

        for match in matches:
            writer.writerow([match['id'], date,match['box_score_link'], json.dumps(match['game_page_card_data']), json.dumps(match['box_score_page_data'])])
    print("successfully written")


def get_match_player_data(driver, url):
    driver.get(url)
    script = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script_content)
    return(data['props']['pageProps']['game'])
    


def get_players(driver):
    url = "https://www.nba.com/players"  # Replace with your actual endpoint
    driver.get(url)
    script = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script_content)

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
        
        print(player_data)
        
        players_data.append(player_data)
        
    
    with open('players_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for player in players_data:
            writer.writerow([json.dumps(player)])


 



def read_historical_data(file_path='historical.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
    except Exception as e:
        print(f"An error occurred while reading the file {file_path}: {e}")


    
 
def get_teams_data(driver):
    # Navigate to the website
    driver.get("https://www.nba.com/teams")  # Replace with the URL of the website

    # Wait for the page to load fully (optional, depending on website behavior)
    driver.implicitly_wait(10)

    # Locate all relevant divs
    team_divs = driver.find_elements(By.CLASS_NAME, "TeamFigure_tfContent__Vxiyh")

    # Iterate through divs and extract the specific href
    team_links = []
    for div in team_divs:
        try:
            # Locate the link with href starting with '/stats/team/'
            stats_link = div.find_element(By.CSS_SELECTOR, 'a[href^="/stats/team/"]')
    
            team_links.append(stats_link.get_attribute("href"))
        except Exception as e:
            print("Stats link not found in this div:", e)
    print("have team links")
    print(team_links)
    team_data_list = []
    for link in team_links:
        team_data = get_team_data(driver, link)
        team_data_list.append(team_data)
    print(team_data_list)
    with open('teams_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['DATA'])
        
        for team_data in team_data_list:
            writer.writerow([json.dumps(team_data)])
            
            
def get_team_data(driver,team_link):
    driver.get(team_link)
    script = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script_content)
    print("have team data")
    return data['props']['pageProps']['team']['info']
    
get_teams_data(driver)

#print(get_team_data(driver,"/stats/team/1610612746"))