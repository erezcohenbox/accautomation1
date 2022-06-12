#import yaml

class bcolors:
    OK = '\033[92m'      #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m'    #RED
    RESET = '\033[0m'

environment = [
    {
        'server #1': {
        'ip address' : 'xxx.xxx.xxx.xxx',
        'user name': 'username',
        'password': 'password'
        },
        'server #2': {
        'ip address' : 'xxx.xxx.xxx.xxx',
        'user name': 'username',
        'password': 'password'
        }
    }
]

with open("configfile.yaml", 'w') as yamlfile:
    data = yaml.dump(environment, yamlfile)
    print(bcolors.OK + "\t> successfully created." + bcolors.RESET)


