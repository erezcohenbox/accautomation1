import os
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
configFileObject = ConfigObj(configFileName,raise_errors=False)




class configfile:

    def Initialize():
        with open(configFileName, 'w') as configfile:
            pass
        return

    def sectionsCount():
        return(len(configFileObject.sections))

    def sectionsNames():
        return(configFileObject.sections)

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
        return

    def sectionRemove():
        print(bcolors.NOTE + 'configuration file contains ' + str(configfile.sectionsCount()) + ' server(s) environment.' + bcolors.RESET)
        print(bcolors.INFO + ' | '.join(configFileObject.sections) + bcolors.RESET)
        aeonix_host = input(bcolors.PROMPT + 'type the server to remove: ' + bcolors.RESET)

        try:
            configFileObject.sections.remove(aeonix_host)
            configFileObject.write()
            print(bcolors.OK + 'done.' + bcolors.RESET)
        except ValueError:
            print(bcolors.FAIL + 'value not in list.' + bcolors.RESET)
        return

    def sectionAdd():
        print(bcolors.NOTE + 'adding new server section' + bcolors.RESET)
        aeonix_host = input(bcolors.INFO + 'aeonix host = '+ bcolors.RESET)
        if configfile.validateInput(aeonix_host, 'ipAddress') == 'invalid':
            return

        aeonix_user = input(bcolors.INFO + 'aeonix user = '+ bcolors.RESET)
        if configfile.validateInput(aeonix_user, 'regularString') == 'invalid':
            return

        aeonix_password = input(bcolors.INFO + 'aeonix password = '+ bcolors.RESET)
        if configfile.validateInput(aeonix_password, 'regularString') == 'invalid':
            return

        aeonix_web_user = input(bcolors.INFO + 'aeonix web user = '+ bcolors.RESET)
        if configfile.validateInput(aeonix_web_user, 'regularString') == 'invalid':
            return

        aeonix_web_password = input(bcolors.INFO + 'aeonix web password = '+ bcolors.RESET)
        if configfile.validateInput(aeonix_web_password, 'regularString') == 'invalid':
            return

        sipp_host = input(bcolors.INFO + 'sipp host = '+ bcolors.RESET)
        if configfile.validateInput(sipp_host, 'ipAddress') == 'invalid':
            return

        sipp_user = input(bcolors.INFO + 'sipp user = '+ bcolors.RESET)
        if configfile.validateInput(sipp_user, 'regularString') == 'invalid':
            return

        sipp_password = input(bcolors.INFO + 'sipp password = '+ bcolors.RESET)
        if configfile.validateInput(sipp_password, 'regularString') == 'invalid':
            return                   

        configfile.sectionWrite(aeonix_host, aeonix_user, aeonix_password, aeonix_web_user,
                                aeonix_web_password, sipp_host, sipp_user, sipp_password)


    def validateInput(valueInput, valueType):
        if valueType in ["ipAddress"]:
            try:
                ipaddress.ip_address(valueInput)
                #print(f'{ip} is correct. Version: IPv{ip.version}')
            except ValueError:
                print(bcolors.FAIL + 'invalid value.' + bcolors.RESET)
                return ('invalid')
        elif valueType in ["regularString"]:
            if " " in valueInput or valueInput == "":
                print(bcolors.FAIL + 'invalid value.' + bcolors.RESET)
                return ('invalid')
        else:
            return


#a = configfile.Initialize() v
#a = configfile.sectionsCount() v
#a = configfile.sectionsNames() v
#a = configfile.checkOptions() v
#a = configfile.sectionWrite(aeonix_host, aeonix_user, aeonix_password, aeonix_web_user, aeonix_web_password, sipp_host, sipp_user, sipp_password) v
#a = configfile.sectionRemove() 
#a = configfile.sectionAdd()
#print(a)

prompt = bcolors.MENU + """

Aeonix Load Gen configuration file menu
1 -- add a new server
2 -- delete a server
3 -- review the configuration file
4 -- initialize/clear the configuration file
5 -- go back
""" + bcolors.NOTE + f"""note:  you can use the {', '.join(configfile.checkOptions())} option(s) only\n""" + bcolors.PROMPT + """
Enter your choice [1-5]: """ + bcolors.RESET

choice = input(prompt)