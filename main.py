import os, sys
#import ssh_execute
import config
import prepare
#import playground_3
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
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+
    |A|e|o|n|i|x| |L|o|a|d| |G|e|n|
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+    
    Aeonix Load Gen main menu
    1 -- environment configuration and status
    2 -- prepare for load running
    3 -- run load tests
    4 -- quit\n
    Enter your choice [1-4]: """

    choice = input(prompt)

    if choice in ["1"]:
        environment_menu()
    elif choice in ["2"]:
        prepare_menu()
    elif choice in ["3"]:
        main_menu()
    elif choice in ["4"]:
        print(bcolors.WARNINGV + "    > goodbye...\n" + bcolors.RESET)
        sys.exit()  # Leave the program
    else:
        main_menu()


def environment_menu():
    prompt = """
    Aeonix Load Gen environment menu
    1 -- configure the environment
    2 -- check environment status
    3 -- go back\n
    Enter your choice [1-3]: """
    
    choice = input(prompt)

    if choice in ["1"]:
        config.setconfigfile()
        environment_menu()
    elif choice in ["2"]:
        ready = prepare.execute('check_if_ready', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'environmnet is not ready - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'environmnet is ready for simulation tests' + bcolors.RESET)
        environment_menu()
    elif choice in ["3"]:
        main_menu()
    else:
        environment_menu()


def prepare_menu():
    prompt = """
    Aeonix Load Gen prepare for load running menu
    1 -- select simulation type and create files
    2 -- upload all the simulation files 
    3 -- terminate all sipp jobs and download the logs
    4 -- clean all sipp logs
    5 -- bulk prepare (terminate, clean and upload)
    6 -- go back\n
    Enter your choice [1-4]: """

    choice = input(prompt)

    if choice in ["1"]:
        prepare.create_sim_files(0,0,'intra')
        prepare_menu()
    elif choice in ["2"]:
        #prepare.create_sim_files()
        ready = prepare.execute('upload', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'upload was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'upload done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["3"]:
        ready = prepare.execute('terminate', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'terminate was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'terminate done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["4"]:
        ready = prepare.execute('clean', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'clean was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'clean done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["5"]:
        prepare.handling_sipp_jobs('bulk')
        prepare_menu()
    elif choice in ["6"]:
        main_menu()
    else:
        prepare_menu()


# the program is initiated, so to speak, here
main()
