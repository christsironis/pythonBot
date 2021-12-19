from datetime import date
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as url
import smtplib
import redis
import sys
import os

def SendEmail(error):
	try:
		fromMy = 'tsiochris0002@yahoo.gr' # fun-fact: from is a keyword in python, you can't use it as variable, did abyone check if this code even works?
		to  = 'christsironiss@gmail.com'
		subj='PythonBot'
		date='2/1/2010'
		message_text=error
		msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )

		username = str('tsiochris0002@yahoo.gr')  
		password = str('yeilupckstpfkofo')  

		server = smtplib.SMTP("smtp.mail.yahoo.com",587)
		server.starttls()
		server.login(username,password)
		server.sendmail(fromMy, to,msg)
		server.quit()  
		print("Email with error has been send!")

	except:
		print("Error created during email creation!")


def LogIn():
	try:
		username= "christsironiss@gmail.com"
		password= "abcdefghik"

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

		browser.get(('https://vod.antenna.gr'))

		loginButton2 = WebDriverWait(browser, 20).until(
			EC.visibility_of_element_located((By.XPATH, '//div[@class="login-box"]//button[1]//span')))
			
		browser.execute_script("arguments[0].click();", loginButton2)

		browser.switch_to.window(browser.window_handles[-1])
		print(browser.window_handles)
		print(browser.current_url)

		# pop window interaction
		userInput = browser.find_element(By.ID,'loginId')
		userInput.send_keys(username)
		passInput = browser.find_element(By.ID,'password')
		passInput.send_keys(password)
		sundesh = browser.find_element(By.XPATH,'//div[@class="form-row"]//button')
		sundesh.click()

		# finds the request that has the password
		browser.wait_for_request("https://api.antenna.gr/v100/api/auth.class.api.php/logon/354",10)
		for request in browser.requests:
			if request.url == "https://api.antenna.gr/v100/api/auth.class.api.php/logon/354":
					token=url.urlencode(request.params)
					print(token)

		# sends the password to the redis server   
		red = redis.Redis(host='redis-13661.c233.eu-west-1-1.ec2.cloud.redislabs.com', port='13661', 
						password='CyPk7oc145cDyTnKvVfVVrDF3Ic0NZa5')
		old = red.get('password')
		red.set('old_password', old)
		red.set('password', token)

		browser.quit()
		
	except:
		print(sys.exc_info())
		SendEmail(sys.exc_info())


today=date.today().weekday()

if today == 0 or today == 3 :
	LogIn()
else :
	print("Executes only on Monday=0 and wednesday=3 today is " + str(date.today().weekday()) )
