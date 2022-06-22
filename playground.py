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

def ssh_ip(host, user, password, cmdx):
    import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        _stdin, _stdout,_stderr = client.exec_command(cmdx)
        client.close()
        return True
    except Exception:
        return False
    

def checkservers():
    import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmdx='pwd'
    serverlist =[]
    config = ConfigObj('configfile.ini')
    for servernumber in range(len(config.sections)):
        host = config['SERVER_' + str(servernumber + 1)]['host']
        user = config['SERVER_' + str(servernumber + 1)]['user']
        password = config['SERVER_' + str(servernumber + 1)]['password']
        serverlist.append(str(host))
        #print(serverlist)
        if ping_ip(host):
            print(f"      host: {host:15} ping ok")
        else:
            print(f"      host: {host:15} ping unreachable")

        if ssh_ip(host, user, password, cmdx):
            print(' '*27, 'ssh established')
        else:
            print(' '*27, 'ssh timeout error')



checkservers()

