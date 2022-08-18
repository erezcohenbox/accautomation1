from asyncio.windows_events import NULL
import os, sys, shutil, datetime
import ipaddress
from configobj import ConfigObj
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


def server_command(server, component, option):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    sections = len(config.sections)  
    remote_path = 'simulator/'
    check = None
    err = 0
    #print(bcolors.INFO +'configuration file contains ' + str(sections) + ' server(s) sections' + bcolors.RESET)
    #for sectionnumber in range(1, sections + 1):
    SECTION = 'SERVER_' + str(server) 
    aeonix_host = config[SECTION]['host']
    aeonix_user = config[SECTION]['user']
    aeonix_password = config[SECTION]['password']
    sipp_host = config[SECTION]['sipp_host']
    sipp_user = config[SECTION]['sipp_user']
    sipp_password = config[SECTION]['sipp_password']
    serverdict = {'section':SECTION, 'aeonix_host': aeonix_host, 'aeonix_user': aeonix_user, 'aeonix_password':aeonix_password, 'sipp_host': sipp_host, 'sipp_user': sipp_user, 'sipp_password':sipp_password}
    #print(serverdict['section'], serverdict['aeonix_host'], serverdict['sipp_host'])

    if component in ["aeonix"]:
        host = aeonix_host
        user = aeonix_user
        password = aeonix_password
    elif component in ["sipp"]:
        host = sipp_host
        user = sipp_user
        password = sipp_password

    if option in ["comm"]:
        check = server_options(host, user, password, '', '', '')

    elif option in ["hostname"]:
        check = server_options(host, user, password, '', '', 'hostname')

    elif option in ["jobs"] and component == 'sipp':
        check = server_options(host, user, password, '', '', 'jobs')

    elif option in ["status"] and component == 'aeonix':
        check = server_options(host, user, password, '', '', 'status')

    elif option in ["version"] and component == 'aeonix':
        check = server_options(host, user, password, '', '', 'version')

    elif option in ["terminate"] and component == 'sipp':
        check = server_options(host, user, password, '', '', 'terminate')

    elif option in ["clean"] and component == 'sipp':
        check = server_options(host, user, password, '', remote_path, 'clean')
    
    return(check)


def server_options(host, user, password, local_path, remote_path, option):
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
    
    elif option in ['hostname']:
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
            return('running')
        elif response == '':
            return('stopped')

    elif option in ['terminate']:
        ssh_command = 'killall sipp ; echo terminated at : ' + timestamp + '\r >> ' + remote_path + 'load.info'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        return None

    elif option in ['pack']:
        ssh_command = 'cd ' + remote_path + '; zip -r ../sim_`hostname`_' + timestamp + '_logs.zip * &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)

    elif option in ['download']:
        sftp.get('simulator_logs', local_path + '\simulator_logs')

    elif option in ['clean']:
        ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; ./clean_logs.sh &>/dev/null &'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        return None

    elif option in['version']:
        ssh_command ="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        return(response if response !='' else 'error')

    elif option in['status']:
        ssh_command ='sudo service aeonix status'
        stdin,stdout,stderr = client.exec_command(ssh_command)
        outlines = stdout.readlines()
        response = ''.join(outlines)
        running = response.count('running')
        stopped = response.count('stopped')
        return('running' if running == 6 and stopped == 0 else 'stopped' if running == 0 and stopped == 6 else 'error')

    else:
        return('open')
    sftp.close()
    transport.close()
    client.close()

remote_path = 'simulator/'
results = server_command('3','sipp','clean')
print(results)





capacity = 1
start_at = 30000
method = 'intra'
options = 'clean'
#create_sim_files(capacity, start_at, method, options)
# options:
    # terminate v
    # comm      v
    # jobs      v 
    # clean     v
    # pack
    # download
    # create
    # upload

#check_if_ready()