"""CDP.network.ResponseReceived with CDP.network.ResourceType.XHR."""
import ast
import asyncio
import colorama
import mycdp
import sys
import time
from seleniumbase.undetected import cdp_driver

xhr_requests = []
last_xhr_request = None
c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
cr = colorama.Style.RESET_ALL
if "linux" in sys.platform:
    c1 = c2 = cr = ""

async def get_url_grphqls(driver,url,time_to_wait=20):
    global xhr_requests
    global last_xhr_request
    #xhr_responses = await receiveXHR(driver, xhr_requests)
    tab2 = await driver.get(url)
    listenXHR(tab2)
    print(f"wait for {time_to_wait} sec")
    for x in range(15):
        print(x, end="\r")
        time.sleep(1)  
    xhr_responses = await receiveXHR(tab2, xhr_requests)
    for response in xhr_responses:
        print(c1 + "*** ==> XHR Request URL <== ***" + cr)
        print(f'{response["url"]}')
        is_base64 = response["is_base64"]
        b64_data = "Base64 encoded data"
        try:
            headers = ast.literal_eval(response["body"])["headers"]
            print(c2 + "*** ==> XHR Response Headers <== ***" + cr)
            print(headers if not is_base64 else b64_data)
        except Exception:
            response_body = response["body"]
            print(c2 + "*** ==> XHR Response Body <== ***" + cr)
            print(response_body if not is_base64 else b64_data)

def listenXHR(page):
    async def handler(evt):

        # Get AJAX requests
        if evt.type_ is mycdp.network.ResourceType.FETCH  and evt.response.url.startswith("https://stake.com/_api/graphql"):
            print("evt.type_")
            print(evt.type_)
            print(evt.response.url)
            xhr_requests.append([evt.response.url, evt.request_id])
            global last_xhr_request
            last_xhr_request = time.time()
    page.add_handler(mycdp.network.ResponseReceived, handler)

async def receiveXHR(page, requests):
    responses = []
    retries = 0
    max_retries = 5
    await asyncio.sleep(6)
    # Wait at least 2 seconds after last XHR request for more
    while True:
        if last_xhr_request is None or retries > max_retries:
            break
        if time.time() - last_xhr_request <= 2:
            retries = retries + 1
            await asyncio.sleep(6)
            continue
        else:
            break
    await page

    # Loop through gathered requests and get response body
    print("requests")
    print(requests)
    print("==========================")

    for request in requests:
        try:
            print("waitning for 2")
            await asyncio.sleep(2)
            res = await page.send(mycdp.network.get_response_body(request[1]))
            print("Response URL:", request[0])
            print("res=========", res)
            if res is None:
                continue
            responses.append({
                "url": request[0],
                "body": res[0],
                "is_base64": res[1],
            })
        except Exception as e:
            print("Error getting response:", e)
    return responses

async def crawl():
    driver = await cdp_driver.cdp_util.start_async()
    tab = await driver.get("about:blank")
    listenXHR(tab)
    tab = await driver.get("https://stake.com/")
    #listenXHR(tab)

    # Change url to something that makes ajax requests
    ##tab = await driver.get("https://stake.com/sports/basketball")
    await asyncio.sleep(10)

    # driver.uc_gui_click_captcha()
    #await get_url_grphqls(driver,"https://stake.com/sports/basketball")

    #return 
    xhr_responses = await receiveXHR(driver, xhr_requests)
    tab = await driver.get("https://stake.com/sports/basketball/usa/nba/45048496-philadelphia-76ers-boston-celtics")
    #listenXHR(tab2)
    await asyncio.sleep(30)


    xhr_responses = await receiveXHR(tab, xhr_requests)
    for response in xhr_responses:
        print(c1 + "*** ==> XHR Request URL <== ***" + cr)
        print(f'{response["url"]}')
        is_base64 = response["is_base64"]
        b64_data = "Base64 encoded data"
        try:
            headers = ast.literal_eval(response["body"])["headers"]
            print(c2 + "*** ==> XHR Response Headers <== ***" + cr)
            print(headers if not is_base64 else b64_data)
        except Exception:
            response_body = response["body"]
            print(c2 + "*** ==> XHR Response Body <== ***" + cr)
            print(response_body if not is_base64 else b64_data)

    await asyncio.sleep(30)

if __name__ == "__main__":
    print("================== Starting ==================")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(crawl())


