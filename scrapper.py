import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import csv
from datetime import datetime, timedelta
# Configure Selenium

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

#ervice = Service("/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/chromedriver-linux64/chromedriver")
service = Service("C:\\Users\\sharj\\Documents\\Projects\\Data-Scraping\\NBA-stats\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)


# url = "https://www.nba.com/players"
# driver.get(url)
# Find the script tag with the id "__NEXT_DATA__"
# Open the webpage
def get_player_data(driver,id,slug_name):
    data = []

    try:
        url = f"https://www.nba.com/player/{id}/{slug_name}/profile"
        driver.get(url)

        table = driver.find_element(By.CSS_SELECTOR, "section.Block_block__62M07 table")

        headers = [header.text for header in table.find_elements(By.CSS_SELECTOR, "thead th")]

        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        data = []
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            data.append([cell.text for cell in cells])
    except Exception as e:
        print(f"An error occurred while fetching data for player {slug_name}: {e}")

# Print results
    print(f"headers: {headers}")
    return({slug_name:data})
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
    with open(f'match_data{date[:7]}.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        #writer.writerow(['Game ID','Date','Box Score Link', 'Game Page Card data ','Box Score Page Data'])
        if file.tell() == 0:
            writer.writerow(['Game ID', 'Date', 'Box Score Link', 'Game Page Card data', 'Box Score Page Data'])

        for match in matches:
            writer.writerow([match['id'], date,match['box_score_link'], match['game_page_card_data'], match['box_score_page_data']])
    print("successfully written")


    # post_url = 'https://thankfully-brief-cat.ngrok-free.app/nba-data/players/match-stats'
    # headers = {
    #     "Content-Type": "application/json"
    # }
    
    # body = {"data": json.dumps(matches)}
    # post_response = requests.post(post_url, headers=headers, json=body)
    # if post_response.status_code == 200:
    #     print("Data posted successfully")
    # else:
    #     print(f"Failed to post data: {post_response.status_code}")
    #print(data['props']['pageProps']['gameCardFeed']['modules'][0]['cards'][0]['cardData']['actions'].keys())
    # for player in data['props']['pageProps']['players']:
    #     print(player['PLAYER_SLUG'])
    #     get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
    #     headers = {
    #         "Content-Type": "application/json"
    #     }
        
    #     player_data = get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
    #     print(player_data)
# get_player_data(driver, 1628378, "donovan-mitchell")


def get_match_player_data(driver, url):
    driver.get(url)
    script = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script_content)

    # Now you can access the data like a regular Python dictionary
    # print(data['props']['pageProps']['players'])
    #url = "http://example.com/api/players"  # Replace with your actual endpoint
    # data['props']['pageProps']['players']
    return(data['props']['pageProps']['game'])
    
    # for player in data['props']['pageProps']['players']:
    #     print(player['PLAYER_SLUG'])
    #     get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
    #     headers = {
    #         "Content-Type": "application/json"
    #     }
        
    #     player_data = get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
    #     print(player_data)
    

def get_players(driver):
    script = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script_content)

    # Now you can access the data like a regular Python dictionary
    # print(data['props']['pageProps']['players'])
    url = "http://example.com/api/players"  # Replace with your actual endpoint
    data['props']['pageProps']['players']
    for player in data['props']['pageProps']['players']:
        print(player['PLAYER_SLUG'])
        get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
        headers = {
            "Content-Type": "application/json"
        }
        
        player_data = get_player_data(driver, player['PERSON_ID'], player['PLAYER_SLUG'])
        print(player_data)

# get_match_players_data(driver, "https://www.nba.com/game/det-vs-hou-0022400600/box-score")
#start_date = datetime(2024, 10, 22)2025-01-11
start_date = datetime(2025, 1, 11)
end_date = datetime.today()

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    get_match_data(driver, date_str)
    current_date += timedelta(days=1)
    if current_date.day == 1:
        time.sleep(5)

# # # Close the driver


# response = requests.get('https://thankfully-brief-cat.ngrok-free.app/nba/players/stats/20002712?season=2024')
