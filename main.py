import os, sys
import config
import prepare


class bcolors:
    PROMPT  =   '\033[90m    > ' #GRAY
    PROMPTV =   '\033[90m'       #GRAY
    FAIL =      '\033[91m    > ' #RED
    FAILV =     '\033[91m'       #RED
    FAIL2 =     '\033[91m      ' #RED
    OK =        '\033[92m    > ' #GREEN
    OKV =       '\033[92m'       #GREEN
    WARNING =   '\033[93m    > ' #YELLOW
    WARNINGV =  '\033[93m'       #YELLOW
    WARNING2 =  '\033[93m      ' #YELLOW
    WARNINGX =  '\033[95m    > ' #PURPLE/PINK
    WARNINGXV = '\033[95m'       #PURPLE/PINK
    INFO =      '\033[96m    > ' #LIGHT BLUE
    INFOV =     '\033[96m'       #LIGHT BLUE
    INFO2 =     '\033[0m      '  #LIGHT BLUE
    MENU =      '\033[97m    > ' #WHITE
    MENUV =     '\033[97m'       #WHITE
    RESET =     '\033[0m'        #RESET
    CLS =       '\033[2J'        #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences



def main():
    main_menu()


def main_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENUV + """
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+
    |A|e|o|n|i|x| |L|o|a|d| |G|e|n|
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+    
    Aeonix Load Gen main menu
    1 -- environment configuration and status
    2 -- prepare for load running
    3 -- run load tests
    4 -- quit\n""" + bcolors.PROMPTV + """
    Enter your choice [1-4]: """ + bcolors.RESET 

    choice = input(prompt )

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
    prompt = bcolors.MENUV + """
    Aeonix Load Gen environment menu
    1 -- configure the environment
    2 -- check environment status
    3 -- go back\n""" + bcolors.PROMPTV + """
    Enter your choice [1-3]: """ + bcolors.RESET
    
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
    prompt = bcolors.MENUV + """ 
    Aeonix Load Gen prepare for load running menu
    1 -- select simulation type and create files
    2 -- upload all the simulation files 
    3 -- terminate all sipp jobs
    4 -- download all the logs (zipped)
    5 -- clean up all sipp logs
    5 -- clean up all sipp zip logs
    7 -- bulk prepare (terminate, clean and upload)
    8 -- go back\n""" + bcolors.PROMPTV + """
    Enter your choice [1-4]: """ + bcolors.RESET

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
        ready = prepare.execute('download', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'download was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'download done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["5"]:
        ready = prepare.execute('clean', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'clean was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'clean done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["6"]:
        ready = prepare.execute('clean_zip', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'clean was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'clean done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["7"]:
        prepare.handling_sipp_jobs('bulk')
        prepare_menu()
    elif choice in ["8"]:
        main_menu()
    else:
        prepare_menu()


# the program is initiated, so to speak, here
main()
