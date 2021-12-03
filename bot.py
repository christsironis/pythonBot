from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as url
import redis
import os 

# Heroku stuff
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

username= "christsironiss@gmail.com"
password= "abcdefghik"

# browser = webdriver.Chrome()
browser.get(('https://vod.antenna.gr/#/'))

print("\nasdfasdfasdfadf\n")

loginButton = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='login-box']//button[1]//span"))
)
browser.execute_script("arguments[0].click();", loginButton)

print (loginButton)

# wait to make sure there are two windows open
WebDriverWait(browser, 10).until(lambda d: len(d.window_handles) == 2)


# wait to make sure the new window is loaded
WebDriverWait(browser, 10).until(lambda d: d.title != "")

# print (browser.title)
# switch windows
browser.switch_to.window(browser.window_handles[-1])

print(browser.page_source)

userInput = browser.find_element(By.ID,'loginId')
userInput.send_keys(username)
passInput = browser.find_element(By.ID,'password')
passInput.send_keys(password)
sundesh = browser.find_element(By.XPATH,'//div[@class="form-row"]//button')
sundesh.click()

# browser.wait_for_request("https://api.antenna.gr/v100/api/auth.class.api.php/logon/354",10)
# for request in browser.requests:
# 	if request.url == "https://api.antenna.gr/v100/api/auth.class.api.php/logon/354":
# 			token=url.urlencode(request.params)
# 			print(token)
	    

# print(token)

# red = redis.Redis(host='redis-13661.c233.eu-west-1-1.ec2.cloud.redislabs.com', port='13661', 
#                 password='CyPk7oc145cDyTnKvVfVVrDF3Ic0NZa5')
# old = red.get('password')
# red.set('old_password', old)
# red.set('password', token)


