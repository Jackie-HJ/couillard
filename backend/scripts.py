from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from datetime import datetime, timedelta
import pytz


import time, json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver_service = Service('./chromedriver-mac-arm64/chromedriver')

driver = webdriver.Chrome(service=driver_service, options=chrome_options)

cookie = None

def get_cookie(pvSystemId):
    url = 'https://www.solarweb.com/Home/GuestLogOn?pvSystemId=' + str(pvSystemId)
    print("url: " + url)
    driver.get(url)

    # Wait for the page to load and make any necessary interactions
    time.sleep(5)  # Adjust the sleep duration as needed

    # Capture network requests from the page
    logs = driver.get_log('performance')

    # Filter the network requests to get the relevant data
    network_requests = [log['message'] for log in logs]

    # Process and print the network requests
    for req in network_requests:
        obj = json.loads(req)
        try:
            global cookie
            cookie = obj["message"]["params"]["headers"]["Cookie"]
            break
        except KeyError:
            pass

    # Close the browser
    driver.quit()


def get_month_data(month, year, id):
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
        data = json.loads(response.text)['settings']['series'][0]['data']
    else:
        return response.status_code
    
    retval = {}
    
    for ts, val in data:
        dt_object = datetime.fromtimestamp(ts/1000, pytz.timezone('GMT'))
        date_string = dt_object.strftime("%Y-%m-%d")

        retval[date_string] = val

    return retval



if __name__=='__main__':
    print(get_month_data(1, 2023, '369bf812-62f9-4d4f-b1d4-4ee52ac4e47a'))