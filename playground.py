from selenium import webdriver
from selenium.webdriver.edge import service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

edgeOption = webdriver.EdgeOptions()
edgeOption.use_chromium = True
edgeOption.add_argument("--headless")
edgeOption.add_argument("--disable-logging")
edgeOption.add_argument('--ignore-ssl-errors=yes')
edgeOption.add_argument('--ignore-certificate-errors')
#chromeOption.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
s=service.Service(r'C:\Users\a180046\VSCode\drivers\msedgedriver.exe')
driver = webdriver.ChromiumEdge(service=s, options=edgeOption)
driver.refresh()
driver.implicitly_wait(5)


driver.get('https://10.2.4.72:8443/aeonix')
driver.implicitly_wait(15)

username = 'aeonixadmin'
#password = 'Ujnm^678'
password = 'anx'
driver.find_element(By.ID, "loginForm:loginUserName").send_keys(username)
driver.find_element(By.ID, "loginForm:password").send_keys(password)
driver.find_element(By.ID, "loginForm:loginBtn").send_keys(Keys.RETURN)

time.sleep(2)


driver.get('https://10.2.4.72:8443/aeonix/rs/system/cluster.jsf')
#driver.get('https://172.28.9.221:8443/aeonix/rs/system/cluster.jsf')




i = 0
print('----------------')
rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:clusterobj']/tbody/tr")
print (len(rwdata))
for r in rwdata:
    i = i + 1
    print(str(i) + ' ' + r.text)

print('----------------')
l = driver.find_elements(By.XPATH, "//img[@title='Connection status: OK']")
print ('Connection OK ' + str(len(l)))
l = driver.find_elements(By.XPATH, "//img[@title='Connection status: Not connected']")
print ('Not Connected ' + str(len(l)))
    

print('----------------')
rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:totalEP']")
print (len(rwdata))
for r in rwdata:
   print(r.text)

i = 0
print('----------------')
rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:clusterIntegrityTable']/tbody/tr")
print (len(rwdata))
for r in rwdata:
    i = i + 1
    print(str(i) + ' ' + r.text)
#to close the browser




#time.sleep(15)
driver.close()
driver.quit()