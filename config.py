import configparser

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

#https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config['DEFAULT'] = {'host': '10.1.16.55',
                    'user': 'aeonixadmin',
                    'password': 'anx'}

#inifile = open("configfile.ini", 'w')
#for key, value in records.items():

config['DEFAULT']['ForwardX11'] = 'yes'
with open('configfile.ini', 'w') as configfile:
    config.write(configfile)


