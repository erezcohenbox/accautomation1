from lib2to3.pgen2.parse import ParseError
import os, re
import ipaddress #, datetime
from configobj import ConfigObj

class bcolors:
    #PROMPT  =   '\033[90m    > ' #GRAY
    NOTE     =  '\033[90m'       #GRAY
    FAIL     =  '\033[91m'       #RED
    OK       =  '\033[92m'       #GREEN
    MENU     =  '\033[93m'       #YELLOW
    VARIABLE =  '\034[94m'       #BLUE
    WARNING  =  '\033[95m'       #PINK
    INFO     =  '\033[96m'       #LIGHT BLUE
    PROMPT   =  '\033[97m'       #WHITE
    RESET    =  '\033[0m'        #RESET
    CLS      =  '\033[2J'        #CLS

configFileName = 'configfileNew.ini'

try:
    configFileObject = ConfigObj(configFileName,raise_errors=True)
except:
    file = open(configFileName,"w")
    file.close()
    configFileObject = ConfigObj(configFileName,raise_errors=True)

class configfile:

    def initialize():
        with open(configFileName, 'w') as configfile:
            pass
        return

    def sectionsCount():
        return(len(configFileObject.sections))

    def sectionsNames():
        return(configFileObject.sections)

    def sectionsNamesDisplay():
        return(' | '.join(configFileObject.sections))

    def checkOptions():
        configFileOptions = ''
        try:
            with open(configFileName) as configFile:
                filesize = os.path.getsize(configFileName)
                #filesize = os.path.getsize(configfile)
                if filesize > 0:
                    #configFileOptions = ['add','edit','delete','clear']
                    configFileOptions = ['add','delete','clear']
                else:
                    configFileOptions = ['add']
        except FileNotFoundError:
            configFileOptions = ['initialize']
        
        return(configFileOptions)

    def sectionWrite(elementKeysInput):
        configFileObject[elementKeysInput[0]] = {}
        configFileObject[elementKeysInput[0]]['aeonix_host'] = elementKeysInput[0]
        configFileObject[elementKeysInput[0]]['aeonix_user'] = elementKeysInput[1]
        configFileObject[elementKeysInput[0]]['aeonix_password'] = elementKeysInput[2]
        configFileObject[elementKeysInput[0]]['aeonix_web_user'] = elementKeysInput[3]
        configFileObject[elementKeysInput[0]]['aeonix_web_password'] = elementKeysInput[4]
        configFileObject[elementKeysInput[0]]['sipp_host'] = elementKeysInput[5]
        configFileObject[elementKeysInput[0]]['sipp_user'] = elementKeysInput[6]
        configFileObject[elementKeysInput[0]]['sipp_password'] = elementKeysInput[7]
        configFileObject.write()
        print(bcolors.OK + 'done.' + bcolors.RESET)
        return

    def sectionRemove(aeonix_host):
        try:
            configFileObject.sections.remove(aeonix_host)
            configFileObject.write()
            #print(bcolors.OK + 'done.' + bcolors.RESET)
            return (True)
        except ValueError:
            #print(bcolors.FAIL + 'value not in list.' + bcolors.RESET)
            return (False)



    def sectionAdd():
        print(bcolors.NOTE + 'adding new server section' + bcolors.RESET)
        elementKeys = ['aeonix host', 'aeonix user', 'aeonix password', 'aeonix web user',
                                'aeonix web password', 'sipp host', 'sipp user', 'sipp password']
        elementKeysInput = []

        for iter in range(8):
            elementKeysInput.append(input(f'{elementKeys[iter]} = '))
            if 'host' in elementKeys[iter]:
                try:
                    ipaddress.ip_address(elementKeysInput[iter]) 
                except:
                    #print(bcolors.FAIL + 'invalid value.' + bcolors.RESET)
                    return (False)

            else:
                if " " in elementKeysInput[iter] or elementKeysInput[iter] == "":
                    #print(bcolors.FAIL + 'invalid value.' + bcolors.RESET)
                    return (False)

        configfile.sectionWrite(elementKeysInput)
        return(True)

    def overview():
        if configfile.sectionsCount() >= 1:
            file = open(configFileName,"r")
            fileLines = file.readlines()
            count = 0
            #print(bcolors.INFO +'configuration file contains ' + str(len(config.sections)) + ' server(s) sections' + bcolors.RESET)
            for line in fileLines:
                count += 1
                if line[0] =='[':
                    print('      ' + '-' * 60)
                print("      {}".format(line.strip()))
            file.close()
            print('      ' + '-' * 60)
            #reorderconfigfile()
        else:
            return




#a = configFileObject.walk
#print(a)

prompt = bcolors.MENU + """

Aeonix Load Gen configuration file menu
1 -- add a new server
2 -- delete a server
3 -- review the configuration file
4 -- clear/initialize the configuration file
5 -- go back
""" + bcolors.NOTE + f"""note:  you can use the {', '.join(configfile.checkOptions())} option(s) only\n""" + bcolors.PROMPT + """
Enter your choice [1-5]: """ + bcolors.RESET

#choice = input(prompt)

