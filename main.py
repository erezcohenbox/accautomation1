import os, sys
import ssh_execute
import config
import ipaddress


class bcolors:
    OK = '\033[92m'      #GREEN
    INFO = '\033[95m'    #PURPLE
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m'    #RED
    RESET = '\033[0m'    #RESET
    CLS = '\033[2J'      #CLEAR SCREEN
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences



def main():
    main_menu()


def main_menu():
    print(bcolors.RESET)
    prompt = """
    Aeonix Contact Center Main Menu
    1 -- environment setup
    2 -- service options
    3 -- database options
    4 -- quit\n
    Enter your choice [1-4]: """

    choice = input(prompt)

    if choice in ["1"]:
        environment_menu()
    elif choice in ["2"]:
        serviceMenu()
    elif choice in ["3"]:
        serviceMenu()
    elif choice in ["4"]:
        print(bcolors.WARNING + "    > goodbye...\n" + bcolors.RESET)
        sys.exit()  # Leave the program
    else:
        main_menu()


def environment_menu():
    prompt = """
    Aeonix Contact Center environment Menu
    1 -- overview of environment status
    2 -- set up the environment
    3 -- go back\n
    Enter your choice [1-3]: """
    
    choice = input(prompt)

    if choice in ["1"]:
        #config.overviewconfigfile()
        config.checkservers()
        environment_menu()
    elif choice in ["2"]:
        config.setconfigfile()
        environment_menu()
    elif choice in ["3"]:
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

    choice = input(prompt)

    if choice in ["1"]:
        acc_server_status = ssh_execute.service('accd', 'status')
        print(bcolors.INFO + '    > service accd is ' + acc_server_status.split(" ")[2] + bcolors.RESET)
        print(bcolors.INFO + '    > service accwebappsd is ' + acc_server_status.split(" ")[11] + bcolors.RESET)
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
