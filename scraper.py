from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import numpy as np
import requests

def send_to_telegram(message):

    apiToken = '6694185107:AAFlsOoN61IkOET3ISPjBSGU3e7E18hu8Uw'
    chatID = '6445257283'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

chrome_service = Service(ChromeDriverManager().install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.implicitly_wait(10) 

driver.get('https://www.room.nl/aanbod/studentenwoningen#?gesorteerd-op=publicatiedatum-&locatie=Delft-Regio%2BHaaglanden%252F%2BLeiden&woningsoort=1')

rooms = driver.find_elements(By.XPATH, "//*[contains(@id,'object-tile')]")

room_ids = []
for i in rooms:
    room_ids.append(i.get_attribute("id"))
    
room_ids_new = np.array(room_ids)

room_ids_old = np.loadtxt("rooms.csv", dtype = str)

if not np.array_equal(np.sort(room_ids_new.flat), np.sort(room_ids_old.flat)):
    send_to_telegram("New room available!!!")
    np.savetxt("rooms.csv", room_ids, fmt='%s')
