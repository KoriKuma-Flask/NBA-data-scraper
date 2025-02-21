import requests

url = 'https://shuffle.com/graphql'
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'ip-country=PK; _ga=GA1.1.1389699345.1739203218; _fbp=fb.1.1739203219111.37627662415460352; ajs_anonymous_id=80ae1afb-37e5-4f07-97a3-9a390f0b85e7; intercom-id-w4g68fv7=03402502-78c5-4255-a91f-7abbd6a39b62; intercom-session-w4g68fv7=; intercom-device-id-w4g68fv7=b302613a-29c7-4e17-80c5-9bccaf99ce2b; _ga_WS1L4WVMG4=GS1.1.1739203218.1.1.1739203334.0.0.0; ph_phc_7qhjC04BVp6b3gMsRgWJyK7CG3QCVwfjnRgmYdiBMba_posthog=%7B%22distinct_id%22%3A%220194f097-0836-767c-9dac-e6f82273dfae%22%2C%22%24sesid%22%3A%5B1739203334521%2C%220194f097-0834-73a4-84e5-40e802899757%22%2C1739203217460%5D%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fshuffle.com%2Fsports%2Fbasketball%2F15-usa%2F132-nba%2F52630047-cleveland-cavaliers-vs-minnesota-timberwolves%22%7D%7D',
    'origin': 'https://shuffle.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://shuffle.com/sports/basketball/15-usa/132-nba/52630047-cleveland-cavaliers-vs-minnesota-timberwolves',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-correlation-id': 'g838p2dc1f-j7mi47ed60-1.54.0-1ijo9hkgv-3::anon'
}
data = {
    "operationName": "GetGlobalData",
    "variables": {},
    "query": """query GetGlobalData {
  appSettings {
    id
    geoRestrictedRegions
    geoRestrictedRegionsL1
    rain {
      minTipUSD
      minUsers
      maxUsers
      __typename
    }
    tip {
      minTipUSD
      minBalanceAfterTipUSD
      __typename
    }
    kycAge {
      country
      age
      __typename
    }
    dice {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    mines {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    plinko {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    crash {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    limbo {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    keno {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    hilo {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    blackjack {
      maxPayoutUSD
      maxBetUSD
      sidebetLimit
      minBetUSD
      __typename
    }
    roulette {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    wheel {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    tower {
      maxPayoutUSD
      maxBetUSD
      minBetUSD
      __typename
    }
    sportsBet {
      minBetUSD
      minPartialBetRatio
      __typename
    }
    sportsMaintenance {
      maintenanceStartDateTimeUTC
      maintenanceEndDateTimeUTC
      warningMaintenanceStartDateTimeUTC
      __typename
    }
    __typename
  }
  vipLevels {
    level
    amount
    __typename
  }
}"""
}

response = requests.post(url, headers=headers, json=data)
print(response.json())