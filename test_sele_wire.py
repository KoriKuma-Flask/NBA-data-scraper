import colorama
import mycdp
import sys
from seleniumbase import SB

c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
cr = colorama.Style.RESET_ALL
if "linux" in sys.platform:
    c1 = c2 = cr = ""

async def send_handler(event: mycdp.network.RequestWillBeSent):
    r = event.request
    s = f"{r.method} {r.url}"
    
    # Extract and print headers
    for k, v in r.headers.items():
        s += f"\n\t{k} : {v}"

    # Check for GraphQL request
    if r.method == "POST" and "graphql" in r.url.lower():
        if hasattr(r, "postData"):  # Some versions may use r.postData or r.post_data
            s += f"\n\nGraphQL Request Body:\n{r.postData}"

    print(c1 + "*** ==> RequestWillBeSent <== ***" + cr)
    print(s)

async def receive_handler(event: mycdp.network.ResponseReceived):
    r = event.response
    s = f"{r.status} {r.url}"
    
    # Extract and print headers
    for k, v in r.headers.items():
        s += f"\n\t{k} : {v}"
    
    # Print response body if available
    if hasattr(r, "body"):
        s += f"\n\nResponse Body:\n{r.body}"

    print(c2 + "*** ==> ResponseReceived <== ***" + cr)
    print(s)

with SB(uc=True, test=True, locale_code="en") as sb:
    sb.activate_cdp_mode("about:blank")

    url = "https://stake.com/sports/basketball"
    sb.cdp.open(url)
    sb.uc_gui_click_captcha()

    sb.cdp.add_handler(mycdp.network.RequestWillBeSent, send_handler)
    sb.cdp.add_handler(mycdp.network.ResponseReceived, receive_handler)
    sb.cdp.open(url)
    sb.sleep(20)


