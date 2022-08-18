import os, sys, shutil, datetime
import ipaddress
from configobj import ConfigObj
import subprocess
import platform
import paramiko
#import main

class bcolors:
    OK = '\033[92m    > '      #GREEN
    OKV = '\033[92m'           #GREEN
    INFO = '\033[96m    > '    #LIGHT BLUE
    INFO2 = '\033[0m      '    #
    WARNING = '\033[93m    > ' #YELLOW
    WARNINGV = '\033[93m'      #YELLOW
    WARNING2 = '\033[93m      '#YELLOW
    FAIL = '\033[91m    > '    #RED
    FAILV = '\033[91m'         #RED
    FAIL2 = '\033[91m      '   #RED
    RESET = '\033[0m'          #RESET
    CLS = '\033[2J'            #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences


def check_if_ready():
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    remote_path = 'simulator/'
    err = 0
    for sectionnumber in range(1, sections + 1):
        SECTION = 'SERVER_' + str(sectionnumber) 
        host = config[SECTION]['host']
        user = config[SECTION]['user']
        password = config[SECTION]['password']
        sipp_host = config[SECTION]['sipp_host']
        sipp_user = config[SECTION]['sipp_user']
        sipp_password = config[SECTION]['sipp_password']
        serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
        #print(serverdict['section'], serverdict['host'], serverdict['sipp_host'])

        print()
        print(bcolors.INFO + 'checking sipp simulator SERVER_' + str(sectionnumber) + ' environment:' + bcolors.RESET)
        
        print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- aeonix server', host, ' - communication check  : ') + bcolors.RESET, end='')
        check = sipp_server_options(host, user, password, '', '', '')
        result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
        print(result)

        print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- aeonix server', host, ' - version check        : ') + bcolors.RESET, end='')
        check = sipp_server_options(host, user, password, '', '', 'anxver')
        result, err = (('failed', err+1) if check == 'error' else (check, err+0))
        print(result)

        print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- aeonix server', host, ' - operational check    : ') + bcolors.RESET, end='')
        check = sipp_server_options(host, user, password, '', '', 'anxrun')
        result, err = (('failed', err+1) if check == 'error' else (check, err+0))
        print(result)
        
        print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- sipp server', sipp_host, ' - communication check  : ') + bcolors.RESET, end='')
        check = sipp_server_options(sipp_host, sipp_user, sipp_password, '', '', '')
        result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
        print(result)

        print(bcolors.INFO2 + '{:<16s}{:>15s}{:>20s}'.format('- sipp server', sipp_host, ' - running job(s) check : ') + bcolors.RESET, end='')
        check = sipp_server_options(sipp_host, sipp_user, sipp_password, '', '', 'jobs')
        result, err = (('failed', err+1) if check == 'error' else ('passed', err+0))
        print(result)
    
    print()
    if err > 0:
        print(bcolors.FAIL + 'environmnet is not ready ' + str(err) + ' problems were detected - please check' + bcolors.RESET)
    else:
        print(bcolors.INFO + 'environmnet is ready for simulation tests' + bcolors.RESET)
    
    return('error' if err > 0 else 'passed')


def create_sim_files(capacity, start_at, method, options):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    #method = 'intra'
    template_method = 'templates/'+ method + '/'
    remote_path = 'simulator/'
        
    servers_capacity = {
        1: [1000, 2000, 3000, 5000],
        2: [2000, 4000, 6000, 8000],
        3: [3000, 6000, 9000, 12000],
        4: [4000, 8000, 10000, 12000],
        5: [5000, 10000, 15000, 20000],
        6: [6000, 12000, 18000, 24000]
    }
    first_user =     [30000, 40000, 50000, 60000, 70000]
    method_type = ['intra', 'inter', 'trunk']

    startuser=start_at

    if capacity == 0 or start_at == 0 or method_type =='':

        print(bcolors.INFO +'configuration file contains ' + str(sections) + ' server(s) sections' + bcolors.RESET)

        print()
        print(bcolors.INFO +'please choose 1 - 4 for total users amount to run with:' + bcolors.RESET)
        print(bcolors.INFO2, end ='')
        #print(servers_capacity[1][0])
        i = 0
        for element in servers_capacity[sections]:
            i += 1
            print(str(i) + '--> ' + str(element), end="  ")
        
        print(bcolors.RESET)
        print()
        try:
            choice = input("\r    Enter your choice [1-4]: ")
            if int(choice) < 1 or int(choice) > 4:
                print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
                return()
            capacity = servers_capacity[sections][int(choice) - 1]
            print(bcolors.INFO + str(capacity) + ' total users capacity was selected ' + bcolors.RESET)
            #return()
        except (ValueError, IndexError):
            print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
            return()
        
        
        print()
        print(bcolors.INFO +'please choose the first user to begin with:' + bcolors.RESET)
        print(bcolors.INFO2, end ="")
        i = 0
        for element in first_user:
            i += 1
            print(str(i) + '--> ' + str(element), end="  ")    
        
        print()
        print(bcolors.RESET)

        try:
            choice = input("\r    Enter your choice [1-5]: ")
            if int(choice) < 1 or int(choice) > 5:
                print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
                return()
            start_at = first_user[int(choice) - 1]
            print(bcolors.INFO + str(start_at) + ' as the first user was selected ' + bcolors.RESET)
            #return()
        except (ValueError, IndexError):
            print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
            return()

    print()
    print(bcolors.INFO + 'the following data was collected and saved: ' + bcolors.RESET)
    print(bcolors.INFO2 + '- load test configuration contains : ' + str(sections) + ' server(s)')
    print(bcolors.INFO2 + '- total capacity load amount of    : ' + str(capacity) + ' users') 
    print(bcolors.INFO2 + '- scope of imported uesrs          : from user #' + str(start_at) + ' to user #' + str(start_at + capacity - 1 ))
    print(bcolors.INFO2 + '- prefered load run method         : ' + method)

    # save all to 'temp' file
    temp = [str(sections), str(capacity), str(start_at), method]
    with open("temp", "w") as tempfile:
        tempfile.writelines(",".join(temp))
        tempfile.close()

    shutil.rmtree('scripts/', ignore_errors=True)
    main_local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method)
    os.makedirs(main_local_path, exist_ok = True)

    print()
    print(bcolors.INFO  + 'creating  : aeonix \'import_' + str(capacity) + '_users.csv\' file having the following fields/order...' + bcolors.RESET) 
    print(bcolors.INFO2 + '\'User ID\', \'Internal aliases\', \'Description\', \'Phone name\', \'Phone type\', \'Phone Domain\'' + bcolors.RESET) 
    #fieldnames =  ['User ID', 'Internal aliases', 'Description', 'Phone name', 'Phone type', 'Phone Domain']
    with open(main_local_path +'/import_'+str(capacity)+'_users.csv', 'w') as usersfile:
        for counter in range(start_at, int(start_at + capacity)):
            usersfile.write(str(counter) +','+str(counter) +','+str(counter) +'_Desc,'+str(counter)+',SIP terminal'+',aeonix.com\n')
        usersfile.close()


    for sectionnumber in range(1, sections + 1):
        print()
        print(bcolors.INFO + 'handling sipp simulator server_' + str(sectionnumber) + ' files:' + bcolors.RESET)

        SECTION = 'SERVER_' + str(sectionnumber) 
        host = config[SECTION]['host']
        user = config[SECTION]['user']
        password = config[SECTION]['password']
        sipp_host = config[SECTION]['sipp_host']
        sipp_user = config[SECTION]['sipp_user']
        sipp_password = config[SECTION]['sipp_password']
        serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
        #print(serverdict['section'], serverdict['host'], serverdict['sipp_host'])


        local_path = os.path.join ('scripts/', str(capacity) + '_users'+ '_' + method + '/server_'+str(sectionnumber))
        os.makedirs(local_path, exist_ok = True)
        files = os.listdir(template_method)
        print(bcolors.INFO2 + '- copy all templates files to local directory ../' + local_path + bcolors.RESET)
        [shutil.copy(template_method + fn, local_path) for fn in os.listdir(template_method)]
    
        print(bcolors.INFO2 + '- parsing executable \'*.sh\' scripts' + bcolors.RESET)
        replace_string(local_path +'/register.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/register.sh','[users]', str(int(capacity/sections)))
        replace_string(local_path +'/answer.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/call.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/blf.sh','[servers]', sipp_host + ' ' + host)

        print(bcolors.INFO2 + '- creating sequantial \'*.csv\' files' + bcolors.RESET)
        with open(local_path+'/register.csv', 'w') as registerfile:
            registerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + capacity/sections)):
                registerfile.write(str(counter) +';[authentication username='+str(counter) +' password=Aeonix123@]\n')
            registerfile.close()
        
        with open(local_path+'/call_answer.csv', 'w') as callanswerfile:
            callanswerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + capacity/sections), 2):
                callanswerfile.write(str(counter) + ';' + str(counter+1) +';\n')
            callanswerfile.close()
        
        print(bcolors.INFO2 + '- creating \'load.info\' file' + bcolors.RESET)
        with open(local_path + '/load.info', 'w') as loadinfofile:
            loadinfofile.write(SECTION +' (out of ' + str(sections) + ')\n')
            loadinfofile.write('total users = ' + str(capacity) + '\n')
            loadinfofile.write('sipp host : ' + sipp_host + ' --> aeonix host : ' + host + '\n')
            loadinfofile.write('users from : ' + str(startuser) + ' to : ' + str(int(startuser + capacity/sections - 1)) + ' (' + str(int(capacity/sections)) + ' users)\n')
            loadinfofile.close()

        print(bcolors.INFO2 + '- upload all simulation files' + bcolors.RESET)
        file_upload = sipp_server_options(sipp_host, sipp_user, sipp_password, local_path, remote_path, 'upload')
        
        startuser = startuser + int(capacity/sections) 


def replace_string(filepath, replace, with_string):
    with open(filepath, 'r+') as f:
        replace_string = f.read().replace(replace, with_string)
    with open(filepath, 'w', newline='\n') as f:
        f.write(replace_string)
    f.close()



def sipp_server_options(host, user, password, local_path, remote_path, option):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        transport = paramiko.Transport(host, 22)
        transport.connect(username=user,password=password)
        client.connect(hostname = host, username=user,password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except:
        return('error')
    
    
    if option in ['upload']:
        try:
            sftp.chdir(remote_path)
            ssh_command = 'cd ' + remote_path + '; chmod +x *.sh'
            stdin,stdout,stderr = client.exec_command(ssh_command)
        except IOError:
            sftp.mkdir(remote_path)
            sftp.chdir(remote_path)
        
        files = os.listdir(local_path)    
        for filename in files:
            sftp.put(local_path + '/' + filename, filename)
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; rm -rf *.zip'
        ssh_command = 'echo created at : ' + timestamp + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)
    
    elif option in ['host']:
        ssh_command = 'hostname'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response)

    elif option in ['jobs']:
        ssh_command = 'pgrep sipp'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        if response != '':
            return('error')

    elif option in ['terminate']:
        ssh_command = 'killall sipp ; echo terminated at : ' + timestamp + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)

    elif option in ['pack']:
        ssh_command = 'cd ' + remote_path + '; zip -r ../sim_`hostname`_' + timestamp + '_logs.zip * &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)

    elif option in ['download']:
        sftp.get('simulator_logs', local_path + '\simulator_logs')

    elif option in ['clean']:
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; ./clean_logs.sh &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)


    elif option in['anxver']:
        ssh_command ="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response if response !='' else 'error')

    elif option in['anxrun']:
        ssh_command ='sudo service aeonix status'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        running = response.count('running')
        stopped = response.count('stopped')
        return('running' if running == 6 and stopped == 0 else 'error')

    sftp.close()
    transport.close()
    client.close()


#results = check_if_ready()
#print(results)

capacity = 0
start_at = 30000
method = 'intra'
options = 'clean'
create_sim_files(capacity, start_at, method, options)
# options:
    # terminate
    # comm
    # jobs
    # clean
    # pack
    # download
    # create
    # upload

#check_if_ready()