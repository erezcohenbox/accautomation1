#import yaml

class bcolors:
    OK = '\033[92m'      #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m'    #RED
    RESET = '\033[0m'

servers = {
    "host": "10.1.16.55",
    "user": "root",
    "passwd": "ANX406729",
    "db": "write-math",
}

#inifile = open("configfile.ini", 'w')
#for key, value in records.items():

with open("configfile.ini", 'w') as inifile:
    inifile.write(str(servers))
    print(bcolors.OK + "    > successfully created." + bcolors.RESET)
    inifile.close


