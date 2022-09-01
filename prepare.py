import os, shutil, datetime, time
from turtle import left
from configobj import ConfigObj
import paramiko
from selenium import webdriver
from selenium.webdriver.edge import service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
pd.set_option('display.colheader_justify', 'right')

class bcolors:
    PROMPT  =   '\033[90m    > ' #GRAY
    PROMPTV =   '\033[90m'       #GRAY
    FAIL =      '\033[91m    > ' #RED
    FAILV =     '\033[91m'       #RED
    FAIL2 =     '\033[91m      ' #RED
    OK =        '\033[92m    > ' #GREEN
    OKV =       '\033[92m'       #GREEN
    WARNING =   '\033[93m    > ' #YELLOW
    WARNINGV =  '\033[93m'       #YELLOW
    WARNING2 =  '\033[93m      ' #YELLOW
    WARNINGX =  '\033[95m    > ' #PURPLE/PINK
    WARNINGXV = '\033[95m'       #PURPLE/PINK
    INFO =      '\033[96m    > ' #LIGHT BLUE
    INFOV =     '\033[96m'       #LIGHT BLUE
    INFO2 =     '\033[0m      '  #LIGHT BLUE
    MENU =      '\033[97m    > ' #WHITE
    MENUV =     '\033[97m'       #WHITE
    RESET =     '\033[0m'        #RESET
    CLS =       '\033[2J'        #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences


def create_sim_files(capacity, start_at, method):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    #method = 'intra'
    template_method = 'templates/'+ method + '/'
    remote_path = 'simulator/'
        
    servers_capacity = {
        1: [1000, 2000, 3000, 5000],
        2: [2000, 4000, 6000, 8000],
        3: [3000, 6000, 9000, 12000],
        4: [4000, 8000, 10000, 12000],
        5: [5000, 10000, 15000, 20000],
        6: [6000, 12000, 18000, 24000]
    }
    first_user =     [30000, 40000, 50000, 60000, 70000]
    method_type = ['intra', 'inter', 'trunk']

    if capacity == 0 or start_at == 0 or method_type =='':

        

        print()
        print(bcolors.INFO +'please choose 1 - 4 for total users amount to run with:' + bcolors.RESET)
        print(bcolors.INFO2, end ='')
        #print(servers_capacity[1][0])
        i = 0
        for element in servers_capacity[sections]:
            i += 1
            print(str(i) + '--> ' + str(element), end="  ")
        
        print(bcolors.RESET)
        print()
        try:
            choice = input("\r    Enter your choice [1-4]: ")
            if int(choice) < 1 or int(choice) > 4:
                print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
                return()
            capacity = servers_capacity[sections][int(choice) - 1]
            print(bcolors.INFO + str(capacity) + ' total users capacity was selected ' + bcolors.RESET)
            #return()
        except (ValueError, IndexError):
            print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
            return()
        
        
        print()
        print(bcolors.INFO +'please choose the first user to begin with:' + bcolors.RESET)
        print(bcolors.INFO2, end ="")
        i = 0
        for element in first_user:
            i += 1
            print(str(i) + '--> ' + str(element), end="  ")    
        
        print()
        print(bcolors.RESET)

        try:
            choice = input("\r    Enter your choice [1-5]: ")
            if int(choice) < 1 or int(choice) > 5:
                print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
                return()
            start_at = first_user[int(choice) - 1]
            print(bcolors.INFO + str(start_at) + ' as the first user was selected ' + bcolors.RESET)
            #return()
        except (ValueError, IndexError):
            print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
            return()

    print()
    print(bcolors.INFO + 'the following data was collected and saved: ' + bcolors.RESET)
    print(bcolors.INFO2 + '- load test configuration contains : ' + str(sections) + ' server(s)')
    print(bcolors.INFO2 + '- total capacity load amount of    : ' + str(capacity) + ' users') 
    print(bcolors.INFO2 + '- scope of imported uesrs          : from user #' + str(start_at) + ' to user #' + str(start_at + capacity - 1 ))
    print(bcolors.INFO2 + '- prefered load run method         : ' + method)

    # save all to 'temp' file
    temp = [str(sections), str(capacity), str(start_at), method]
    with open("temp", "w") as tempfile:
        tempfile.writelines(",".join(temp))
        tempfile.close()

    shutil.rmtree('scripts/', ignore_errors=True)
    main_local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method)
    os.makedirs(main_local_path, exist_ok = True)

    print()
    print(bcolors.INFO  + 'creating: aeonix \'import_' + str(capacity) + '_users.csv\' file having the following fields/order...' + bcolors.RESET) 
    print(bcolors.INFO2 + '\'User ID\', \'Internal aliases\', \'Description\', \'Phone name\', \'Phone type\', \'Phone Domain\'' + bcolors.RESET) 
    #fieldnames =  ['User ID', 'Internal aliases', 'Description', 'Phone name', 'Phone type', 'Phone Domain']
    with open(main_local_path +'/import_'+str(capacity)+'_users.csv', 'w') as usersfile:
        for counter in range(start_at, int(start_at + capacity)):
            usersfile.write(str(counter) +','+str(counter) +','+str(counter) +'_Desc,'+str(counter)+',SIP terminal'+',aeonix.com\n')
        usersfile.close()

    startuser=start_at

    for sectionnumber in range(1, sections + 1):
        print()
        print(bcolors.INFO + 'handling simulator SERVER_' + str(sectionnumber) + ' files:' + bcolors.RESET)

        serverdict = get_section_info(sectionnumber)

        sipp_local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(sectionnumber) + '/sipp')
        aeonix_local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(sectionnumber) + '/aeonix')
        download_local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(sectionnumber) + '/download')
        os.makedirs(sipp_local_path, exist_ok = True)
        os.makedirs(aeonix_local_path, exist_ok = True)
        os.makedirs(download_local_path, exist_ok = True)

        files = os.listdir(template_method)
        print(bcolors.INFO2 + '- copy all templates files to local directory ../' + sipp_local_path + bcolors.RESET)
        shutil.copytree(template_method + '/sipp', sipp_local_path, dirs_exist_ok=True)
        shutil.copytree(template_method + '/aeonix', aeonix_local_path, dirs_exist_ok=True)

        print(bcolors.INFO2 + '- parsing executable \'*.sh\' scripts' + bcolors.RESET)
        replace_string(sipp_local_path +'/register.sh','[servers]', serverdict['sipp_host'] + ' ' + serverdict['host'])
        replace_string(sipp_local_path +'/register.sh','[users]', str(int(capacity/sections)))
        replace_string(sipp_local_path +'/answer.sh','[servers]', serverdict['sipp_host'] + ' ' + serverdict['host'])
        replace_string(sipp_local_path +'/call.sh','[servers]', serverdict['sipp_host'] + ' ' + serverdict['host'])
        replace_string(sipp_local_path +'/blf.sh','[servers]', serverdict['sipp_host'] + ' ' + serverdict['host'])

        print(bcolors.INFO2 + '- creating sequantial \'*.csv\' files' + bcolors.RESET)
        with open(sipp_local_path +'/register.csv', 'w') as registerfile:
            registerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + capacity/sections)):
                registerfile.write(str(counter) +';[authentication username='+str(counter) +' password=Aeonix123@]\n')
            registerfile.close()
        
        with open(sipp_local_path +'/call_answer.csv', 'w') as callanswerfile:
            callanswerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + capacity/sections), 2):
                callanswerfile.write(str(counter) + ';' + str(counter+1) +';\n')
            callanswerfile.close()
        
        print(bcolors.INFO2 + '- creating \'load.info\' file' + bcolors.RESET)
        with open(sipp_local_path + '/load.info', 'w') as loadinfofile:
            loadinfofile.write(serverdict['section'] +' (out of ' + str(sections) + ')\n')
            loadinfofile.write('TOTAL USERS = ' + str(capacity) + '\n')
            loadinfofile.write('sipp host : ' + serverdict['sipp_host'] + ' --> aeonix host : ' + serverdict['host'] + '\n')
            loadinfofile.write('users from : ' + str(startuser) + ' to : ' + str(int(startuser + capacity/sections - 1)) + ' (' + str(int(capacity/sections)) + ' users)\n\n')
            loadinfofile.close()
        
        shutil.copyfile(sipp_local_path + '/load.info', aeonix_local_path + '/load.info')

        print(bcolors.INFO2 + '- setting \'cluster_disconnect.sh\' file' + bcolors.RESET)
        with open(aeonix_local_path + '/disconnect_server.sh', 'w', newline='\n') as disconnectfile:
            disconnectfile.write('#!/bin/sh\n\n')
            for server in range(1, sections + 1):
                if server == sectionnumber:
                    continue
                serverdict = get_section_info(server)
                disconnectfile.write ('sudo iptables -A OUTPUT -d ' + serverdict['host'] + ' -j DROP\n')
                disconnectfile.write ('sudo iptables -A INPUT -s ' + serverdict['host'] + ' -j DROP\n\n')
                loadinfofile.close()

        startuser = startuser + int(capacity/sections) 


def get_section_info(sectionnumber):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    SECTION = 'SERVER_' + str(sectionnumber) 
    host = config[SECTION]['host']
    user = config[SECTION]['user']
    password = config[SECTION]['password']
    sipp_host = config[SECTION]['sipp_host']
    sipp_user = config[SECTION]['sipp_user']
    sipp_password = config[SECTION]['sipp_password']
    serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
    return(serverdict)


def replace_string(filepath, replace, with_string):
    with open(filepath, 'r+') as f:
        replace_string = f.read().replace(replace, with_string)
    with open(filepath, 'w', newline='\n') as f:
        f.write(replace_string)
    f.close()


def execute (command, trace):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    remote_path = 'simulator/'
    err = 0
    reply=''
    if trace: print(bcolors.INFO +'configuration file contains ' + str(sections) + ' server(s) sections' + bcolors.RESET)

    if command == "check_cluster_status":
        edgeOption = webdriver.EdgeOptions()
        edgeOption.use_chromium = True
        edgeOption.add_experimental_option('excludeSwitches', ['enable-logging'])
        edgeOption.add_argument("--headless")
        #edgeOption.add_argument("--enable-logging")
        #edgeOption.add_argument("--log-level=3")
        edgeOption.add_argument('--ignore-ssl-errors=yes')
        edgeOption.add_argument('--ignore-certificate-errors')
        s=service.Service(r'bin\drivers\msedgedriver.exe')
        server_i = 0
        if sections >= 1:
            for server_i in range (1, int(sections)+1):
                server_dict = get_section_info(str(server_i))
                host = server_dict['host']
                username = server_dict['user'] 
                password = server_dict['password']
                driver = webdriver.ChromiumEdge(service=s, options=edgeOption)
                driver.refresh()
                driver.implicitly_wait(5)
                try:
                    driver.get('https://' + host + ':8443/aeonix')
                    break
                except: 
                    if trace: print(bcolors.FAIL + 'can\'t access via https://' + host + ':8443/aeonix - please check!' + bcolors.RESET)
                    if server_i < int(sections):
                        continue
                    else:
                        reply = 'error'
                        return(reply)
        else:
            return           # configfile.ini is probably empty

        driver.implicitly_wait(5)
        driver.find_element(By.ID, "loginForm:loginUserName").send_keys(username)
        driver.find_element(By.ID, "loginForm:password").send_keys(password)
        driver.find_element(By.ID, "loginForm:loginBtn").send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get('https://' + host + ':8443/aeonix/rs/system/cluster.jsf')

        clusterobj_titles = ['HOST', 'ADDR', 'EPS', 'IN', 'OUT', 'REC', 'ACC', 'LIC', 'TIME']
        clusterobj = {}

        if trace: print()
        idx = 0
        rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:clusterobj']/tbody/tr/td")
        for r in rwdata:
            idx += 1
            if idx == 2: 
                nested = r.text
                clusterobj[nested] = {}
            if idx >= 3 and idx < 11: clusterobj[nested][clusterobj_titles[idx-2]] = r.text
            if idx == 10: idx = 0
        if trace: print (str(int(len(rwdata)/10)) + ' server(s) environmnt (via https://' + host + ':8443/aeonix): ')
        clusterobj_df = pd.DataFrame.from_dict(clusterobj).T
        if trace: print(clusterobj_df)

        srv_stat_ok = driver.find_elements(By.XPATH, "//img[@title='Connection status: OK']")
        if trace: print (str(len(srv_stat_ok)) + ' server(s) are in \'Connection OK\' state' )
        if len(srv_stat_ok) != sections: reply = 'error'
        srv_stat_nc = driver.find_elements(By.XPATH, "//img[@title='Connection status: Not connected']")
        if trace: print (str(len(srv_stat_nc)) + ' server(s) are in \'Not Connected\' state' )
        if len(srv_stat_nc) != 0: reply = 'error'

        idx = 0
        rwdata = driver.find_elements(By.XPATH, "//*[@id='thePollingForm:totalEP']/tbody/tr/td")
        for r in rwdata:
            idx += 1
            if idx == 3:
                tot_eps = str(r.text)
                if trace: print('Total registered endpoints: ' + tot_eps)

        if sections == 1: return(reply) # no more data for 1 server environmnt so return

        if trace: print()
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
                nested = clusterIntegrityTable[idx]
                clusterIntegrityPanel[nested] = {}
                continue
            clusterIntegrityPanel[nested][clusterIntegrityTitles[i]] = clusterIntegrityTable[idx]
            i += 1
            if i >= 4: i = 0
        clusterIntegrityPanel_df = pd.DataFrame.from_dict(clusterIntegrityPanel).T
        if trace: print(clusterIntegrityPanel_df)
        #if trace: print(clusterIntegrityPanel)
        driver.close()
        driver.quit()
        return(reply)

   
    #
    for server in range(1, sections + 1):
        if command == "check_if_ready":
            if trace: print('\n' + bcolors.INFO + 'checking simulator SERVER_' + str(server) + ' environment:' + bcolors.RESET)
            host = server_command(server, 'aeonix', 'ipaddress_anx')
            if trace: print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- aeonix server', host, ' - communication check  : ') + bcolors.RESET, end='')
            check = server_command(server, 'aeonix', 'comm')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)

            if trace: print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- aeonix server', host, ' - version check        : ') + bcolors.RESET, end='')
            check = server_command(server, 'aeonix', 'version')
            result, err = (('failed', err+1) if check == 'error' else (check, err+0))
            if trace: print(result)

            if trace: print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- aeonix server', host, ' - operational check    : ') + bcolors.RESET, end='')
            check = server_command(server, 'aeonix', 'status')
            result, err = (('failed', err+1) if check == 'error' or check == 'stopped' else (check, err+0))
            if trace: print(result)
            
            host = server_command(server, 'aeonix', 'ipaddress_sipp')
            if trace: print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- sipp server', host, ' - communication check  : ') + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'comm')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)

            if trace: print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- sipp server', host, ' - running job(s) check : ') + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'jobs')
            #result, err = (('failed', err+1) if check == 'running' else ('passed', err+0))
            result, err = ((check, err+1) if check == 'running' else ('passed', err+0))
            if trace: print(result)
        
        elif command == 'upload':
            if trace: print(bcolors.INFO2 + '- upload all SERVER_' + str(server) + ' simulation files ' + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'upload')
            check = server_command(server, 'aeonix', 'upload')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)

        elif command == 'patch':
            if trace: print(bcolors.INFO2 + '- patched all SERVER_' + str(server) + ' files ' + bcolors.RESET, end='')
            #check = server_command(server, 'sipp', 'upload')
            check = server_command(server, 'aeonix', 'patch')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)

        elif command == 'terminate':
            if trace: print(bcolors.INFO2 + '- terminate all SERVER_' + str(server) + ' active simulators ' + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'terminate')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)
        
        elif command == 'clean':
            if trace: print(bcolors.INFO2 + '- clean all SERVER_' + str(server) + ' logs ' + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'clean')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)
        
        elif command == 'clean_zip':
            if trace: print(bcolors.INFO2 + '- clean all SERVER_' + str(server) + ' zip logs ' + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'clean')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)

        elif command == 'download':
            if trace: print(bcolors.INFO2 + '- download all SERVER_' + str(server) + ' logs ' + bcolors.RESET, end='')
            check = server_command(server, 'sipp', 'download')
            result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
            if trace: print(result)
    
    #return(err if err > 0 else 'passed')
    return(err)

# ----------------------------------------------------------------------------------------

def server_command(server, component, option):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    remote_path = 'simulator/'
    check = None
    err = 0
    #print(bcolors.INFO +'configuration file contains ' + str(sections) + ' server(s) sections' + bcolors.RESET)
    #for sectionnumber in range(1, sections + 1):
    SECTION = 'SERVER_' + str(server) 
    aeonix_host = config[SECTION]['host']
    aeonix_user = config[SECTION]['user']
    aeonix_password = config[SECTION]['password']
    sipp_host = config[SECTION]['sipp_host']
    sipp_user = config[SECTION]['sipp_user']
    sipp_password = config[SECTION]['sipp_password']
    serverdict = {'section':SECTION, 'aeonix_host': aeonix_host, 'aeonix_user': aeonix_user, 'aeonix_password':aeonix_password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
    #print(serverdict['section'], serverdict['aeonix_host'], serverdict['sipp_host'])

    if component in ["aeonix"]:
        host = aeonix_host
        user = aeonix_user
        password = aeonix_password
    elif component in ["sipp"]:
        host = sipp_host
        user = sipp_user
        password = sipp_password

    if option in ["comm"]:
        check = server_options(host, user, password, '', '', '')

    elif option in ["hostname"]:
        check = server_options(host, user, password, '', '', 'hostname')

    elif option in ["ipaddress"]:
        check = server_options(host, user, password, '', '', 'ipaddress')
    
    elif option in ["ipaddress_anx"]:
        check = aeonix_host

    elif option in ["ipaddress_sipp"]:
        check = sipp_host

    elif option in ["jobs"] and component == 'sipp':
        check = server_options(host, user, password, '', '', 'jobs')

    elif option in ["status"] and component == 'aeonix':
        check = server_options(host, user, password, '', '', 'status')

    elif option in ["version"] and component == 'aeonix':
        check = server_options(host, user, password, '', '', 'version')

    elif option in ["patch"] and component == 'aeonix':
        check = server_options(host, user, password, '', remote_path, 'patch')

    elif option in ["terminate"] and component == 'sipp':
        check = server_options(host, user, password, '', remote_path, 'terminate')

    elif option in ["clean"] and component == 'sipp':
        check = server_options(host, user, password, '', remote_path, 'clean')

    elif option in ["clean_zip"] and component == 'sipp':
        check = server_options(host, user, password, '', remote_path, 'clean_zip')

    elif option in ["upload"]: # and component == 'sipp':
        try:
            with open("temp", "r") as tempfile:
                tmp_list = tempfile.read().split(',')
                tempfile.close()
            capacity = tmp_list[1] #total number of users
            method = tmp_list[3]   #method
        except:
            return('error')
        if component == 'sipp':
            local_path =  local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(server) + '/sipp')
        elif component == 'aeonix':
            local_path = local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(server) + '/aeonix')
        check = server_options(host, user, password, local_path, remote_path, 'upload')
    
    elif option in ["download"] and component == 'sipp':
        try:
            with open("temp", "r") as tempfile:
                tmp_list = tempfile.read().split(',')
                tempfile.close()
            capacity = tmp_list[1] #total number of users
            method = tmp_list[3]   #method
        except:
            return('error')
        local_path =  local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(server))
        check = server_options(host, user, password, local_path, remote_path, 'pack')
        check = server_options(host, user, password, local_path, remote_path, 'download')

    return(check)


def server_options(host, user, password, local_path, remote_path, option):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_zip = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        transport = paramiko.Transport(host, 22)
        transport.connect(username=user,password=password)
        client.connect(hostname = host, username=user,password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except:
        return('error')
        
    if option in ['upload']:
        try:
            sftp.chdir(remote_path)
            #ssh_command = 'chmod +x *.sh'
            ssh_command = 'cd ' + remote_path + '; chmod +x *.sh'
            stdin,stdout,stderr = client.exec_command(ssh_command)
        except IOError:
            sftp.mkdir(remote_path)
            sftp.chdir(remote_path)
        
        files = os.listdir(local_path)    
        for filename in files:
            sftp.put(local_path + '/' + filename, filename)
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; rm -rf *.zip'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'echo ' + timestamp + ' created and uploaded' + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)

    elif option in ['patch']:
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; ./patch.sh &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'echo ' + timestamp + ' server was patched  ' + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response)

    elif option in ['hostname']:
        ssh_command = 'hostname'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response)

    elif option in ['ipaddress']:
        ssh_command = 'hostname -I'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response)

    elif option in ['jobs']:
        ssh_command = 'pgrep sipp'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        if response != '':
            return('running')
        elif response == '':
            return('stopped')

    elif option in ['terminate']:
        ssh_command = 'killall sipp'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'cd ' + remote_path
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'echo ' + timestamp + ' terminate all running sipp jobs' + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        return None

    elif option in ['pack']:
        ssh_command = 'cd ' + remote_path + '; zip -r ../sim_`hostname`_' + timestamp_zip + '_logs.zip * &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'echo ' + timestamp + ' pack log files to zip' + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)

    elif option in ['download']:
        ssh_command = 'cd ~'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        file_list = sftp.listdir()
        for item in file_list:
            if 'zip' in item:
                sftp.get(item, local_path + '/download/' + item)
                ssh_command = 'echo ' + timestamp + ' download file: ' + item + '\r >> ' + remote_path + 'load.info'
                stdin,stdout,stderr = client.exec_command(ssh_command)

    elif option in ['clean']:
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; ./clean_logs.sh &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'echo ' + timestamp + ' clean up the log files ' + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        return None

    elif option in ['clean_zip']:
        ssh_command = 'cd ~' + remote_path + '; rm -rf *.zip'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        ssh_command = 'echo ' + timestamp + ' clean up the zip log files ' + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        return None

    elif option in['version']:
        ssh_command ="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response if response !='' else 'error')

    elif option in['status']:
        ssh_command ='sudo service aeonix status'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        running = response.count('running')
        stopped = response.count('stopped')
        return('running' if running == 6 and stopped == 0 else 'stopped' if running == 0 and stopped == 6 else 'error')

    else:
        return('open')
    sftp.close()
    transport.close()
    client.close()

remote_path = 'simulator/'
#results = server_command('3','sipp','clean')
#print(results)