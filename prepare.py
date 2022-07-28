import os
import ipaddress
#from ossaudiodev import SNDCTL_DSP_BIND_CHANNEL
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
    FAIL = '\033[91m    > '    #RED
    FAILV = '\033[91m'         #RED
    RESET = '\033[0m'          #RESET
    CLS = '\033[2J'            #CLS
    #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences





def load_type_select():
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)    
    servers_capacity =     [[1000, 2000, 3000, 5000],
                            [2000, 4000, 6000, 8000],
                            [3000, 6000, 9000, 12000],
                            [4000, 8000, 10000, 12000],
                            [5000, 10000, 15000, 20000],
                            [6000, 12000, 18000, 24000]] 
    
    print(bcolors.INFO +'configuration file contains ' + str(sections) + ' server(s) sections' + bcolors.RESET)
    print()
    print(bcolors.INFO +'please choose one of the following total users amount to run with:' + bcolors.RESET)
    print(bcolors.INFO2, end ="")
    for amount in range(len(servers_capacity[sections])):
        print(str(amount + 1) + " --> " + str(servers_capacity[sections - 1][amount]), end=" | ")
    print()
    print(bcolors.RESET)
    
    try:
        choice = input("\r    Enter your choice [1-4]: ")
        if int(choice) < 1 or int(choice) > 4:
            print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
            return()
        capacity = servers_capacity[sections-1][int(choice) - 1]
        print(bcolors.INFO + str(capacity) + ' total users capacity was selected ' + bcolors.RESET)
        #return()
    except (ValueError, IndexError):
        print(bcolors.WARNINGV + "    > invalid value was selected...\n" + bcolors.RESET)
        return()
    
    first_user =     [30000, 40000, 50000, 60000, 70000]
    
    print()
    print(bcolors.INFO +'please choose the first user to begin with:' + bcolors.RESET)
    print(bcolors.INFO2, end ="")
    for amount in range(len(first_user)):
        print(str(amount + 1) + " --> " + str(first_user[amount]), end=" | ")
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
    print(bcolors.INFO2 + '- prefered load run method         : intra test')

    # save all to 'temp' file
    temp = [str(capacity), str(start_at), 'intra']
    with open("temp", "w") as tempfile:
        tempfile.writelines(",".join(temp))
        tempfile.close()

        
        




def create_sim_files():
#def create_sim_files(users, startat, method):
    import os, shutil

    try:
        with open("temp", "r") as tempfile:
            joined_list = tempfile.read().split(',')
        #print(joined_list)
        tempfile.close()
        users = int(joined_list[0])
        startat = int(joined_list[1])
        method = joined_list[2]

    except(FileNotFoundError):
        print(bcolors.FAIL + 'you should \'set load type and capacity\' first' + bcolors.RESET)
        return()

    load_method = 'templates/'+ method + '/'
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)
    
    startuser=startat
    shutil.rmtree('scripts/', ignore_errors=True)
    local_path = os.path.join ('scripts/', str(users)+'_users')
    remote_path = 'simulator/'
    os.makedirs(local_path, exist_ok = True)
    
    print(bcolors.INFO  + 'creating  : aeonix \'import_' + str(users) + '_users.csv\' file having the following fields/order...' + bcolors.RESET) 
    print(bcolors.INFO2 + '\'User ID\', \'Internal aliases\', \'Description\', \'Phone name\', \'Phone type\', \'Phone Domain\'' + bcolors.RESET) 
    #fieldnames =  ['User ID', 'Internal aliases', 'Description', 'Phone name', 'Phone type', 'Phone Domain']
    with open(local_path+'/import_'+str(users)+'_users.csv', 'w') as usersfile:
        for counter in range(startuser, int(startuser + users)):
            usersfile.write(str(counter) +','+str(counter) +','+str(counter) +'_Desc,'+str(counter)+',SIP terminal'+',aeonix.com\n')
        usersfile.close()

     
    for sectionnumber in range(1, sections + 1):
        print()
        print(bcolors.INFO + 'handling simulator files of sipp server_' + str(sectionnumber) + ':' + bcolors.RESET)
        local_path = os.path.join ('scripts/', str(users)+'_users/server_'+str(sectionnumber))
        os.makedirs(local_path, exist_ok = True)
        files = os.listdir(load_method)
        print(bcolors.INFO2 + '- copy all templates files to local directory ../' + local_path + bcolors.RESET)
        [shutil.copy(load_method + fn, local_path) for fn in os.listdir(load_method)]
        
        SECTION = 'SERVER_' + str(sectionnumber) 
        host = config[SECTION]['host']
        user = config[SECTION]['user']
        password = config[SECTION]['password']
        sipp_host = config[SECTION]['sipp_host']
        sipp_user = config[SECTION]['sipp_user']
        sipp_password = config[SECTION]['sipp_password']
        serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
        #print(serverdict['section'], serverdict['host'], serverdict['sipp_host'])
        
        print(bcolors.INFO2 + '- parsing executable \'*.sh\' scripts' + bcolors.RESET)
        replace_string(local_path +'/register.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/register.sh','[users]', str(int(users/sections)))
        replace_string(local_path +'/answer.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/call.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/blf.sh','[servers]', sipp_host + ' ' + host)

        print(bcolors.INFO2 + '- creating sequantial \'*.csv\' files' + bcolors.RESET)
        with open(local_path+'/register.csv', 'w') as registerfile:
            registerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + users/sections)):
                registerfile.write(str(counter) +';[authentication username='+str(counter) +' password=Aeonix123@]\n')
            registerfile.close()
        
        with open(local_path+'/call_answer.csv', 'w') as callanswerfile:
            callanswerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + users/sections), 2):
                callanswerfile.write(str(counter) + ';' + str(counter+1) +';\n')
            callanswerfile.close()
        
        print(bcolors.INFO2 + '- uploading simulator files to sipp server' + bcolors.RESET)
        sfpt_upload_sipp_files(sipp_host, sipp_user, sipp_password, local_path, remote_path)
        
        startuser = startuser + int(users/sections) 
    print()
    print(bcolors.INFO + 'all file can be found in: ' + os.getcwd() + '/scripts/' + str(users)+ '_users' + bcolors.RESET)


def replace_string(filepath, replace, with_string):
    with open(filepath, 'r+') as f:
        replace_string = f.read().replace(replace, with_string)
    with open(filepath, 'w', newline='\n') as f:
        f.write(replace_string)
    f.close()

def sfpt_upload_sipp_files(host, user, password, local_path, remote_path):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try: #new
        transport = paramiko.Transport(host, 22)
        transport.connect(username=user,password=password)
        client.connect(hostname = host, username=user,password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except:
        print(bcolors.FAIL + 'communication error with sipp server - files upload failed, please check' + bcolors.RESET)
        return()
    try:
        sftp.chdir(remote_path)
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; ./prepare_to_run.sh'
        stdin,stdout,stderr = client.exec_command(ssh_command)
    except IOError:
        sftp.mkdir(remote_path)
        sftp.chdir(remote_path)
    files = os.listdir(local_path)
    
    for filename in files:
        sftp.put(local_path + '/' +filename, filename)
    ssh_command = 'cd ' + remote_path + '; chmod +x *.sh'
    stdin,stdout,stderr = client.exec_command(ssh_command)
    print(bcolors.INFO + 'files upload completed successfuly' + bcolors.RESET)
    sftp.close()
    transport.close()
    client.close()


#create_sim_files(2000, 30000, 'intra')
# how many users total, user starts at, run method