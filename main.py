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
    2 -- prepare sipp for load running
    3 -- prepare aeonix for load running
    4 -- run load tests
    5 -- quit\n""" + bcolors.PROMPTV + """
    Enter your choice [1-4]: """ + bcolors.RESET 

    choice = input(prompt )

    if choice in ["1"]:
        environment_menu()
    elif choice in ["2"]:
        prepare_menu()
    elif choice in ["3"]:
        main_menu()
    elif choice in ["4"]:
        main_menu()
    elif choice in ["5"]:
        print(bcolors.WARNINGV + "    > goodbye...\n" + bcolors.RESET)
        sys.exit()  # Leave the program
    else:
        main_menu()


def environment_menu():
    prompt = bcolors.MENUV + """
    Aeonix Load Gen environment menu
    1 -- configure the environment file
    2 -- check environment status
    3 -- check cluster status
    4 -- go back\n""" + bcolors.PROMPTV + """
    Enter your choice [1-3]: """ + bcolors.RESET
    
    choice = input(prompt)

    if choice in ["1"]:
        config.setconfigfile()
        environment_menu()
    elif choice in ["2"]:
        ready = prepare.execute('check_if_ready', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'environmnet is not ready - at least ' + str(ready) + ' problem(s) found - please check' + bcolors.RESET)
            print(bcolors.FAIL + 'note: sipp runnning job(s) are counted as a problem although might not be such' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'environmnet is ready for simulation tests' + bcolors.RESET)
        environment_menu()
    elif choice in ["3"]:
        reply = prepare.execute('check_cluster_status', True)
        if reply == 'error':
            print('\n'+ bcolors.FAIL + 'cluster is not ready - at least 1 problem(s) found - please check' + bcolors.RESET)       
        else:
            print('\n'+ bcolors.INFO + 'cluster is ready for simulation tests' + bcolors.RESET)
        environment_menu()
    elif choice in ["4"]:
        main_menu()
    else:
        environment_menu()


def prepare_menu():
    prompt = bcolors.MENUV + """ 
    Aeonix Load Gen prepare environment for load running
    1 -- select simulation type and create files
    2 -- upload all the simulation files 
    3 -- apply aeonix patches (captcha, etc..) 
    4 -- terminate all sipp jobs
    5 -- download all the logs (zipped)
    6 -- clean up all sipp logs
    7 -- clean up all sipp zip logs
    8 -- headless prepare (terminate, clean and upload)
    9 -- go back\n""" + bcolors.PROMPTV + """
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
        ready = prepare.execute('patch', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'patch was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'patch done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["4"]:
        ready = prepare.execute('terminate', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'terminate was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'terminate done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["5"]:
        ready = prepare.execute('download', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'download was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'download done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["6"]:
        ready = prepare.execute('clean', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'clean was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'clean done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["7"]:
        ready = prepare.execute('clean_zip', True)
        if int(ready) > 0:
            print('\n'+ bcolors.FAIL + 'clean was not properly made - ' + str(ready) + ' problem(s) detected - please check' + bcolors.RESET)
        else:
            print('\n'+ bcolors.INFO + 'clean done properly - environmnt is ready for simulation tests' + bcolors.RESET)
        prepare_menu()
    elif choice in ["8"]:
        prepare.handling_sipp_jobs('bulk')
        prepare_menu()
    elif choice in ["9"]:
        main_menu()
    else:
        prepare_menu()


# the program is initiated, so to speak, here
main()
