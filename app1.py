from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from urllib.parse import quote
import os

message = quote(message)

data = pd.read_csv('updated_filtered_volume.csv')



options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=D:/var/tmp/chrome_user_data")

driver = webdriver.Chrome(executable_path=r"D:\Data Science\chromedriver-win64\chromedriver-win64\chromedriver.exe",
                          options=options)
print('Once your browser opens up sign in to web whatsapp')
driver.get('https://web.whatsapp.com')
input(style.MAGENTA + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER..." + style.RESET)


import time
delay = 30


for idx, (name, number) in enumerate(zip(names, numbers)):
    number = number.strip()
    if number == "":
        continue
    print('{}/{} => Sending message to {}.'.format((idx+1), total_number, [name, number]))
    
    try:
        url = f'https://web.whatsapp.com/send?phone={number}&text=Dear {name}, {message}'
        sent = False
        for i in range(1):
            if not sent:
                driver.get(url)
                try:
                    time.sleep(60)
                    click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='11']")))
                except Exception as e:
                    print(f"\nFailed to send message to: {number}, retry ({i+1}/3)")
                    print("Make sure your phone and computer is connected to the internet.")
                    print("If there is an alert, please dismiss it.")
                else:
                    time.sleep(1)
                    click_btn.click()
                    sent=True
                    time.sleep(3)
                    print(style.GREEN + 'Message sent to: ' + number + style.RESET)
    except Exception as e:
        print(style.RED + 'Failed to send message to ' + number + str(e) + style.RESET)

# driver.close()