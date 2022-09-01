from selenium import webdriver
from selenium.webdriver.edge import service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

import time

edgeOption = webdriver.EdgeOptions()
edgeOption.use_chromium = True
edgeOption.add_argument("--headless")
edgeOption.add_argument("--disable-logging")
edgeOption.add_argument('--ignore-ssl-errors=yes')
edgeOption.add_argument('--ignore-certificate-errors')
#chromeOption.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
#s=service.Service(r'C:\Users\a180046\VSCode\drivers\msedgedriver.exe')
s=service.Service(r'bin\drivers\msedgedriver.exe')
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



clusterobj_titles = ['HOST', 'ADDR', 'EPS', 'IN', 'OUT', 'REC', 'ACC', 'LIC', 'TIME']
clusterobj = {}

print()
idx = 0
rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:clusterobj']/tbody/tr/td")
for r in rwdata:
    idx += 1
    if idx == 2: 
        nested = r.text
        clusterobj[nested] = {}
    if idx >= 3 and idx < 11: clusterobj[nested][clusterobj_titles[idx-2]] = r.text
    if idx == 10: idx = 0
print (str(int(len(rwdata)/10)) + ' server(s) environmnt: ')
clusterobj_df = pd.DataFrame.from_dict(clusterobj).T
#print(clusterobj)
print(clusterobj_df)

srv_stat_ok = driver.find_elements(By.XPATH, "//img[@title='Connection status: OK']")
print (str(len(srv_stat_ok)) + ' server(s) are in \'Connection OK\' state' )
srv_stat_nc = driver.find_elements(By.XPATH, "//img[@title='Connection status: Not connected']")
print (str(len(srv_stat_nc)) + ' server(s) are in \'Not Connected\' state' )

idx = 0
rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:totalEP']/tbody/tr/td")
for r in rwdata:
    idx += 1
    if idx == 3:
        tot_eps = str(r.text)
        print('Total registered endpoints: ' + tot_eps)

clusterIntegrityTitles =[]
clusterIntegrityTable = []
clusterIntegrityPanel ={}

idx = 0
rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:clusterIntegrityTable']/tbody/tr/td")

for r in rwdata:
    idx += 1
    if idx == 1: 
        clusterIntegrityTitles.append(r.text)
    clusterIntegrityTable.append(r.text)
    if idx == 5: idx = 0

i = 0
for idx in range(len(rwdata)):
    if idx %5 == 0: 
        #print(clusterIntegrityTable[idx])
        nested = clusterIntegrityTable[idx]
        clusterIntegrityPanel[nested] = {}
        continue
    clusterIntegrityPanel[nested][clusterIntegrityTitles[i]] = clusterIntegrityTable[idx]
    i += 1
    if i >= 4: i = 0
clusterIntegrityPanel_df = pd.DataFrame.from_dict(clusterIntegrityPanel).T
#print(clusterobj)
print(clusterIntegrityPanel_df)


driver.close()
driver.quit()