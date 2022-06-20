import configparser
import os
import ipaddress
from configobj import ConfigObj


class bcolors:
    OK = '\033[92m    > '      #GREEN
    INFO = '\033[95m    > '    #PURPLE
    WARNING = '\033[93m    > ' #YELLOW
    FAIL = '\033[91m    > '    #RED
    RESET = '\033[0m'          #RESET
    CLS = '\033[2J'            #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

def checkconfigstatus():
    configfileoptions = ''
    config = configparser.ConfigParser()
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
    config = configparser.ConfigParser()
    fileoptions = checkconfigstatus()
    
    prompt = f"""
    Aeonix Contact Center environment configuration Menu
    1 -- add a new server
    2 -- edit a server
    3 -- delete a server
    4 -- initialize a configuration file (if not exist)
    5 -- clear the configuration file content
    6 -- go back
    note that you can use the: {', '.join(fileoptions)} option(s) only\n
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
    sectioncount = len(config.sections)
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
        
        #servernumber = len(config.sections)
        #sectionlist = ', '.join(config.sections)
        #for servers in sectionlist:

        
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




def overviewconfigfile():
    config = ConfigObj('configfile.ini')
    if (len(config.sections)) >= 1:
        print(bcolors.INFO +'configuration file is not empty.' + bcolors.RESET)
        config.get
    else:
        print(bcolors.FAIL + 'configuration file is empty.' + bcolors.RESET)
        print(bcolors.FAIL + 'please set the environment.' + bcolors.RESET)
    
