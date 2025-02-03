
import requests
from flask import Flask, jsonify

app = Flask(__name__)
@app.route('/get_todays_fixtures', methods=['GET'])
def get_todays_fixtures():
    url = 'https://stake.com/_api/graphql'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'access-control-allow-origin': '*',
        'content-type': 'application/json',
        'cookie': 'currency_currency=btc; currency_hideZeroBalances=false; currency_currencyView=crypto; session_info=undefined; fiat_number_format=en; casinoSearch=["Monopoly","Crazy Time","Sweet Bonanza","Money Train","Reactoonz"]; sportsSearch=["Liverpool FC","Kansas City Chiefs","Los Angeles Lakers","FC Barcelona","FC Bayern Munich"]; oddsFormat=decimal; sportMarketGroupMap={}; locale=en; _ga=GA1.1.1081632327.1737898125; intercom-id-cx1ywgf2=daa4dc0b-c9f5-4b74-b1d3-8382250faf70; intercom-session-cx1ywgf2=; intercom-device-id-cx1ywgf2=768c7a72-c502-4a9f-8f65-53295fc9532e; _hjSessionUser_5261158=eyJpZCI6ImE3Mjk5OWVkLTEzMDItNWE2ZS1hMjRkLWU3ZTRmZTgyOWYyMiIsImNyZWF0ZWQiOjE3Mzc4OTgxMjYzODIsImV4aXN0aW5nIjp0cnVlfQ==; leftSidebarView_v2=minimized; sidebarView=hidden; cookie_consent=true; _hjSession_5261158=eyJpZCI6IjhiZmY4YzgyLTczMTQtNGJkNC05Y2JlLTg1Njk2MDA1ZGZmMyIsImMiOjE3MzgwOTQ4NzU0MDcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; cf_chl_rc_m=3; _cfuvid=VwaBuZan5tvThRLATQDSz54zkAmsLWELdlNjaPD.uAU-1738097733837-0.0.1.1-604800000; cf_clearance=PYsMvzjysk.bE8M502Ldc7fbUkfMgv1y4dnp1PdGIak-1738099369-1.2.1.1-.eKrmdIhGsDMPJ5Gn73mIa5USKbEKjHdDomB0CGwGrLmBQeIVNvtDufuT8ukNIjsUtl.tKbMu2bUn270ycrLYdml0bX_vPwu7KBkRIbLtpfUkYOZD8umi97muFmEJkvjLuX5x7bEPG2FFlSJgErA_pmQrZuCHC5IbYTTcys9P6Xo3J2zpmo7FUifnGzmwyOeYNrGKS0kSw1FdH8XaiSePdhKm7muIE2lUKlAtfyaK1abcU3XjsdVDWDv_hy5gcFuU4W80r7yVccHAfAcwYD9WufwWppyI22ea1_KfvHSu1vyo7sC5qaNXM3CUgpbB2wrtYyTgxzgTP6RDDXQe2QoxA; __cf_bm=.KG5aMj0Hkfd.0ad5kez6Vd0z.vLjogvTKGaUWFAFTk-1738099489-1.0.1.1-sG1xt6Z9uscpurAaFfoKaVivgeOc1h5fcO2gsUOF5XrONRtejw53iz75PZAemmXuiy7GsayVRa5dAFbSSSmbDQ; _ga_TWGX3QNXGG=GS1.1.1738094514.12.1.1738099860.0.0.0; __cf_bm=xwQLEe7hQBI40m2EKmAoQr2XsmiLQ_OnkIeSI9aBwlk-1738622548-1.0.1.1-WV96e.PvIac3Bhw06k9qU6.KHwUjZi1PrjuMijEEay9QgsGeBGUByKvluWUq039LGRTLGHMkzPmESXuVZUny9w',
        'origin': 'https://stake.com',
        'priority': 'u=1, i',
        'referer': 'https://stake.com/sports/basketball/outrights',
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
        'x-language': 'en',
        'x-operation-name': 'SportIndex',
        'x-operation-type': 'query'
    }
    data = {
        "query": '''
        query SportIndex($group: String!, $type: SportSearchEnum = popular) {
        slugSport(sport: "basketball") {
            id
            name
            templates(group: $group) {
            id
            name
            extId
            }
            firstTournament: tournamentList(type: $type, limit: 1) {
            id
            name
            fixtureCount(type: $type)
            fixtureList(type: $type, limit: 10) {
                ...FixturePreview
            }
            }
        }
        }

        fragment SportFixtureLiveStreamExists on SportFixture {
        id
        }

        fragment SportFixtureCompetitor on SportFixtureCompetitor {
        name
        extId
        countryCode
        abbreviation
        iconPath
        }

        fragment SportFixtureDataMatch on SportFixtureDataMatch {
        startTime
        competitors {
            ...SportFixtureCompetitor
        }
        teams {
            name
            qualifier
        }
        tvChannels {
            language
            name
            streamUrl
        }
        __typename
        }

        fragment SportFixtureDataOutright on SportFixtureDataOutright {
        name
        startTime
        endTime
        __typename
        }

        fragment CategoryTreeNested on SportCategory {
        id
        name
        slug
        sport {
            id
            name
            slug
        }
        }

        fragment TournamentTreeNested on SportTournament {
        id
        name
        slug
        category {
            ...CategoryTreeNested
            cashoutEnabled
        }
        }


        fragment FixturePreview on SportFixture {
        id
        ...SportFixtureLiveStreamExists
        status
        slug
        name
        provider
        marketCount(status: [active, suspended])
        extId
        data {
            __typename
            ...SportFixtureDataMatch
            ...SportFixtureDataOutright
        }
        tournament {
            ...TournamentTreeNested
        }
        }''',
        "variables": {
            "sport": "basketball",
            "group": "winner"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        fixtures_data = response.json()
        return jsonify({"status": "success", "data": fixtures_data}), 200
    
    else:
        print(f"Failed to fetch fixtures data: {response.status_code}")
        return jsonify({"status": "error", "message": "Failed to fetch fixtures data"}), response.status_code

if __name__ == "__main__":
    # scheduler_thread = threading.Thread(target=run_scheduler)
    # scheduler_thread.daemon = True
    # scheduler_thread.start()
    app.run(host='0.0.0.0', port=5000)
    
    
