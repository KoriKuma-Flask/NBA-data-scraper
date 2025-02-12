import datetime
import json
import requests
from seleniumbase import SB 
import time


global_cookies = {"_hjSessionUser_5261158":"eyJpZCI6ImU1MzY0ZDhhLTU5ODgtNWRlZC1iNmQ4LTBmOTYxNDQzMzBjNSIsImNyZWF0ZWQiOjE3Mzg3MDU0OTA1MTcsImV4aXN0aW5nIjp0cnVlfQ","currency_currency":"btc","currency_hideZeroBalances":"false","currency_currencyView":"crypto","fiat_number_format":"en","cookie_consent":"false","leftSidebarView_v2":"minimized","sidebarView":"hidden","casinoSearch":"[\\\"Monopoly\\\",\\\"Crazy Time\\\",\\\"Sweet Bonanza\\\",\\\"Money Train\\\",\\\"Reactoonz\\\"]","sportsSearch":"[\\\"Liverpool FC\\\",\\\"Kansas City Chiefs\\\",\\\"Los Angeles Lakers\\\",\\\"FC Barcelona\\\",\\\"FC Bayern Munich\\\"]","oddsFormat":"decimal","sportMarketGroupMap":"{}","locale":"en","_ga":"GA1.1.1804084262.1738705586","intercom-device-id-cx1ywgf2":"09b4530e-b2eb-45eb-aef7-864c1ea3b9cf","session":"f4cb7b48fcc88ddaaee2c71207d2523298aef182a2ca984bfb956b7a0c05e761d0082675751d717e56b2ffcd78436760","session_info":"{\\\"id\\\":\\\"01fbde82-6690-43b5-a71b-b83810ae8483\\\",\\\"sessionName\\\":\\\"Chrome (Unknown)\\\",\\\"ip\\\":\\\"188.166.207.96\\\",\\\"country\\\":\\\"SG\\\",\\\"city\\\":\\\"Singapore (Pioneer)\\\",\\\"active\\\":true,\\\"updatedAt\\\":\\\"Tue, 04 Feb 2025 21:46:36 GMT\\\"}","fullscreen_preference":"false","_cfuvid":"LpUFtmZOhJlFCnEsspX87howpmYoKWc4plglxPEpSZU-1738750508064-0.0.1.1-604800000","cf_clearance":"27QSwGqbc_CJlbtCjzGmECnJHDALtdj1zN6PlIj3ZBk-1738750509-1.2.1.1-ZdZchmTKP6jPmsT58m9Jj.9lk3JTgG4AeVbq5jB1th9.fb9m5rsSZGRgrOn5WmOHTEaxQ1FjjxCgk7W0VFrfdGeAuqHGv1fkRPwJrS4.1p._DYeizDPEyTLHUZaIO8NgZFsxIERcuw7f49ocacP.kc3W0V1atgdMbWRnE.YudcYKBR240c7WHvrB9YMd1PIQOAF8shZjaKJ9nU0Q6Uxg7zLa3THzj4._n7sjZ0LXvKAApsJEwMpq13.2b8IoL95hU8Oj7G0SVyaSyJXq_tnyKCXXE_rL9PMw5YG2oJInsQsd3rMVzo6oW2T7wOkSHw7x22jA0XalJ4aF50I0wKn4kg","_ga_TWGX3QNXGG":"GS1.1.1738750409.2.1.1738750789.0.0.0","intercom-session-cx1ywgf2":"OVJyVzJ5TmlIaEhpMS90R1ZiYjkvcGlQZkxFcmJ6NlEwTzJhVjAvWlVlejMwcEdrTk9mL0tpYlIzdVQ4RHJwYlZ2UWtsSFhWVmZ1T2ZEeUZGUVhWM0V3ZU9tbDdGNzd6OHhKWDJaZi9Jbkk9LS11ZG5vVERPTmNWT1A3c3BSOERxMCtRPT0","__cf_bm":"3sS_9b1AshM9134ZVoxydrofXBbj8VZgrJZtxND8UWQ-1738753843-1.0.1.1-fLb456PyDKWoPzdEclVcLEO7Z9qpmhIwg3wnxnELk_X3adtFFMQ74u_JQuDVGKyF97sRTJw9nKWq36uucDioNA","_dd_s":"rum"}
def getNewCookies():
  #url = "https://2captcha.com/demo/cloudflare-turnstile-challenge"
  url = "https://stake.com/"

  with  SB(uc=True, xvfb=True, headless=False)  as sb:
      
      #get_match_player_points("45048537-charlotte-hornets-milwaukee-bucks","00b190c8-f0b0-4011-8111-844e665821f0"))
      
      sb.uc_open_with_reconnect(url, 4)
      sb.uc_gui_click_captcha()  # Click the CAPTCHA
      
      # Get page details
      page_title = sb.get_title()
      print("Page Title:", page_title)
      
      # Use driver.current_url to get the current URL
      current_url = sb.driver.current_url
      print("Current URL:", current_url)
      
      page_source = sb.get_page_source()
      print("Page Source:", page_source[:200])  # Print first 200 characters to avoid long output
      
      # Get page cookies
      cookies = sb.driver.get_cookies()
      print("Cookies:", cookies)
      timestamp = cookies[0]['expiry']

      # Convert the timestamp to UTC time
      utc_time = datetime.datetime.utcfromtimestamp(timestamp)

      # Get the current UTC time
      current_utc_time = datetime.datetime.utcnow()
      print(current_utc_time)
      print(utc_time)
      print("are new cookies valid?:")
      print(utc_time > current_utc_time)
      global_cookies.update({cookie['name']: cookie['value'] for cookie in cookies})
      print(cookies)
      #iframe_src = sb.get_attribute('iframe[title="Widget containing a Cloudflare security challenge"]', 'src')
      #print("Iframe Src:", iframe_src)
      print("done")
      time.sleep(5)

#cookies = {"__cf_bm":"cnDu1olQ1_Xk.sv_sSbfAhy6HX3QDIdyywrsuB534R8-1739100940-1.0.1.1-qPtS0cFHH3ILEDEy2Cmr2xeVMIh7P4Jb2_6k97pibvvMMtvyRUT9gpsFsH8riWp5XGUWa4HTtTuwCwse8uKjNg"}





def get_match_player_points(fixture,fixtureId):
    url = 'https://stake.com/_api/graphql'
    print("cookies")
    print(global_cookies)
    cookie_string = "; ".join([f"{key}={value}" for key, value in global_cookies.items()])
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
        # with open('/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/python_scripts/response_data.json', 'w') as f:
        #   json.dump(response_data, f, indent=4)
        # with open('/home/tk-lpt-0809/Documents/NBA-data-scraper-scrapper_init/python_scripts/match_player_points.json', 'w') as f:
        #     json.dump(response, f, indent=4)
        return response


    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch match player points data: {e}")
        print(response.text)
        return {}
getNewCookies()
print(global_cookies)
print(get_match_player_points("45048537-charlotte-hornets-milwaukee-bucks","00b190c8-f0b0-4011-8111-844e665821f0"))