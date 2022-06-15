import configparser
import os

class bcolors:
    OK = '\033[92m'      #GREEN
    INFO = '\033[95m'    #PURPLE
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m'    #RED
    RESET = '\033[0m'    #RESET
    CLS = '\033[2J'      #CLEAR SCREEN
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
                configfileoptions = ['A','E','D','C']
            else:
                #file exist with empty settings
                # so Add is the only function that can be used
                configfileoptions = ['A']
    except FileNotFoundError:
        #file does not exist
        #so New file Creation is the only function that can be used 
        configfileoptions = ['N']
    
    return(configfileoptions)





def setconfigfile():
    #https://docs.python.org/3/library/configparser.html
    config = configparser.ConfigParser()
    fileoptions = checkconfigstatus()
    print(fileoptions)

    prompt = """
    Aeonix Contact Center environment configuration Menu
    1 -- add a new server
    2 -- edit a server
    3 -- delete a server
    4 -- create a configuration file (if not exist)
    5 -- clear the configuration file
    6 -- go back\n
    Enter your choice [1-6]: """
    
    choice = input(prompt)
    
    if choice in ["1"]:
        print('option 1 selected')
        if 'A' in fileoptions:
            print('you can add')
        else:
            print('you can NOT add')
        setconfigfile()
    elif choice in ["2"]:
        print('option 2 selected')
        if 'E' in fileoptions:
            print('you can edit')
        else:
            print('you can NOT edit')            
        setconfigfile()
    elif choice in ["3"]:
        print('option 3 selected')
        if 'D' in fileoptions:
            print('you can delete')
        else:
            print('you can NOT delete')   
        setconfigfile()
    elif choice in ["4"]:
        print('option 4 selected')
        if 'N' in fileoptions:
            print('you can create new config file')
            createconfigfile()
        else:
            print('you can NOT recreate the config file')
        setconfigfile() 
    elif choice in ["5"]:
        print('option 5 selected')
        if 'C' in fileoptions:
            print('you can clear the config file')
            clearconfigfile()
        else:
            print('you can NOT clear the config file')   
        setconfigfile()
    elif choice in ["6"]:
        return()
    else:
        setconfigfile()

def createconfigfile():
    config = configparser.ConfigParser()
    print(bcolors.FAIL + '    > configuration file not found, creating...' + bcolors.RESET)
    with open('configfile.ini', 'w') as configfile:
        config.write(configfile)
    print(bcolors.FAIL + '    > please configure the environment.' + bcolors.RESET)


def clearconfigfile():
    config = configparser.ConfigParser()
    print(bcolors.WARNING + '    > this will clear the configuration file' + bcolors.RESET)
    prompt =""
    choice = input(prompt)
    if choice in ["YES"]:
        print('option 1 selected')
        with open('configfile.ini', 'w') as configfile:
            config.write(configfile)
        print(bcolors.FAIL + '    > please configure the environment.' + bcolors.RESET)
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
                print(bcolors.FAIL + '    > configuration file is empty.' + bcolors.RESET)
                print(bcolors.FAIL + '    > please configure the environment.' + bcolors.RESET)
    except FileNotFoundError:
        createconfigfile()



#def setconfigfile():
#    config = configparser.ConfigParser()
#    config.read ('configfile.ini')
#    print(config.sections())


    """
    config['SERVER_1'] = {'host': 'xxx.xxx.xxx.xxx',
                        'user': 'aeonixadmin',
                        'password': 'anx'}

    config['SERVER_2'] = {'host': 'xxx.xxx.xxx.xxx',
                        'user': 'aeonixadmin',
                        'password': 'anx'}

    config['SERVER_3'] = {'host': 'xxx.xxx.xxx.xxx',
                        'user': 'aeonixadmin',
                        'password': 'anx'}

    config['SERVER_3'] = {'host': 'xxx.xxx.xxx.xxx',
                        'user': 'aeonixadmin',
                        'password': 'anx'}

    config['SERVER_4'] = {'host': 'xxx.xxx.xxx.xxx',
                        'user': 'aeonixadmin',
                        'password': 'anx'}

    #config['SERVER_1']['host'] = '10.1.16.55'

    with open('configfile.ini', 'w') as configfile:
        config.write(configfile)
    """