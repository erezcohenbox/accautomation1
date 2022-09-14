import os
import ipaddress #, datetime
from configobj import ConfigObj

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
    WARNING2 =  '\033[93m      ' #YELLOW
    WARNINGX =  '\033[95m    > ' #PURPLE/PINK
    WARNINGXV = '\033[95m'       #PURPLE/PINK
    INFO =      '\033[96m    > ' #LIGHT BLUE
    INFOV =     '\033[96m'       #LIGHT BLUE
    INFO2 =     '\033[0m      '  #LIGHT BLUE
    MENU =      '\033[97m    > ' #WHITE
    MENUV =     '\033[97m'       #WHITE
    RESET =     '\033[0m'        #RESET
    CLS =       '\033[2J'        #CLS

configFileName = 'configfileNew.ini'
configFileObject = ConfigObj(configFileName,raise_errors=False)

class configfile:


    def sectionsCount():
        #configFile = ConfigObj('configfile.ini')
        return(len(configFileObject.sections))

    def checkOptions():
        configFileOptions = ''
        try:
            with open(configFileName) as configFile:
                filesize = os.path.getsize(configFileName)
                #filesize = os.path.getsize(configfile)
                if filesize > 0:
                    configFileOptions = ['add','edit','delete','clear']
                else:
                    configFileOptions = ['add']
        except FileNotFoundError:
            configFileOptions = ['initialize']
        
        return(configFileOptions)

    def sectionWrite(aeonix_host, aeonix_user, aeonix_password, aeonix_web_user,
                     aeonix_web_password, sipp_host, sipp_user, sipp_password):
        configFileObject[aeonix_host] = {}
        configFileObject[aeonix_host]['aeonix_host'] = aeonix_host
        configFileObject[aeonix_host]['aeonix_user'] = aeonix_user
        configFileObject[aeonix_host]['aeonix_password'] = aeonix_password
        configFileObject[aeonix_host]['aeonix_web_user'] = aeonix_web_user
        configFileObject[aeonix_host]['aeonix_web_password'] = aeonix_web_password
        configFileObject[aeonix_host]['sipp_host'] = sipp_host
        configFileObject[aeonix_host]['sipp_user'] = sipp_user
        configFileObject[aeonix_host]['sipp_password'] = sipp_password
        configFileObject.write()
        print(bcolors.OK + 'done.' + bcolors.RESET)

    def sectionRemove(aeonix_host):
        configFileObject.sections.remove(aeonix_host)
        configFileObject.write()
        print(bcolors.OK + 'done.' + bcolors.RESET)
        return()

    def Initialize():
        with open(configFileName, 'w') as configfile:
            pass
        return()

    def sectionInput():
        print(bcolors.WARNING + 'adding new server section' + bcolors.RESET)
        
        aeonix_host = input(bcolors.INFO + 'aeonix host = '+ bcolors.RESET )
        try:
            checkIp = ipaddress.ip_address(aeonix_host)
            #print(f'{ip} is correct. Version: IPv{ip.version}')
        except ValueError:
            print(bcolors.FAIL + 'invalid ip address...' + bcolors.RESET)
            return()
        
        aeonix_user = input(bcolors.INFO + 'aeonix user = '+ bcolors.RESET)
        if " " in aeonix_user or aeonix_user =="":
            print(bcolors.FAIL + 'invalid user name...' + bcolors.RESET)
            return()

        aeonix_password = input(bcolors.INFO + 'aeonix password = '+ bcolors.RESET)
        if " " in aeonix_password or aeonix_password =="":
            print(bcolors.FAIL + 'invalid password...' + bcolors.RESET)
            return()

        aeonix_user = input(bcolors.INFO + 'aeonix user = '+ bcolors.RESET)
        if " " in aeonix_user or aeonix_user =="":
            print(bcolors.FAIL + 'invalid user name...' + bcolors.RESET)
            return()

        aeonix_password = input(bcolors.INFO + 'aeonix user = '+ bcolors.RESET)
        if " " in aeonix_password or aeonix_password =="":
            print(bcolors.FAIL + 'invalid user name...' + bcolors.RESET)
            return()

        #sections = configfile.sectionsCount(configFileObject)
        #serverNumber = sections + 1
        aeonix_host = '172.28.9.222'
        aeonix_user = 'aeonixadmin'
        aeonix_password = 'anx'
        aeonix_web_user = 'aeonixadmin'
        aeonix_web_password = 'Ujxxxx'
        sipp_host = '172.28.9.71'
        sipp_user = 'erezcohem'
        sipp_password = 'tadirantele'
        configfile.sectionWrite(aeonix_host, aeonix_user, aeonix_password, aeonix_web_user,
                     aeonix_web_password, sipp_host, sipp_user, sipp_password)

#a = configfile.sectionsCount()
#a = configfile.checkOptions()
#a = configfile.sectionAdd()
#a = configfile.sectionRemove('172.28.9.221')
a = configFileObject


print(a)