#import configparser
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
    #config = configparser.ConfigParser()
    try:
        with open('configfile.ini') as configfile:
            filesize = os.path.getsize('configfile.ini')
            if filesize > 0:
                #file exist and have some settings
                # so Add, Edit, Delete and Clear functions can be used
                configfileoptions = ['add','edit','delete','clear']
            else:
                #file exist with empty settings
                # so Add is the only function that can be used
                configfileoptions = ['add']
    except FileNotFoundError:
        #file does not exist
        #so New file Initialization is the only function that can be used 
        configfileoptions = ['initialize']
    
    return(configfileoptions)





def setconfigfile():
    #https://docs.python.org/3/library/configparser.html
    #config = configparser.ConfigParser()
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
    #sectioncount = len(config.sections)
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
    

def checkservers():
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmdx='pwd'
    serverlist =[]
    config = ConfigObj('configfile.ini')
    print()
    for servernumber in range(len(config.sections)):
        host = config['SERVER_' + str(servernumber + 1)]['host']
        user = config['SERVER_' + str(servernumber + 1)]['user']
        password = config['SERVER_' + str(servernumber + 1)]['password']
        serverlist.append(str(host))
        #print(serverlist)
        print('    [SERVER_' + str(servernumber + 1) + ']')
        print('    host = ' + config['SERVER_' + str(servernumber + 1)]['host'])
        print('    user = ' + config['SERVER_' + str(servernumber + 1)]['user'])
        print('    password = ' + config['SERVER_' + str(servernumber + 1)]['password'])

        if ping_ip(host):
            bcolors.FAIL
            print(bcolors.OK + 'pinging host...  ping ok' + bcolors.RESET )
        else:
            print(bcolors.FAIL + 'pinging host...  ping unreachable' + bcolors.RESET )
        
        if ssh_ip(host, user, password, cmdx):
            print(bcolors.OK +   'remote access... ssh established' + bcolors.RESET)
        else:
            print(bcolors.FAIL + 'remote access... ssh timeout error' + bcolors.RESET)
        
        print()

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