import configparser

class bcolors:
    OK = '\033[92m'      #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m'    #RED
    RESET = '\033[0m'


#https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
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

#config['SERVER_1']['password'] = 'ANX406729'

with open('configfile.ini', 'w') as configfile:
    config.write(configfile)


