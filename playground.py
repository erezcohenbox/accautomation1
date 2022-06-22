from configobj import ConfigObj
import os
import ipaddress
import paramiko

import platform
import subprocess



def ping (host):
    config = ConfigObj('configfile.ini')
    print(config['SERVER_1'])
    print(config['SERVER_1']['host'])
    print(config['SERVER_1']['host'] == '1.1.1.1')
    #host = config['SERVER_1']['host'] 

    param = '-n' if platform.system().lower()=='windows' else '-c'
    response = os.system('ping ' + param + ' 1 ' + config['SERVER_1']['host'])
    if response == 0:
       print('network active')
    else:
       print('network error')


def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', current_ip_address ), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
            return False

def checkservers():
    import paramiko

    serverlist =[]
    config = ConfigObj('configfile.ini')
    for servernumber in range(len(config.sections)):
        host = config['SERVER_' + str(servernumber + 1)]['host']
        serverlist.append(str(host))
    print(serverlist)

    for each in serverlist:
        #user = config['SERVER_' + str(servernumber + 1)]['user']
        #password = config['SERVER_' + str(servernumber + 1)]['password']
        
        user = config['SERVER_1']['user']
        password = config['SERVER_1']['password']
        #print(user,password)
        if ping_ip(each):
            print(f"      host: {each:15} is up")
        else:
            print(f"      host: {each:15} is unreachable")
    
    

        #command = "echo"
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(each, username=user, password=password)
        _stdin, _stdout,_stderr = client.exec_command("")
        print(_stdout.read().decode())
        client.close()

checkservers()

