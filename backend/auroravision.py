from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json, time
import requests
from datetime import datetime, timedelta
import pytz

start_date = datetime(2022, 10, 1)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver_service = Service('./chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=driver_service, options=chrome_options)


def get_cookie_auroravision():

    url = 'https://easyview.auroravision.net/easyview/index.html?entityId=17722147'
    driver.get(url)

    # Wait for the page to load and make any necessary interactions
    time.sleep(5)  # Adjust the sleep duration as needed

    # Capture network requests from the page
    logs = driver.get_log('performance')

    # Filter the network requests to get the relevant data
    network_requests = [json.loads(log['message']) for log in logs]

    cookie = None
    for req in network_requests:
        try:
            cookie = req["message"]["params"]["headers"]["cookie"]
            break
        except KeyError:
            pass

    return cookie + '; _gat=1'

def get_month_data_auroravision(eids, start_date, end_date, cookie):
    url = f'https://easyview.auroravision.net/easyview/services/gmi/summary/GenerationEnergy.json?type=GenerationEnergy&eids={eids}&tz=America%2FChicago&start={start_date}&end={end_date}&range=30D&hasUsage=false&label=30D&dataProperty=chartData&binSize=Min15&bins=true&plantPowerNow=false&v=2.1.62'
    print(cookie)
    headers = {
        'Accept': 'application/json',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Host': 'easyview.auroravision.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': f'https://easyview.auroravision.net/easyview/index.html?entityId={eids}',
        'Cookie': cookie,
        'Sec-Fetch-Dest': 'empty',
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text).get('chartData', [])
        print(json.loads(response.text))

        retval = {}

        for entry in data:
            ts = entry['timestamp']
            val = entry['value']
            dt_object = datetime.fromtimestamp(ts / 1000, pytz.timezone('GMT'))
            date_string = dt_object.strftime('%Y-%m-%d')
            retval[date_string] = val

        return retval

    return None


cookie = get_cookie_auroravision()
print(get_month_data_auroravision('17722147', '20231015', '20231115', cookie))