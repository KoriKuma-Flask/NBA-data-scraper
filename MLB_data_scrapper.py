import requests
import json
from datetime import datetime, timedelta
import threading
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
    url = "https://statsapi.mlb.com/api/v1/schedule"
    params = {
        "sportId": "1,51,21",
        "startDate": start_date,
        "endDate": end_date,
        "timeZone": "America/New_York",
        "gameType": "E,S,R,F,D,L,W,A",
        "language": "en",
        "leagueId": "104,103,160,590,426,427,428,429,430,431,432",
        "sortBy": "gameDate,gameType",
        "hydrate": "team,linescore(matchup,runners),xrefId,flags,statusFlags,broadcasts(all),venue(location),decisions,person,probablePitcher,stats,game(content(media(epg),summary),tickets),seriesStatus(useOverride=true)"
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
        print(f"Failed to fetch schedule. Status code: {response.status_code}")
        return None




def fetch_live_game_feed(game_id):
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




response = fetch_live_game_feed("715882")  # Example game ID, replace with actual game ID
if response:
    with open("live_game_feed.json", "w") as file:
        json.dump(response, file, indent=4)
    print("Response saved to live_game_feed.json")











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
        print
        def process_player(player, players_data):
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
                players_data.append(player_data)

        threads = []
        players_data = []

        for player in response["people"]:
            thread = threading.Thread(target=process_player, args=(player, players_data))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        with open("players_detailed_data.json", "w") as file:
            json.dump(players_data, file, indent=4)
        print("Detailed player data saved to players_detailed_data.json")


def get_match_data():
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    response = fetch_schedule(start_date, end_date)
    if response and "dates" in response:
        matches_data = []
        for date_info in response["dates"]:
            for game in date_info.get("games", []):
                game_id = game.get("gamePk")
                if game_id:
                    live_game_data = fetch_live_game_feed(game_id)
                    if live_game_data:
                        game["liveGameData"] = live_game_data
                matches_data.append(game)
        with open("matches_data.json", "w") as file:
            json.dump(matches_data, file, indent=4)
        print("Match data saved to matches_data.json")


players()
get_match_data()














def fetch_team_roster():
    url = "https://www.espn.in/mlb/team/roster/_/name/chw/chicago-white-sox"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.espn.in/mlb/teams",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    cookies = {
        "SWID": "45509DD4-0E73-4311-C3B9-28D6E1E612D9",
        "country": "pk",
        "edition-view": "espn-en-in",
        "edition": "espn-en-in",
        "region": "unknown",
        "_dcf": "1",
        "s_ensCDS": "0",
        "cookieMonster": "1",
        "userZip": "54020",
        "connectionspeed": "full",
        "_nr": "0",
        "hashedIp": "cab0b0b19fa7f31f8f70f94e2b1bc62e9342b620289509cb1dbc1c4c49677524",
        "block.check": "false|false",
        "client_type": "html5",
        "client_version": "4.7.1",
        "_cb": "URH8DBkzc_ZIOVuH",
        "AMCVS_EE0201AC512D2BE80A490D4C@AdobeOrg": "1",
        "AMCV_EE0201AC512D2BE80A490D4C@AdobeOrg": "-50417514|MCMID|71362407027313147730123162865817177841|MCAAMLH-1746267994|3|MCAAMB-1746267994|6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y|MCOPTOUT-1745670394s|NONE|MCAID|NONE|vVersion|5.5.0",
        "s_cc": "true",
        "espn-prev-page": "espnin:mlb:team:roster:home",
        "s_sq": "[[B]]",
        "__gads": "ID=aba4af9a5cac1582:T=1745663190:RT=1745666613:S=ALNI_MaSImWn4XstAeGeM_f5xRot0RgdoQ",
        "__gpi": "UID=00001098dbd61be5:T=1745663190:RT=1745666613:S=ALNI_MZegHrPl242QyBD3-RidIkdjtW_RQ",
        "__eoi": "ID=efb3162f66aa05f6:T=1745663190:RT=1745666613:S=AA-AfjZUhjW9Z_rW2pikRdzCj27-",
        "_cb_svref": "https://www.espn.in/mlb/teams",
        "_chartbeat2": ".1745663194086.1745666701405.1.BF8BpdgLwIsuUKyfvB9c9DT2Mal.3",
        "nol_fpid": "cv0rq9uxvyvuyqalxxfgd1ufjrmx31745663194|1745663194444|1745666701490|1745666701618",
        "_chartbeat4": "t=CTQV_obsOJyhq_6-DZLgQoB7b0Kh&E=7&x=0&c=0.8&y=3127&w=911",
        "s_ensNR": "1745666750092-Repeat"
    }

    response = requests.get(url, headers=headers)
    with open("team_roster.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    





















def fetch_team_data():
    url = "https://www.espn.in/mlb/teams"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.espn.in/mlb/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    cookies = {
        "SWID": "45509DD4-0E73-4311-C3B9-28D6E1E612D9",
        "country": "pk",
        "edition-view": "espn-en-in",
        "edition": "espn-en-in",
        "region": "unknown",
        "_dcf": "1",
        "s_ensCDS": "0",
        "cookieMonster": "1",
        "userZip": "54020",
        "connectionspeed": "full",
        "_nr": "0",
        "hashedIp": "cab0b0b19fa7f31f8f70f94e2b1bc62e9342b620289509cb1dbc1c4c49677524",
        "block.check": "false|false",
        "client_type": "html5",
        "client_version": "4.7.1",
        "_cb": "URH8DBkzc_ZIOVuH",
        "AMCVS_EE0201AC512D2BE80A490D4C@AdobeOrg": "1",
        "AMCV_EE0201AC512D2BE80A490D4C@AdobeOrg": "-50417514|MCMID|71362407027313147730123162865817177841|MCAAMLH-1746267994|3|MCAAMB-1746267994|6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y|MCOPTOUT-1745670394s|NONE|MCAID|NONE|vVersion|5.5.0",
        "s_cc": "true",
        "espn-prev-page": "espnin:mlb:schedule",
        "__gads": "ID=aba4af9a5cac1582:T=1745663190:RT=1745664332:S=ALNI_MaSImWn4XstAeGeM_f5xRot0RgdoQ",
        "__gpi": "UID=00001098dbd61be5:T=1745663190:RT=1745664332:S=ALNI_MZegHrPl242QyBD3-RidIkdjtW_RQ",
        "__eoi": "ID=efb3162f66aa05f6:T=1745663190:RT=1745664332:S=AA-AfjZUhjW9Z_rW2pikRdzCj27-",
        "s_ensNR": "1745664343047-New",
        "_chartbeat2": ".1745663194086.1745664347759.1.DXxSeqaai6lX6Ge2I9GygCsT1Z.11",
        "_chartbeat5": "",
        "s_sq": "[[B]]",
        "nol_fpid": "cv0rq9uxvyvuyqalxxfgd1ufjrmx31745663194|1745663194444|1745664347889|1745664348037"
    }

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

