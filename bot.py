from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as url
import requests
import smtplib
import browser 
import redis
import sys
import re

def SendEmail(funct,error):
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


def LogIn():
    try:
        username = "tsiochris0002@yahoo.gr"
        # username = "christsironiss@gmail.com"
        password = "abcdefghik"

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
        browser.wait_for_request(
            "https://api.antenna.gr/v100/api/auth.class.api.php/logon/354", 10)
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

        # browser.quit()
        return token

    except:
        print(sys.exc_info())
        SendEmail("Selenium Login \n",sys.exc_info())


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
        SendEmail("LoginToken \n",sys.exc_info())


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
        SendEmail("Deregestration \n",sys.exc_info())


today=date.today().weekday()

override = 0
if len(sys.argv) > 1:
    override = sys.argv[1]

if (today == 0 or today == 3 or override ) :
    if browser.browser :
        print("browser already exists")
    else:
        print("browser not found, initialize CreateBrowser")
        browser = browser.CreateBrowser()
    password = LogIn()
    loginToken = LoginToken(password)
    deregester(password, loginToken)
else:
    print("Executes only on Monday=0 and wednesday=3 today is",today)

