import requests
from datetime import datetime, timedelta
import pytz
from driver_setup import get_driver


import time, json

cookie = None

def get_cookie_fronius(url):
    # url = 'https://www.solarweb.com/Home/GuestLogOn?pvSystemId=8a1561d2-1393-4cc0-a7d5-939b6346e631'
    driver = get_driver()

    try:
        driver.get(url)
    except Exception as e:
        print(e.message)

    # Wait for the page to load and make any necessary interactions
    time.sleep(10)  # Adjust the sleep duration as needed

    # Capture network requests from the page
    logs = driver.get_log('performance')

    # Filter the network requests to get the relevant data
    network_requests = [log['message'] for log in logs if json.loads(log["message"]).get("message", {}).get("method") == 'Network.requestWillBeSentExtraInfo']

    # Process and print the network requests
    for req in network_requests:
        obj = json.loads(req)
        if "GetWidgetChart" in req:            
            try:
                new_cookie = ""
                for cook in obj["message"]["params"]["associatedCookies"]:
                    new_cookie += cook["cookie"]["name"] + "=" + cook["cookie"]["value"] + "; "

                global cookie
                cookie = new_cookie
                break
            except Exception:
                continue

    print(cookie)
    
    current_url = driver.current_url

    # Close the page
    try:
        driver.quit()
    except Exception as e:
        print(e.message)

    return current_url


def get_month_data(month, year, id):
    global cookie
    url2 = "https://www.solarweb.com/Chart/GetChartNew?pvSystemId=" + id + "&year=" + str(year) + "&month=" + str(month) + "&day=01&interval=month&view=production"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Pragma': 'no-cache',
        'Referer': 'https://www.solarweb.com/PvSystems/PvSystem?pvSystemId=' + id,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }

    response = requests.get(url2, headers=headers)
    data = None

    if response.status_code == 200:
        data = json.loads(response.text)['settings']['series']
        if data != []:
            data = data[0]['data']
    else:
        print(f'Failed to get data from Fronius. Status code: {response.status_code}')
        return None
    retval = {}
    
    for ts, val in data:
        dt_object = datetime.fromtimestamp(ts/1000, pytz.timezone('GMT'))
        date_string = dt_object.strftime("%Y-%m-%d")

        retval[date_string] = val

    return retval



if __name__=='__main__':
    get_cookie_fronius()
    print(get_month_data(12, 2023, 'b78bc29c-7a93-46d9-905e-51625fffdd77'))
