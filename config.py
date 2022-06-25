import os
import ipaddress
from configobj import ConfigObj
import subprocess
import platform
import paramiko

class bcolors:
    OK = '\033[92m    > '      #GREEN
    INFO = '\033[96m    > '    #LIGHT BLUE
    WARNING = '\033[93m    > ' #YELLOW
    FAIL = '\033[91m    > '    #RED
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
    print(bcolors.WARNING + 'adding [SERVICE_' + str(servernumber) +'] section' + bcolors.RESET)
    
    try:
        host = input(bcolors.INFO + 'host = '+ bcolors.RESET )
        ip = ipaddress.ip_address(host)
        #print(f'{ip} is correct. Version: IPv{ip.version}')
    except ValueError:
        print(bcolors.FAIL + 'invalid ip address...' + bcolors.RESET)
        return()

    username = input(bcolors.INFO + 'username = '+ bcolors.RESET)
    if " " in username or username =="":
        print(bcolors.FAIL + 'invalid username...' + bcolors.RESET)
        return()
    
    password = input(bcolors.INFO + 'password = '+ bcolors.RESET)
    if " " in password or password =="":
        print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
        return()
    
    choice = input(bcolors.WARNING + 'add server to configuration? [YES] ' + bcolors.RESET)
    if choice in ["YES"]:
        
        config = ConfigObj('configfile.ini')
        config['SERVER_' + str(servernumber)] = {}
        config['SERVER_' + str(servernumber)]['host'] = host
        config['SERVER_' + str(servernumber)]['user'] = username
        config['SERVER_' + str(servernumber)]['password'] = password
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

    username = input(bcolors.INFO + 'username = '+ bcolors.RESET)
    if " " in username or username =="":
        print(bcolors.FAIL + 'invalid username...' + bcolors.RESET)
        return()
    
    password = input(bcolors.INFO + 'password = '+ bcolors.RESET)
    if " " in password or password =="":
        print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
        return()
    
    choice = input(bcolors.WARNING + 'edit the configuration? [YES] ' + bcolors.RESET)
    if choice in ["YES"]:
        
        config = ConfigObj('configfile.ini')
        config['SERVER_' + str(servernumber)] = {}
        config['SERVER_' + str(servernumber)]['host'] = host
        config['SERVER_' + str(servernumber)]['user'] = username
        config['SERVER_' + str(servernumber)]['password'] = password
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
        #print ('      '+ '-' * 20)
        for line in configfilelines:
            count += 1
            if line[0] =='[':
                print()
            print("      {}".format(line.strip()))
        print ()
        configfile.close()
        print(bcolors.INFO +'configuration file contains ' + str(len(config.sections)) + ' server(s)' + bcolors.RESET)
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
    print(bcolors.INFO + 'configuration contains ' + str(len(config.sections)) + ' server(s) ' + bcolors.RESET)
    print()
    for sectionnumber in range(1, len(config.sections) + 1):
        element = serverelements(sectionnumber)
        SECTION = element['section']
        host =  element['host']
        user =  element['user']
        password =  element['password']
        print('    [' + SECTION + ']')
        print('    host = ' + host)
        print('    user = ' + user)
        print('    password = ' + password)
        
        print(bcolors.INFO + 'pinging host...      ', end ='')
        if ping_ip(host):
            print('ping ok')
        else:
            print('unreachable')
  
        print(bcolors.INFO + 'remote ssh access... ', end ='')
        if ssh_ip(host, user, password, cmdx):
            print('established')
        else:
            print('timeout error')
        #keep this section for open port scaning
        #print(bcolors.INFO + 'check port 3308...   ', end ='')
        #if socket_ip(host, 3308):
        #    print('port is open')
        #else:
        #    print('port is not open')
        print(bcolors.RESET)
    

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
    #import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        _stdin, _stdout,_stderr = client.exec_command(cmdx)
        client.close()
        return True
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
    