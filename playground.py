from configobj import ConfigObj
import os
import ipaddress
import paramiko

import platform
import subprocess



def printsections():
    config = ConfigObj('configfile.ini')
    print(config['SERVER_1'])
    print(config['SERVER_1']['host'])
    print(config['SERVER_1']['host'] == '1.1.1.1')
    #host = config['SERVER_1']['host'] 




    

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

def serverelements(sectionnumber):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    SECTION = 'SERVER_' + str(sectionnumber) 
    host = config[SECTION]['host']
    user = config[SECTION]['user']
    password = config[SECTION]['password']
    serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password}
    #print(serverdict['section'])
    return(serverdict)


#serverelements(1)
#print(serverelements(1)['host'])
'''
config = ConfigObj('configfile.ini')
print()
for sectionnumber in range(1, len(config.sections)):
    serverelements(1)
    SECTION = serverelements(sectionnumber['section'])
    host = serverelements(sectionnumber['host'])
    user = serverelements(sectionnumber['user'])
    password = serverelements(sectionnumber['password'])
    print('    [' + SECTION + ']')
    print('    host = ' + host)
    print('    host = ' + user)
    print('    host = ' + password)
'''


def ssh_upload(host, user, password, cmdx):
    import paramiko
    #import os
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    transport = paramiko.Transport(host, 22)
    transport.connect(username=user,password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    #stdin,stdout,stderr = client.exec_command(cmdx)
    
    sftp.put(r"C:\temp\tcmd1000x64.exe","/home/aeonixadmin/tcmd1000x64.exe")
    sftp.close()
    transport.close()
   

ssh_upload('10.1.16.55','aeonixadmin','anx', 'pwd')
#checkservers()
#printsections()

