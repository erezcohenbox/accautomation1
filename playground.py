from configobj import ConfigObj
import os
import ipaddress
import paramiko

import platform
import subprocess



def printsections():
    config = ConfigObj('configfile.ini')
    print(config['SERVER_1'])
    print(config['SERVER_1']['host'])
    print(config['SERVER_1']['host'] == '1.1.1.1')
    #host = config['SERVER_1']['host'] 




    

def checkservers():
    import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmdx='pwd'
    serverlist =[]
    config = ConfigObj('configfile.ini')
    for servernumber in range(len(config.sections)):
        host = config['SERVER_' + str(servernumber + 1)]['host']
        user = config['SERVER_' + str(servernumber + 1)]['user']
        password = config['SERVER_' + str(servernumber + 1)]['password']
        serverlist.append(str(host))
        #print(serverlist)
        if ping_ip(host):
            print(f"      host: {host:15} ping ok")
        else:
            print(f"      host: {host:15} ping unreachable")

        if ssh_ip(host, user, password, cmdx):
            print(' '*27, 'ssh established')
        else:
            print(' '*27, 'ssh timeout error')


def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', current_ip_address ), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
            return False

def ssh_ip(host, user, password, cmdx):
    import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        _stdin, _stdout,_stderr = client.exec_command(cmdx)
        client.close()
        return True
    except Exception:
        return False

def serverelements(sectionnumber):
    config = ConfigObj('configfile.ini')
    serverdict = {}
    serverdict.clear
    SECTION = 'SERVER_' + str(sectionnumber) 
    host = config[SECTION]['host']
    user = config[SECTION]['user']
    password = config[SECTION]['password']
    serverdict = {'section':SECTION, 'host': host, 'user': user, 'password':password}
    #print(serverdict['section'])
    return(serverdict)


#serverelements(1)
#print(serverelements(1)['host'])
'''
config = ConfigObj('configfile.ini')
print()
for sectionnumber in range(1, len(config.sections)):
    serverelements(1)
    SECTION = serverelements(sectionnumber['section'])
    host = serverelements(sectionnumber['host'])
    user = serverelements(sectionnumber['user'])
    password = serverelements(sectionnumber['password'])
    print('    [' + SECTION + ']')
    print('    host = ' + host)
    print('    host = ' + user)
    print('    host = ' + password)
'''





def ssh_readfile(host, user, password): 
    commands = [
    "killall sipp \n cd /home/erezcohen/simulator/sipp_sim_from_pc \n rm -rf *_.csv *_errors.log \n pwd \n"
    ]
    
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=user, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()

    for command in commands:
        print("="*50, command, "="*50)
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)

#ssh_readfile('172.28.8.216', 'erezcohen', 'tadirantele')

def ssh_ip(host, user, password, cmdx):
    import paramiko
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        stdin, stdout, stderr = client.exec_command(cmdx)
        client.close()
        return True
    except Exception:
        return False
#cmdx='killall sippx'
#print(ssh_ip('172.28.8.215', 'erezcohen', 'tadirantele', cmdx))

# pip install pysphere
#from pysphere import VIServer, VIProperty, MORTypes
#from pysphere.resources import VimService_services as VI
#from pysphere.vi_task import VITask
# https://jensd.be/370/linux/create-a-new-virtual-machine-in-vsphere-with-python-pysphere-and-the-vmware-api
# https://stackoverflow.com/questions/35197979/getting-error-while-logging-in-to-guest-vm-using-pysphere

def connectToHost(host,host_user,host_pw):
    from pysphere import VIServer, VIProperty, MORTypes
    from pysphere.resources import VimService_services as VI
    from pysphere.vi_task import VITask
    #create server object
    #s=VIServer()
    #connect to the host
    #try:
    #   s.connect(host,host_user,host_pw)
    #   return s
    #except VIApiException, err:
    #   print "Cannot connect to host: "+host+" error message: "+err

#connectToHost('10.1.16.52','root', 'tadirantele' )

#ssh_upload('10.1.16.55','aeonixadmin','anx', 'pwd')
#checkservers()
#printsections()

#import pysipp
#pysipp.client(destaddr=('10.10.8.88', 5060))()

def create_sim_files(users, startat, method):
    import os, shutil

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
    #fieldnames =  ['User ID', 'Internal aliases', 'Description', 'Phone name', 'Phone type', 'Phone Domain']
    with open(local_path+'/import_'+str(users)+'_users.csv', 'w') as usersfile:
        for counter in range(startuser, int(startuser + users)):
            usersfile.write(str(counter) +','+str(counter) +','+str(counter) +'_Desc,'+str(counter)+',SIP terminal'+',aeonix.com\n')
    
    for sectionnumber in range(1, sections + 1):
        local_path = os.path.join ('scripts/', str(users)+'_users/server_'+str(sectionnumber))
        os.makedirs(local_path, exist_ok = True)
        files = os.listdir(load_method)
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
        
        replace_string(local_path +'/register.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/register.sh','[users]', str(int(users/sections)))
        replace_string(local_path +'/answer.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/call.sh','[servers]', sipp_host + ' ' + host)
        replace_string(local_path +'/blf.sh','[servers]', sipp_host + ' ' + host)

        with open(local_path+'/register.csv', 'w') as registerfile:
            registerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + users/sections)):
                registerfile.write(str(counter) +';[authentication username='+str(counter) +' password=Aeonix123@]\n')
        with open(local_path+'/call_answer.csv', 'w') as callanswerfile:
            callanswerfile.write('SEQUENTIAL\n')
            for counter in range(startuser, int(startuser + users/sections), 2):
                callanswerfile.write(str(counter) + ';' + str(counter+1) +';\n')
        
        sfpt_upload_sipp_files(sipp_host, sipp_user, sipp_password, local_path, remote_path)
        
        startuser = startuser + int(users/sections) 
    #print("Finished")


def replace_string(filepath, replace, with_string):
    with open(filepath, 'r+') as f:
        replace_string = f.read().replace(replace, with_string)
    with open(filepath, 'w', newline='\n') as f:
        f.write(replace_string)


def sfpt_upload_sipp_files(host, user, password, local_path, remote_path):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    transport = paramiko.Transport(host, 22)
    transport.connect(username=user,password=password)
    client.connect(hostname = host, username=user,password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
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
    sftp.close()
    transport.close()
    client.close()


#create_sim_files(2000, 30000, 'intra')
# how many users total, user starts at, run method
#

def testfile():
    temp = ['2000', '30000', 'intra']
    with open("temp.txt", "w") as tempfile:
        tempfile.writelines(",".join(temp))
        tempfile.close()

    with open("temp.txt", "r") as tempfile:
        joined_list = tempfile.read().split(',')
        #print(joined_list)
        tempfile.close()

testfile()


        #for items in temp:
        #    tempfile.writelines(items + ', ')
        #tempfile.close()