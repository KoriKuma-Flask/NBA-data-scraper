import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv
from datetime import datetime, timedelta, timezone
import os



def get_match_player_data(driver, url):
    driver.get(url)
    script = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the content of the script tag (which is typically JSON)
    script_content = script.get_attribute('innerHTML')

    # Parse the JSON content
    data = json.loads(script_content)
    return(data['props']['pageProps']['game'])



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
                    break
            # print(match)
            match['box_score_page_data'] = get_match_player_data(driver, "https://www.nba.com/" + match['box_score_link'])
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


def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = Service("/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/chromedriver-linux64/chromedriver")
    #service = Service("C:\\Users\\sharj\\Documents\\Projects\\Data-Scraping\\NBA-stats\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    yesterday_str = "2025-01-28" #yesterday.strftime("%Y-%m-%d")
    print(yesterday_str)
    get_match_data(driver, yesterday_str)
    # Close the driver
    
    print(yesterday_str)
    post_url = 'https://sportsdataapi.onrender.com/nba-data/players/match-stats'
    try:
        with open(f'match_data{yesterday_str}.csv', 'rb') as f:
            response = requests.post(post_url, files={'file': f})
            
        # Check the response
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        
        if response.status_code == 200:
            os.remove(f'match_data{yesterday_str}.csv')
            print("File successfully sent and deleted.")
    except Exception as e:
        print("An error occurred:", e)

    driver.quit()

if __name__ == "__main__":
    main()
