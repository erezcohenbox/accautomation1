from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

#capabilities = DesiredCapabilities.CHROME.copy()
#capabilities["acceptInsecureCerts"] = True
#driver = webdriver.Chrome('C:\\Users\\a180046\\VSCode\\drivers\\chromedriver.exe', desired_capabilities=capabilities)

#options = webdriver.ChromeOptions()
options = webdriver.EdgeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
#driver = webdriver.Chrome('C:\\Users\\a180046\\VSCode\\drivers\\chromedriver.exe', options=options)
driver = webdriver.Edge('C:\\Users\\a180046\\VSCode\\drivers\\msedgedriver.exe', options=options)

driver.implicitly_wait(15)
time.sleep(1)

driver.get('https://10.2.4.72:8443/aeonix')


driver.implicitly_wait(15)
time.sleep(2)
#element = driver.find_element(By.CLASS_NAME, "secondary-button small-link")
# get value of class attribute
#print (element)
#class_value = element.get_attribute('secondary-button small-link')
#print('class value: ', class_value)


username = 'aeonix'
password = 'anx'
driver.find_element(By.ID, "loginForm:loginUserName").send_keys(username)
driver.find_element(By.ID, "loginForm:password").send_keys(password)
#driver.find_element(By.XPATH,"//*[@id=\"organic-div\"]/form/div[3]/button").click()

time.sleep(2)

driver.find_element(By.ID, "loginForm:loginBtn").send_keys(Keys.RETURN)

#driver.close()
#driver.quit()