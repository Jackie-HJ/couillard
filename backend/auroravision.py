from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json, time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver_service = Service('./chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=driver_service, options=chrome_options)


def get_cookie():

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



get_cookie()