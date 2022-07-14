import os, sys
import ssh_execute
import config
import ipaddress


class bcolors:
    OK = '\033[92m    > '      #GREEN
    OKV = '\033[92m'           #GREEN
    INFO = '\033[96m    > '    #LIGHT BLUE
    WARNING = '\033[93m    > ' #YELLOW
    WARNINGV = '\033[93m'      #YELLOW
    FAIL = '\033[91m    > '    #RED
    FAILV = '\033[91m'         #RED
    RESET = '\033[0m'          #RESET
    CLS = '\033[2J'            #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences



def main():
    main_menu()


def main_menu():
    print(bcolors.RESET)
    prompt = """
    Aeonix Load Gen main menu
    1 -- environment status and setup
    2 -- prepare for load running
    3 -- database options
    4 -- quit\n
    Enter your choice [1-4]: """

    choice = input(prompt)

    if choice in ["1"]:
        environment_menu()
    elif choice in ["2"]:
        prepare_menu()
    elif choice in ["3"]:
        serviceMenu()
    elif choice in ["4"]:
        print(bcolors.WARNINGV + "    > goodbye...\n" + bcolors.RESET)
        sys.exit()  # Leave the program
    else:
        main_menu()


def environment_menu():
    prompt = """
    Aeonix Load Gen environment menu
    1 -- overview of environment configuration file
    2 -- check environment status
    3 -- set up the environment
    4 -- go back\n
    Enter your choice [1-3]: """
    
    choice = input(prompt)

    if choice in ["1"]:
        config.overviewconfigfile()
        environment_menu()
    elif choice in ["2"]:
        config.checkservers()
        environment_menu()
    elif choice in ["3"]:
        config.setconfigfile()
        environment_menu()
    elif choice in ["4"]:
        main_menu()
    else:
        environment_menu()


def prepare_menu():
    prompt = """
    Aeonix Load Gen prepare for load running menu
    1 -- check environment status
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
        config.checkservers()
        environment_menu()
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
