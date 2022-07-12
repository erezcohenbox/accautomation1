import os
import ipaddress
from configobj import ConfigObj
import subprocess
import platform
import paramiko

class bcolors:
    OK = '\033[92m    > '      #GREEN
    OKV = '\033[92m'           #GREEN
    INFO = '\033[96m    > '    #LIGHT BLUE
    WARNING = '\033[93m    > ' #YELLOW
    FAIL = '\033[91m    > '    #RED
    FAILV = '\033[91m'         #RED
    RESET = '\033[0m'          #RESET
    CLS = '\033[2J'            #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

def checkconfigstatus():
    configfileoptions = ''
    try:
        with open('configfile.ini') as configfile:
            filesize = os.path.getsize('configfile.ini')
            if filesize > 0:
                configfileoptions = ['add','edit','delete','clear']
            else:
                configfileoptions = ['add']
    except FileNotFoundError:
        configfileoptions = ['initialize']
    
    return(configfileoptions)





def setconfigfile():
    fileoptions = checkconfigstatus()
    
    prompt = f"""
    Aeonix Contact Center environment configuration Menu
    1 -- add a new server
    2 -- edit a server
    3 -- delete a server
    4 -- initialize a configuration file (if not exist)
    5 -- clear the configuration file content
    6 -- go back
    note that you can use the {', '.join(fileoptions)} option(s) only\n
    Enter your choice [1-6]: """ 
    
    choice = input(prompt)
    
    if choice in ["1"]:
        if 'add' in fileoptions: 
            addsection()
    elif choice in ["2"]:
        if 'edit' in fileoptions:
            editsection()
    elif choice in ["3"]:
        if 'delete' in fileoptions:
            deletesection()
    elif choice in ["4"]:
        if 'initialize' in fileoptions: initconfigfile()
    elif choice in ["5"]:
        if 'clear' in fileoptions: clearconfigfile()
    elif choice in ["6"]: return()
    
    setconfigfile()


def countsections():
    config = ConfigObj('configfile.ini')
    return(len(config.sections))

def addsection():
    config = ConfigObj('configfile.ini')
    servernumber = len(config.sections) + 1
    print(bcolors.WARNING + 'adding [SERVER_' + str(servernumber) +'] section' + bcolors.RESET)
    
    try:
        host = input(bcolors.INFO + 'host = '+ bcolors.RESET )
        ip = ipaddress.ip_address(host)
        #print(f'{ip} is correct. Version: IPv{ip.version}')
    except ValueError:
        print(bcolors.FAIL + 'invalid ip address...' + bcolors.RESET)
        return()

    user = input(bcolors.INFO + 'user = '+ bcolors.RESET)
    if " " in user or user =="":
        print(bcolors.FAIL + 'invalid user...' + bcolors.RESET)
        return()
    
    password = input(bcolors.INFO + 'password = '+ bcolors.RESET)
    if " " in password or password =="":
        print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
        return()

    try:
        sipp_host = input(bcolors.INFO + 'sipp_host = '+ bcolors.RESET )
        ip = ipaddress.ip_address(sipp_host)
        #print(f'{ip} is correct. Version: IPv{ip.version}')
    except ValueError:
        print(bcolors.FAIL + 'invalid ip address...' + bcolors.RESET)
        return()

    sipp_user = input(bcolors.INFO + 'sipp_user = '+ bcolors.RESET)
    if " " in sipp_user or sipp_user =="":
        print(bcolors.FAIL + 'invalid user...' + bcolors.RESET)
        return()
    
    sipp_password = input(bcolors.INFO + 'sipp_password = '+ bcolors.RESET)
    if " " in sipp_password or sipp_password =="":
        print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
        return()
    
    choice = input(bcolors.WARNING + 'add server to configuration? [YES] ' + bcolors.RESET)
    if choice in ["YES"]:
        
        config = ConfigObj('configfile.ini')
        config['SERVER_' + str(servernumber)] = {}
        config['SERVER_' + str(servernumber)]['host'] = host
        config['SERVER_' + str(servernumber)]['user'] = user
        config['SERVER_' + str(servernumber)]['password'] = password
        config['SERVER_' + str(servernumber)]['sipp_host'] = sipp_host
        config['SERVER_' + str(servernumber)]['sipp_user'] = sipp_user
        config['SERVER_' + str(servernumber)]['sipp_password'] = sipp_password
        config.write()
        print(bcolors.OK + 'done.' + bcolors.RESET)


def editsection():
    config = ConfigObj('configfile.ini')
    print(bcolors.WARNING + 'which one of the servers you wish to edit?' + bcolors.RESET)
    print(bcolors.INFO + ', '.join(config.sections) + bcolors.RESET)
    servernumber = input(bcolors.WARNING + 'please type the SERVER number: ' + bcolors.RESET)
   
    try:
        host = input(bcolors.INFO + 'host = '+ bcolors.RESET )
        ip = ipaddress.ip_address(host)
        #print(f'{ip} is correct. Version: IPv{ip.version}')
    except ValueError:
        print(bcolors.FAIL + 'invalid ip address...' + bcolors.RESET)
        return()

    user = input(bcolors.INFO + 'user = '+ bcolors.RESET)
    if " " in user or user =="":
        print(bcolors.FAIL + 'invalid user...' + bcolors.RESET)
        return()
    
    password = input(bcolors.INFO + 'password = '+ bcolors.RESET)
    if " " in password or password =="":
        print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
        return()

    try:
        sipp_host = input(bcolors.INFO + 'sipp_host = '+ bcolors.RESET )
        ip = ipaddress.ip_address(sipp_host)
        #print(f'{ip} is correct. Version: IPv{ip.version}')
    except ValueError:
        print(bcolors.FAIL + 'invalid ip address...' + bcolors.RESET)
        return()

    sipp_user = input(bcolors.INFO + 'sipp_user = '+ bcolors.RESET)
    if " " in sipp_user or sipp_user =="":
        print(bcolors.FAIL + 'invalid user...' + bcolors.RESET)
        return()
    
    sipp_password = input(bcolors.INFO + 'password = '+ bcolors.RESET)
    if " " in sipp_password or sipp_password =="":
        print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
        return()

    choice = input(bcolors.WARNING + 'edit the configuration? [YES] ' + bcolors.RESET)
    if choice in ["YES"]:
        
        config = ConfigObj('configfile.ini')
        config['SERVER_' + str(servernumber)] = {}
        config['SERVER_' + str(servernumber)]['host'] = host
        config['SERVER_' + str(servernumber)]['user'] = user
        config['SERVER_' + str(servernumber)]['password'] = password
        config['SERVER_' + str(servernumber)]['sipp_host'] = sipp_host
        config['SERVER_' + str(servernumber)]['sipp_user'] = sipp_user
        config['SERVER_' + str(servernumber)]['sipp_password'] = sipp_password
        config.write()
        print(bcolors.OK + 'done.' + bcolors.RESET)    


def deletesection():
    config = ConfigObj('configfile.ini')
    print(bcolors.WARNING + 'which one of the servers you wish to delete?' + bcolors.RESET)
    print(bcolors.INFO + ', '.join(config.sections) + bcolors.RESET)
    servernumber = input(bcolors.WARNING + 'please type the SERVER number: ' + bcolors.RESET)
    try:
        config.sections.remove('SERVER_'  + str(servernumber))
        config.write()
        print(bcolors.OK + 'done.' + bcolors.RESET)
        
        #now, reorder the server sections from 1 --> and on...
        reorderconfigfile()

    except ValueError:
        print(bcolors.FAIL + 'such server does not exist...' + bcolors.RESET)
        return()


def initconfigfile():
    print(bcolors.FAIL + 'initializing the configuration file...' + bcolors.RESET)
    with open('configfile.ini', 'w') as configfile:
        pass
    print(bcolors.FAIL + 'please set the environment.' + bcolors.RESET)


def clearconfigfile():
    print(bcolors.WARNING + 'this will clear the configuration file' + bcolors.RESET)
    choice = input(bcolors.WARNING + 'are you sure? [YES] ' + bcolors.RESET)
    if choice in ["YES"]:
        with open('configfile.ini', 'w') as configfile:
            pass
        print(bcolors.OK + 'done.' + bcolors.RESET)
        print(bcolors.FAIL + 'please set the environment.' + bcolors.RESET)
    else:
        return()

def reorderconfigfile():
    config = ConfigObj('configfile.ini')
    try:
        serverlist = config.sections
        i = 1
        for server in serverlist:
            config.rename(server, 'SERVER_' + str(i))
            i += 1
        config.write()
    except KeyError:
        print(bcolors.WARNING + 'manual reorder of \'configfile.ini\' file is needed' + bcolors.RESET)

def overviewconfigfile():
    config = ConfigObj('configfile.ini')
    if (len(config.sections)) >= 1:
        configfile = open('configfile.ini',"r")
        configfilelines = configfile.readlines()
        count = 0
        print(bcolors.INFO +'configuration file contains ' + str(len(config.sections)) + ' server(s) sections' + bcolors.RESET)
        for line in configfilelines:
            count += 1
            if line[0] =='[':
                print('      ' + '-' * 60)
            print("      {}".format(line.strip()))
        configfile.close()
        print('      ' + '-' * 60)
        reorderconfigfile()
    else:
        print(bcolors.FAIL + 'configuration file is empty.' + bcolors.RESET)
        print(bcolors.FAIL + 'please set the environment.' + bcolors.RESET)
    

#def serverelements():
#    config = ConfigObj('configfile.ini')
#    serverlist =[]
#    for servernumber in range(len(config.sections)):
#       host = config['SERVER_' + str(servernumber + 1)]['host']
#        user = config['SERVER_' + str(servernumber + 1)]['user']
#        password = config['SERVER_' + str(servernumber + 1)]['password']
#        serverlist.append(str(host))

def checkservers():
    cmdx='pwd'
    element ={}
    config = ConfigObj('configfile.ini')
    print()
    print(bcolors.INFO + 'configuration contains ' + str(len(config.sections)) + ' server(s) sections' + bcolors.RESET)
    for sectionnumber in range(1, len(config.sections) + 1):
        print('      ' + '-' * 60)
        element = serverelements(sectionnumber)
        SECTION = element['section']
        host =  element['host']
        user =  element['user']
        password =  element['password']
        sipp_host =  element['sipp_host']
        sipp_user =  element['sipp_user']
        sipp_password =  element['sipp_password']

        print('      [' + SECTION + ']')
        print('      host = ' + host)
        print(bcolors.INFO + 'pinging...', end='')
        if ping_ip(host):
            print(bcolors.OKV + '           ping ok' + bcolors.RESET)
        else:
            print(bcolors.FAILV + '           unreachable' + bcolors.RESET)

        print(bcolors.INFO + 'remote ssh access... ', end='')
        if ssh_ip(host, user, password, cmdx):
            print(bcolors.OKV + 'established' + bcolors.RESET)
            cmdv="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
            anxver = ssh_ip2(host, user, password, cmdv)
            #print(bcolors.INFO + 'Aeonix version ' + str(anxver) + bcolors.RESET)
            cmdx='sudo service aeonix status'
            anxlist = []
            countrunning =''
            anxlist = ssh_ip2(host, user, password, cmdx)
            countrunning = anxlist.count('running')
            countstopped = anxlist.count('stopped')
            if countrunning == 6:
                print(bcolors.INFO + 'aeonix server ' + str(anxver) + ' is running'+ bcolors.RESET)
            elif countstopped <=6 and countstopped > 0:
                print(bcolors.WARNING + 'aeonix server ' + str(anxver) + ' is not running properly.'+ bcolors.RESET)
                print(bcolors.WARNING + str(countstopped) + ' out of it\'s 6 services are not running, please check...'+ bcolors.RESET)
            else:
                print(bcolors.WARNING + 'aeonix server is not installed.'+ bcolors.RESET)

            cmdv="sudo cat /opt/acc/bin/version |tr -c -d 0-9."
            accver = ssh_ip2(host, user, password, cmdv)
            #print(bcolors.INFO + 'ACC version ' + str(anxver) + bcolors.RESET)
            cmdx='sudo service accd status'
            acclist = []
            countrunning =''
            acclist = ssh_ip2(host, user, password, cmdx)
            countrunning = acclist.count('running')
            countstopped = acclist.count('stopped')
            if countrunning == 2:
                print(bcolors.INFO + 'acc server ' + str(accver) + ' is running'+ bcolors.RESET)
            elif countstopped <=2 and countstopped > 0:
                print(bcolors.WARNING + 'acc server ' + str(accver) + ' is not running properly.'+ bcolors.RESET)
                print(bcolors.WARNING + str(countstopped) + ' out of it\'s 2 services are not running, please check...'+ bcolors.RESET)
            else:
                print(bcolors.WARNING + 'acc server is not installed.'+ bcolors.RESET)

        else:
            print(bcolors.FAILV + 'timeout' + bcolors.RESET)

        print('      sipp_host = ' + sipp_host)
        print(bcolors.INFO + 'pinging...', end='')
        if ping_ip(sipp_host):
            print(bcolors.OKV + '           ping ok' + bcolors.RESET)
        else:
            print(bcolors.FAILV + '           unreachable' + bcolors.RESET)

        print(bcolors.INFO + 'remote ssh access... ', end='')
        if ssh_ip(sipp_host, sipp_user, sipp_password, cmdx):
            print(bcolors.OKV + 'established' + bcolors.RESET)
        else:
            print(bcolors.FAILV + 'timeout' + bcolors.RESET)    

        #keep this section for open port scaning
        #print(bcolors.INFO + 'check port 3308...   ', end ='')
        #if socket_ip(host, 3308):
        #    print('port is open')
        #else:
        #    print('port is not open')
        #print()
    print('      ' + '-' * 60)

def serverelements(sectionnumber):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    SECTION = 'SERVER_' + str(sectionnumber) 
    host = config[SECTION]['host']
    user = config[SECTION]['user']
    password = config[SECTION]['password']
    sipp_host = config[SECTION]['sipp_host']
    sipp_user = config[SECTION]['sipp_user']
    sipp_password = config[SECTION]['sipp_password']
    serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
    #print(serverdict['section'])
    return(serverdict)


def ping_ip(host):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', host ), shell=True, universal_newlines=True)
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

def ssh_ip2(host, user, password, cmdx):
    import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        _stdin, stdout,_stderr = client.exec_command(cmdx)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        client.close()
        return (response)
    except Exception:
        return False

def socket_ip(host, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host,port))
    if result == 0:
        sock.close()
        return True
    else:
        return False
    