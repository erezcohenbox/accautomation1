import sys
import ssh_execute
#import yaml

# new comment

class bcolors:
    OK = '\033[92m'      #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m'    #RED
    RESET = '\033[0m'    #RESET

def main():
    main_menu()


def main_menu():
    prompt = """
    Aeonix Contact Center Main Menu
    1 -- environment setup
    2 -- service options
    3 -- database options
    4 -- quit\n
    Enter your choice [1-4]: """

    choice = input(prompt)[0]

    if choice in ["1"]:
        environment_menu()
    elif choice in ["2"]:
        serviceMenu()
    elif choice in ["3"]:
        serviceMenu()
    elif choice in ["4"]:
        print(bcolors.OK + "\n\t> goodbye...\n" + bcolors.RESET)
        sys.exit()  # Leave the program
    else:
        main_menu()


def environment_menu():
    prompt = """
    Aeonix Contact Center environment setup Menu
    1 -- overview current setup
    2 -- change environment setup
    3 -- go back\n
    Enter your choice [1-3]: """

    choice = input(prompt)[0]

    if choice in ["1"]:
        try:
            with open('configfile.ini') as file:
                print('try to open')
                #data = yaml.safe_load(file)
                #for key, value in data.items():
                #   print(key, ":", value)
        except FileNotFoundError:
            print(bcolors.FAIL + '\t> configuration file not found, creating...' + bcolors.RESET)
            import config
        environment_menu()
    elif choice in ["2"]:
        # acc_server_status = ssh_execute.service('accd', 'restart')
        print('\t> done.')
        environment_menu()
    elif choice in ["3"]:
        # acc_server_status = ssh_execute.service('accwebappsd', 'restart')
        main_menu()
    else:
        environment_menu()


def serviceMenu():
    prompt = """
    Aeonix Contact Center Service Menu
    1 -- check status
    2 -- restart service
    3 -- restart web service
    4 -- start service
    5 -- start web service
    6 -- stop service
    7 -- stop web service
    8 -- go back\n
    Enter your choice [1-8]: """

    choice = input(prompt)[0]

    if choice in ["1"]:
        acc_server_status = ssh_execute.service('accd', 'status')
        print('\t> service accd is ' + acc_server_status.split(" ")[2])
        print('\t> service accwebappsd is ' + acc_server_status.split(" ")[11])
        serviceMenu()
    elif choice in ["2"]:
        acc_server_status = ssh_execute.service('accd', 'restart')
        print('\t> done.')
        serviceMenu()
    elif choice in ["3"]:
        acc_server_status = ssh_execute.service('accwebappsd', 'restart')
        print('\t> done.')
        serviceMenu()
    elif choice in ["4"]:
        acc_server_status = ssh_execute.service('accd', 'start')
        print('\t> done.')
        serviceMenu()
    elif choice in ["5"]:
        acc_server_status = ssh_execute.service('accwebappsd', 'start')
        print('\t> done.')
        serviceMenu()
    elif choice in ["6"]:
        acc_server_status = ssh_execute.service('accd', 'stop')
        print('\t> done.')
        serviceMenu()
    elif choice in ["7"]:
        acc_server_status = ssh_execute.service('accwebappsd', 'stop')
        print('\t> done.')
        serviceMenu()
    elif choice in ["8"]:
        main_menu()
    else:
        serviceMenu()


# the program is initiated, so to speak, here
main()
