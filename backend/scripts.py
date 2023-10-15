from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests


import time, json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver_service = Service('./chromedriver-mac-arm64/chromedriver')

driver = webdriver.Chrome(service=driver_service, options=chrome_options)
url = 'https://www.solarweb.com/Home/GuestLogOn?pvSystemId=8a1561d2-1393-4cc0-a7d5-939b6346e631'
driver.get(url)

# Wait for the page to load and make any necessary interactions
time.sleep(5)  # Adjust the sleep duration as needed

# Capture network requests from the page
logs = driver.get_log('performance')

# Filter the network requests to get the relevant data
network_requests = [log['message'] for log in logs]

# Process and print the network requests
data = []
cookie = None
for req in network_requests:
    obj = json.loads(req)
    try:
        cookie = obj["message"]["params"]["headers"]["Cookie"]
        break
    except KeyError:
        pass

# Close the browser
driver.quit()

url = 'https://www.solarweb.com/Chart/GetWidgetChart?PvSystemId=369bf812-62f9-4d4f-b1d4-4ee52ac4e47a&_=1697406048905'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'Pragma': 'no-cache',
    'Referer': 'https://www.solarweb.com/PvSystems/PvSystem?pvSystemId=369bf812-62f9-4d4f-b1d4-4ee52ac4e47a',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'macOS',
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.text)
    with open('api.json', 'w') as f:
       f.write(response.text)
else:
    print(f"Request failed with status code {response.status_code}")