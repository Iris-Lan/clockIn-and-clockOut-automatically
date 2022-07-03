# This is a sample Python script to do clock_in or clock_out process and record logs via crontab schedule.

import time
import json
import datetime
import pygsheets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def login():
    with open('./json/login.json') as f:
        data = json.load(f)

    # trigger to login or turn the permission off if I don't want to login anytime I chose.
    gc = pygsheets.authorize(service_file='../sheetkey/sheetkey.json')
    sh = gc.open_by_url(data['googleSheetUrl'])
    ws = sh.worksheet_by_title('sheet1')
    if ws.cell('A1').value == 'OFF':
        print("If I don't want to login, I'll turn the permission off so that login process can't be done!!")
    else:
        # login
        service_obj = Service("chromedriverFileUrl")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service_obj, options=options)
        driver.get(data['loginUrl'])
        driver.find_element(By.NAME, "company").clear()
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "company").send_keys(data['company'])
        driver.find_element(By.NAME, "username").send_keys(data['username'])
        driver.find_element(By.NAME, "password").send_keys(data['password'])
        driver.find_element(By.ID, "login-button").click()
        # The time to distinguish between clock_in and clock_out: default value is 2pm.
        if datetime.datetime.now().hour > 14:
            print("It's afternoon now.")
            driver.execute_script("document.getElementById('clockout').click()")
        else:
            print("It's morning now.")
            driver.execute_script("document.getElementById('clockin').click()")
        time.sleep(3)
    driver.quit()


# This login project would be scheduled and the clock_in/clock_out logs are also recorded into log file via crontab.
if __name__ == '__main__':
    print_hi('Iris')

    # check what day is today
    today = datetime.datetime.now().weekday() + 1
    print("Today is the {}th day of this weekend.".format(today))
    # Today is a day off!! Yeah~~~~~~
    if (today % 7 == 0) or (today % 7 == 6):
        print("Today is the {}th day of this weekend. No need to clockIn or clockOut～～～".format(today))
        print("=================")
    # Sadly, today is a working day....
    else:
        # To record the logs.
        print("It's time to login and do clockIn or clockOut：{}".format(datetime.datetime.now()))
        # clock_in or clock_out
        login()
        print("ClockIn or clockOut process finished successfully：{}".format(datetime.datetime.now()))
        print("=================")