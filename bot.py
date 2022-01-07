from datetime import date
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
        # fun-fact: from is a keyword in python, you can't use it as variable, did abyone check if this code even works?
        fromMy = 'tsiochris0002@yahoo.gr'
        to = 'christsironiss@gmail.com'
        subj = 'PythonBot'
        date = '2/1/2010'
        message_text = error
        msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
            fromMy, to, subj, date, message_text)

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


def ReadSession():
    try:
        # sends the password to the redis server
        red = redis.Redis(host='redis-13661.c233.eu-west-1-1.ec2.cloud.redislabs.com', port='13661',
            password='CyPk7oc145cDyTnKvVfVVrDF3Ic0NZa5')
        url = red.get('url')
        session_id = red.get('session_id')
        print(url,session_id)
        red.quit()
        print('webdriver session details was read')
        data=[url,session_id]
        return data
    except:
        print(sys.exc_info())


def writeSession(driver):
    url = driver.command_executor._url
    session_id = driver.session_id
    # sends the password to the redis server
    red = redis.Redis(host='redis-13661.c233.eu-west-1-1.ec2.cloud.redislabs.com', port='13661',
        password='CyPk7oc145cDyTnKvVfVVrDF3Ic0NZa5')
    red.set('url', url)
    red.set('session_id', session_id)
    red.quit()
    print('Wrote webdriver session details')


def CreateBrowser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    #  The first one will make it so the "navigator.webdriver=true" variable in javascript doesn't show. Sites can access that variable to check if your using automation and block you or make you solve a captcha.
    chrome_options.add_argument(
        'disable-blink-features=AutomationControlled')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    print("webdriver.chrome as browser has been created.")
    return browser


def LogIn():
    try:
        username = "tsiochris0002@yahoo.gr"
        # username = "christsironiss@gmail.com"
        password = "abcdefghik"
        data = ReadSession()
        browser=0
        if len(data) == 0:
            browser = CreateBrowser()
            print("mlkaaa2222222")
            writeSession(browser)
        else:
            print("mlkaaa")
            executor_url = data[0]
            session_id = data[1]
            # session_id.strip()
            print(executor_url)
            print(session_id)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            #  The first one will make it so the "navigator.webdriver=true" variable in javascript doesn't show. Sites can access that variable to check if your using automation and block you or make you solve a captcha.
            chrome_options.add_argument(
                'disable-blink-features=AutomationControlled')
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            browser = webdriver.Remote(command_executor=executor_url, chrome_options=chrome_options)
            browser.session_id = session_id


        browser.get(('https://vod.antenna.gr'))

        loginButton2 = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="login-box"]//button[1]//span')))

        browser.execute_script("arguments[0].click();", loginButton2)

        browser.switch_to.window(browser.window_handles[-1])
        print(browser.window_handles)
        print(browser.current_url)

        # pop window interaction
        userInput = browser.find_element(By.ID, 'loginId')
        userInput.send_keys(username)
        passInput = browser.find_element(By.ID, 'password')
        passInput.send_keys(password)
        sundesh = browser.find_element(
            By.XPATH, '//div[@class="form-row"]//button')
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
                    # browser.quit()
                    return token
    except:
        print(sys.exc_info())
        SendEmail("Selenium Login \n", sys.exc_info())


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


def deregester(password, token):
    try:
        post = requests.post("https://api.antenna.gr/v100/api/auth.class.api.php/deregister/354?format=json&seviceID=default",
                             headers={
                                 "accept": "*/*",
                                 "accept-language": "en,el;q=0.9",
                                 "content-type": "application/x-www-form-urlencoded",
                             },
                             data=re.findall("version.*&username", password)[0].split("username")[0] + "loginToken=" + token)
        print(post.json())
    except:
        print(sys.exc_info())
        SendEmail("Deregestration \n", sys.exc_info())


today = date.today().weekday()

override = 0
if len(sys.argv) > 1:
    override = sys.argv[1]

print(ReadSession())

# if (today == 0 or today == 3 or override):
#     password = LogIn()
#     loginToken = LoginToken(password)
#     deregester(password, loginToken)
# else:
#     print("Executes only on Monday=0 and wednesday=3 today is", today)
