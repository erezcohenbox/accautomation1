import configparser
import os
import ipaddress



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
    #print(fileoptions)
    
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
            sectioncount=readsections()
            addsection(sectioncount)
    elif choice in ["2"]:
        if 'edit' in fileoptions:
            print('you can edit')
    elif choice in ["3"]:
        if 'delete' in fileoptions:
            deletesection()
    elif choice in ["4"]:
        if 'initialize' in fileoptions: initconfigfile()
    elif choice in ["5"]:
        if 'clear' in fileoptions: clearconfigfile()
    elif choice in ["6"]: return()
    
    setconfigfile()


def readsections():
    config = configparser.ConfigParser()
    config.read('configfile.ini')
    return(len(config.sections()))

def addsection(sectioncount):
    sectioncount += 1
    print(bcolors.WARNING + 'adding [SERVICE_' + str(sectioncount) +'] section' + bcolors.RESET)
    #print(sectioncount)
    
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
        config = configparser.ConfigParser()
        with open("configfile.ini") as configfile:
            config.read_file(configfile)
        config['SERVER_' + str(sectioncount)] = {'host': host,
                        'user': username,
                        'password': password}
        with open("configfile.ini", "w") as configfile:
            config.write(configfile)     
            print(bcolors.INFO + 'done.' + bcolors.RESET)


def deletesection():
    config = configparser.ConfigParser()
    with open('configfile.ini', 'r') as configfile:
        config.readfp(configfile)
    print(bcolors.WARNING + 'which one of the servers you wish to delete?' + bcolors.RESET)
    print(bcolors.INFO + ', '.join(config.sections()) + bcolors.RESET)
    choice = input(bcolors.WARNING + 'please type the SERVER number: ' + bcolors.RESET)
    config.remove_section('SERVER_' + str(choice))
    #print(config.sections())
    with open('configfile.ini', 'w') as configfile:
        config.write(configfile)
    #with open('configfile.ini', 'r') as configfile:
    #   print(config.read())


def initconfigfile():
    config = configparser.ConfigParser()
    print(bcolors.FAIL + 'initializing the configuration file...' + bcolors.RESET)
    with open('configfile.ini', 'w') as configfile:
        config.write(configfile)
    print(bcolors.FAIL + 'please configure the environment.' + bcolors.RESET)


def clearconfigfile():
    config = configparser.ConfigParser()
    print(bcolors.WARNING + 'this will clear the configuration file' + bcolors.RESET)
    choice = input(bcolors.WARNING + 'are you sure? [YES] ' + bcolors.RESET)
    if choice in ["YES"]:
        with open('configfile.ini', 'w') as configfile:
            config.write(configfile)
        print(bcolors.INFO + 'done.' + bcolors.RESET)
        print(bcolors.FAIL + 'please configure the environment.' + bcolors.RESET)
    else:
        return()




def overviewconfigfile():
    config = configparser.ConfigParser()
    try:
        with open('configfile.ini') as configfile:
            filesize = os.path.getsize('configfile.ini')
            if filesize > 0:
                config.read ('configfile.ini')
                for sect in config.sections():
                    print('    [' + sect + ']')
                    for k,v in config.items(sect):
                        print('     {} = {}'.format(k,v))
                print()
            else:
                print(bcolors.FAIL + 'configuration file is empty.' + bcolors.RESET)
                print(bcolors.FAIL + 'please configure the environment.' + bcolors.RESET)
    except FileNotFoundError:
        initconfigfile()



#def setconfigfile():
#    config = configparser.ConfigParser()
#    config.read ('configfile.ini')
#    print(config.sections())

