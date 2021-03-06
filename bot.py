from datetime import date
from localStorage import *
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as url
import requests
import smtplib
import redis
import sys
import re
import os


def SendEmail(funct, error):
    try:
        if emailSend == True: return
        # fun-fact: from is a keyword in python, you can't use it as variable, did abyone check if this code even works?
        fromMy = 'tsiochris0002@yahoo.gr'
        to = 'christsironiss@gmail.com'
        subj = 'PythonBot'
        date = '2/1/2010'
        message_text = error
        msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (fromMy, to, subj, date, message_text)

        username = str('tsiochris0002@yahoo.gr')
        password = str('yeilupckstpfkofo')

        server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(fromMy, to, msg)
        server.quit()
        print("Error in "+funct+".Email has been send!")

    except:
        print("Error created during email creation!")

def Browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    #  The first one will make it so the "navigator.webdriver=true" variable in javascript doesn't show. Sites can access that variable to check if your using automation and block you or make you solve a captcha.
    chrome_options.add_argument('disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    return browser


def LogIn():
    try:
        username = "tsiochris0003@yahoo.gr"
        # username = "christsironiss@gmail.com"
        password = "abcdefghik"

        browser = Browser()

        browser.get(('https://vod.antenna.gr'))

        loginButton = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="login-box"]//button[1]//span')))

        # set device_id on localstorage
        storage = LocalStorage(browser)
        storage["SHARED_DEVICE"]='{"deviceId-v1":"Web-v1-2bf2d831ef48df5887a7c31fee76927d-8d87f8ebfd43371dab146e7d7cfa5a3a-0.4778393430973782","messageInfo":{"pushtestId":{"displayCount":0,"lastShown":0,"expiresAfter":"2022-06-06T00:00:00Z","capProcessedTime":1641729043}},"installTimestamp":1641729042,"lastLaunchTimestamp":1641729042,"launches":1,"lastVersion":"1.0.7","launchesSinceUpgrade":1}'

        browser.refresh()

        loginButton = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="login-box"]//button[1]//span')))

        browser.execute_script("arguments[0].click();", loginButton)
        browser.switch_to.window(browser.window_handles[-1])
        print(browser.window_handles)
        print(browser.current_url)

        # popup window interaction
        # loginButton = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="top-button-section"]//a/button[@class="secondary-button"]')))
        # browser.execute_script("arguments[0].click();", loginButton)
        userInput = browser.find_element(By.ID, 'loginId')
        userInput.send_keys(username)
        passInput = browser.find_element(By.ID, 'password')
        passInput.send_keys(password)
        sundesh = browser.find_element(By.XPATH, '//div[@class="form-row"]//button')
        sundesh.click()

        # finds the request that has the password
        browser.wait_for_request("https://api.antenna.gr/v100/api/auth.class.api.php/logon/354", 10)
        for request in browser.requests:
                if request.url == "https://api.antenna.gr/v100/api/auth.class.api.php/logon/354":
                    token = url.urlencode(request.params)
                    print(token)

                    # sends the password to the redis server
                    red = redis.Redis(host='redis-13661.c233.eu-west-1-1.ec2.cloud.redislabs.com', port='13661',
                                        password='CyPk7oc145cDyTnKvVfVVrDF3Ic0NZa5')
                    old = red.get('password')
                    red.set('old_password', old)
                    red.set('password', token)
                    red.quit()
                    browser.quit()
                    return token
    except:
        print(sys.exc_info())
        SendEmail("Selenium Login \n", sys.exc_info())
        emailSend=True


def LoginToken(password):
    try:
        post = requests.post("https://api.antenna.gr/v100/api/auth.class.api.php/logon/354",
                             headers={
                                 "accept": "*/*",
                                 "accept-language": "en,el;q=0.9",
                                 "content-type": "application/x-www-form-urlencoded",
                             },
                             data=password)
        data = post.json()
        return data["LogonResponse"]["Success"]['LoginToken']
    except:
        print(sys.exc_info())
        SendEmail("LoginToken \n", sys.exc_info())
        emailSend=True


def deregester(password, token):
    try:
        post = requests.post("https://api.antenna.gr/v100/api/auth.class.api.php/deregister/354?format=json&seviceID=default",
                             headers={
                                 "accept": "*/*",
                                 "accept-language": "en,el;q=0.9",
                                 "content-type": "application/x-www-form-urlencoded",
                             },
                             data=re.findall(".*(?=username)", password)[0] + "loginToken=" + token)
        print(post.json())
    except:
        print(sys.exc_info())
        SendEmail("Deregestration \n", sys.exc_info())
        emailSend=True


today = date.today().weekday()
emailSend=False
override = 0
if len(sys.argv) > 1:
    override = sys.argv[1]

if (today == 0 or today == 3 or override):
    password = LogIn()
    loginToken = LoginToken(password)
    deregester(password, loginToken)
else:
    print("Executes only on Monday=0 and thirsday=3 today is", today)
