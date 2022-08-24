import os
import ipaddress, datetime
from configobj import ConfigObj
import subprocess
import platform
import paramiko

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
    WARNING2 =  '\033[93m      '  #YELLOW
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
    
    prompt = bcolors.MENUV + f"""
    Aeonix Load Gen environment configuration menu
    1 -- add a new server
    2 -- edit a server
    3 -- delete a server
    4 -- configuraion overview
    5 -- initialize a configuration file (if not exist)
    6 -- clear the configuration file content
    7 -- go back
    note that you can use the {', '.join(fileoptions)} option(s) only\n""" + bcolors.PROMPTV + """
    Enter your choice [1-6]: """ + bcolors.RESET
    
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
        overviewconfigfile()
    elif choice in ["5"]:
        if 'initialize' in fileoptions: initconfigfile()
    elif choice in ["6"]:
        if 'clear' in fileoptions: clearconfigfile()
    elif choice in ["7"]: return()
    
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
    
