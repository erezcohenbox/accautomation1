import configparser

def createconfigfile():
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

    #config['SERVER_1']['host'] = '10.1.16.55'

    with open('configfile.ini', 'w') as configfile:
        config.write(configfile)
