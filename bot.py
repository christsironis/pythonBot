from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as url
import redis
import sys
import os
from selenium.webdriver.chrome.options import Options
cwd = os.getcwd()
sys.path.append(cwd)

print(cwd)

username= "christsironiss@gmail.com"
password= "abcdefghik"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920x1080") 
chrome_options.add_argument('disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')
CHROMEDRIVER_PATH = cwd+"\chromedriver.exe"
browser = webdriver.Chrome(options=chrome_options)

browser.get(('https://vod.antenna.gr'))

loginButton = WebDriverWait(browser, 20).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))

browser.execute_script("arguments[0].click();", loginButton)
print(browser.page_source)
loginButton2 = WebDriverWait(browser, 20).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@class="login-box"]//button[1]//span')))

browser.switch_to.window(browser.window_handles[-1])

print(browser.current_url)
userInput = browser.find_element(By.ID,'loginId')
userInput.send_keys(username)
passInput = browser.find_element(By.ID,'password')
passInput.send_keys(password)
sundesh = browser.find_element(By.XPATH,'//div[@class="form-row"]//button')
sundesh.click()

browser.wait_for_request("https://api.antenna.gr/v100/api/auth.class.api.php/logon/354",10)
for request in browser.requests:
	if request.url == "https://api.antenna.gr/v100/api/auth.class.api.php/logon/354":
			token=url.urlencode(request.params)
			print(token)
	    
red = redis.Redis(host='redis-13661.c233.eu-west-1-1.ec2.cloud.redislabs.com', port='13661', 
                password='CyPk7oc145cDyTnKvVfVVrDF3Ic0NZa5')
old = red.get('password')
red.set('old_password', old)
red.set('password', token)

browser.quit()


