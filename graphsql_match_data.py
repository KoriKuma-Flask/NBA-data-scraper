import requests
import json


# Authentication endpoint
AUTH_URL = "https://stake.com/auth"
GRAPHQL_URL = "https://example.com/graphql"



# Login payload (modify based on your API)
auth_payload = {
    "username": "John15963",
    "password": "fjWeGSzU8AKP*@G"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

url = 'https://stake.com/_api/graphql'
cookies = {
  "_hjSessionUser_5261158": "eyJpZCI6ImU1MzY0ZDhhLTU5ODgtNWRlZC1iNmQ4LTBmOTYxNDQzMzBjNSIsImNyZWF0ZWQiOjE3Mzg3MDU0OTA1MTcsImV4aXN0aW5nIjp0cnVlfQ",
  "currency_hideZeroBalances": "false",
  "currency_currencyView": "crypto",
  "fiat_number_format": "en",
  "locale": "en",
  "_ga": "GA1.1.1804084262.1738705586",
  "intercom-device-id-cx1ywgf2": "09b4530e-b2eb-45eb-aef7-864c1ea3b9cf",
  "cookie_consent": "true",
  "currency_currency": "btc",
  "leftSidebarView_v2": "minimized",
  "sidebarView": "hidden",
  "casinoSearch": "[\"Monopoly\",\"Crazy Time\",\"Sweet Bonanza\",\"Money Train\",\"Reactoonz\"]",
  "sportsSearch": "[\"Liverpool FC\",\"Kansas City Chiefs\",\"Los Angeles Lakers\",\"FC Barcelona\",\"FC Bayern Munich\"]",
  "oddsFormat": "decimal",
  "sportMarketGroupMap": "{}",
  "session": "dea806025f2607be9da929df30abcfb9fba3b376530d090ecd28414a125bc5507e4ad1dec649c112dddc30df4a6f9ee9",
  "session_info": "{\"id\":\"785cfb7c-2d9f-43d1-9c96-98de43ce09db\",\"sessionName\":\"Chrome (Unknown)\",\"ip\":\"45.250.255.9\",\"country\":\"JP\",\"city\":\"Shibuya\",\"active\":true,\"updatedAt\":\"Thu, 06 Feb 2025 15:17:22 GMT\"}",
  "_cfuvid": "EOrSF3yj4q6FFl_du9Esw58_8rkINp4PrfDz6FvUbwI-1738948882431-0.0.1.1-604800000",
  "__cf_bm": "bsxzrLILucobwV0g6KacMVdXXnCgXoBVQ9aVv_kC.FE-1739097770-1.0.1.1-Oz1oRLVvwnF1TX34DE13cz.QkFMEqX7vdLOogs20rGcukwLuopSaH3CzLSupKz8Jiwv8cXF.tgVc244mvPabNg",
  "cf_clearance": "JJTJbSSj.zwYtBwYqGmSGT5dnCzdbj7.XjA95IW1_pE-1739095574-1.2.1.1-1G59fySaJpU8VDF4XyshIcjWNUXyWZPTlRecqqZVI4cm3y2lk6vMYBXJlYH0eW7p5pA8bfBKWwHagtnunxPPGcpe3j8ixasTh3JeAHtvspYDGZWCLguuiSxl9kTw62daQvXdZ6jZJCj2a.oj_2cDBeat9GNt5_peinzioWHeuaRQa3kU0igr2ERqJGioqkBoZ9OAwmCK_ngWs2KW9_6Q6_xitOV3h7H1soenczIYQ3yJ1MRfR1WjBTDSTZHPfZRpqemTL8GQukjSsrH3mMQHZ5YgHXOkBBkrDYRehyIoD.P0M_trwxrrs5oTPjsqrOp2fzjq.cye9RwZLarvIAJ8yA",
  "_ga_TWGX3QNXGG": "GS1.1.1739095578.15.0.1739095578.0.0.0",
  "intercom-session-cx1ywgf2": "c3UyV0dWVzFMczNXc0tJRkoyY0h6T0NlSkJEN3Q4ZVN0YjIxT1VFU1hzMHh4RDRwSjltb1BUS1M1QmU5RlZua1dNMHlYcDczRFRQK2x4WFlqcndpQTRhUFhnNExHYjlEbERsOTZpcEhKdDg9LS05N1ZSVHRLUEFYNFh1dHZBTDFTZFhBPT0",
  "_hjSession_5261158": "eyJpZCI6IjQwNGY2MmNlLTAwODAtNGI3MS05Y2E0LWZjMGM2NDc5OWRiZCIsImMiOjE3MzkwOTU1Nzk2NDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0",
  "_dd_s": "rum"
}



def get_match_player_points(fixture,fixtureId):
    url = 'https://stake.com/_api/graphql'
    print(cookies)
    cookie_string = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'access-control-allow-origin': '*',
        'content-type': 'application/json',
        'cookie': cookie_string,
        'origin': 'https://stake.com',
        'priority': 'u=1, i',
        'referer': 'https://stake.com/sports/basketball/usa/nba/45025076-atlanta-hawks-houston-rockets',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"131.0.6778.204"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.204", "Chromium";v="131.0.6778.204", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"5.15.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-language': 'en'
    }
    # fixture = request.args.get('fixture')
    # fixtureId = request.args.get('fixtureId')
    # fixtureId = "00b190c8-f0b0-4011-8111-844e665821f0"
    # fixture = "45048537-charlotte-hornets-milwaukee-bucks"
    
    # fixture = "45048537-charlotte-hornets-milwaukee-bucks"
    # fixtureId = "00b190c8-f0b0-4011-8111-844e665821f0"
    data = {
        "query": """query SwishMarket_SlugFixture($fixture: String!, $atBat: Boolean! = false, $inPlay: Boolean!) {
          slugFixture(fixture: $fixture) {
            ...TeamMarket_SportFixture
            data {
              __typename
              ... on SportFixtureDataMatch {
                competitors {
                  extId
                }
              }
            }
            swishGame {
              id
              status
            }
            swishGameTeams {
              id
              name
              markets {
                trading {
                  betFactor
                }
                stat {
                  type
                }
                ...TeamMarket_SwishMarket
                ...SwishTemplateTotals_SwishMarket
                ...SwishTemplateWinner_SwishMarket
                ...SwishTemplateHandicap_SwishMarket
              }
              players {
                id
                ...TeamMarket_SwishCompetitor
                ...SwishMarketTeam_SwishCompetitor
                markets(inPlay: $inPlay) {
                  ...TeamMarket_SwishMarket
                  ...SwishTemplateTotals_SwishMarket
                  ...SwishTemplateWinner_SwishMarket
                  ...SwishTemplateHandicap_SwishMarket
                }
              }
            }
          }
        }
        fragment CustomSwishBetOutcome_SportFixture on SportFixture {
          id
          status
          tournament {
            slug
          }
          data {
            ... on SportFixtureDataMatch {
              competitors {
                name
                abbreviation
              }
              startTime
            }
            ... on SportFixtureDataOutright {
              name
              startTime
            }
          }
        }
        fragment SwishBetOutcome_SportFixture on SportFixture {
          id
          status
          tournament {
            slug
          }
          data {
            ... on SportFixtureDataMatch {
              competitors {
                name
                abbreviation
              }
              startTime
            }
            ... on SportFixtureDataOutright {
              name
              startTime
            }
          }
        }
        fragment CustomSwishBetOutcome_SwishMarket on SwishMarket {
          id
          stat {
            swishStatId
            name
            value
            customBet
            liveCustomBetAvailable
            type
          }
        }
        fragment SwishBetOutcome_SwishMarket on SwishMarket {
          id
          stat {
            swishStatId
            name
            value
          }
          data @include(if: $atBat) {
            atBat {
              marketDurationStart
            }
          }
        }
        fragment CustomSwishBetOutcome_SwishMarketOutcome on SwishMarketOutcome {
          id
          line
          over
          under
          suspended
          balanced
        }
        fragment SwishBetOutcome_SwishMarketOutcome on SwishMarketOutcome {
          id
          line
          over
          under
          suspended
          balanced
        }
        fragment TeamMarket_SwishMarket on SwishMarket {
          ...CustomSwishBetOutcome_SwishMarket
          ...SwishBetOutcome_SwishMarket
          stat {
            name
            value
          }
          lines {
            ...CustomSwishBetOutcome_SwishMarketOutcome
            ...SwishBetOutcome_SwishMarketOutcome
            id
            balanced
            over
            under
            line
          }
        }
        fragment CustomSwishBetOutcome_SwishCompetitor on SwishCompetitor {
          name
        }
        fragment SwishBetOutcome_SwishCompetitor on SwishCompetitor {
          name
        }
        fragment TeamMarket_SwishCompetitor on SwishCompetitor {
          ...CustomSwishBetOutcome_SwishCompetitor
          ...SwishBetOutcome_SwishCompetitor
        }
        fragment TeamMarket_SportFixture on SportFixture {
          ...CustomSwishBetOutcome_SportFixture
          ...SwishBetOutcome_SportFixture
          swishGame {
            status
          }
        }
        fragment SwishTemplateTotals_SwishMarket on SwishMarket {
          ...TeamMarket_SwishMarket
          competitor {
            name
          }
        }
        fragment SwishTemplateWinner_SwishMarket on SwishMarket {
          ...CustomSwishBetOutcome_SwishMarket
          lines {
            ...CustomSwishBetOutcome_SwishMarketOutcome
          }
          competitor {
            name
          }
        }
        fragment SwishTemplateHandicap_SwishMarket on SwishMarket {
          ...CustomSwishBetOutcome_SwishMarket
          lines {
            ...CustomSwishBetOutcome_SwishMarketOutcome
          }
          competitor {
            name
          }
        }
        fragment SwishMarketTeam_SwishCompetitor on SwishCompetitor {
          id
          name
          position
          ...TeamMarket_SwishCompetitor
          markets(inPlay: $inPlay) {
            ...TeamMarket_SwishMarket
            id
            trading {
              betFactor
            }
            stat {
              customBet
              liveCustomBetAvailable
            }
          }
        }""",
        "variables": {
            "fixture": fixture,
            "fixtureId": fixtureId,
            "provider": "betradar",
            "inPlay": False,
            "groups": ["teamAndMatchProps"]
        }
    }
    
    
    
    
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        headers = dict(response.headers)

        # cookie_dict = {}
        # for cookie in headers['Set-Cookie'].split(';'):
        #   keyValue= cookie.split('=')
        #   if len(keyValue)>1:
        #     cookie_dict[keyValue[0].strip()] = keyValue[1].strip()
        # print(cookie_dict)
        # cookies['cf_bm'] = cookie_dict['__cf_bm']

        response_data = {
            "headers": dict(response.headers),
            "body": response.json()
        }
        response = response.json()
        with open('/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/python_scripts/response_data.json', 'w') as f:
          json.dump(response_data, f, indent=4)
        with open('/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/python_scripts/match_player_points.json', 'w') as f:
            json.dump(response, f, indent=4)
        return response


    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch match player points data: {e}")
        print(response.text)
        return {}

print(get_match_player_points("45048537-charlotte-hornets-milwaukee-bucks","00b190c8-f0b0-4011-8111-844e665821f0"))
# print("\n\n\n")
# get_match_player_points("45048537-charlotte-hornets-milwaukee-bucks","00b190c8-f0b0-4011-8111-844e665821f0")

# refresh_cookies()


#!/usr/bin/env python3

# import requests

# username = "ACCOUNTNAME-zone-custom-region-jp-session-fVFkXUzNH-sessTime-5"
# password = "PASSWORD"
# PROXY_DNS = "xx.xx.xx.xx:9999"



# #https://ACCOUNTNAME-zone-custom-region-jp-session-djq3zrEo7-sessTime-5:PASSWORD@xx.xx.xx.xx:2334


# urlToGet = "http://google..com/"
# proxy = {"http":"http://{}:{}@{}".format(username, password, PROXY_DNS)}
# proxy = {"http":"https://asdfjkl-zone-custom-region-jp-session-djq3zrEo7-sessTime-5:PASSWORD@xx.xx.xx.xx:2334"}
# try:
#     r = requests.get(urlToGet, proxies=proxy, timeout=10)
#     r.raise_for_status()  # Raise an error for bad status codes
#     print("Response: {}".format(r.text))
# except requests.exceptions.RequestException as e:
#     print("Error: {}".format(e))