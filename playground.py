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

#checkservers()
printsections()

"""
import socket
import time

ip = "10.1.16.55"
port = 22
retry = 2
delay = 5
timeout = 3

def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
    except:
            return False
    finally:
            s.close()

def checkHost(ip, port):
    ipup = False
    for i in range(retry):
            if isOpen(ip, port):
                    ipup = True
                    break
            else:
                    time.sleep(delay)
    return ipup

if checkHost(ip, port):
        print (ip + " is UP")
else:
    print (ip + " not responding")

"""