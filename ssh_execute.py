import paramiko

def service():
    #import paramiko
    ip = '10.2.4.72'
    port = 22
    username = 'aeonixadmin'
    password = 'anx'

    cmd = 'sudo service aeonix status'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.readlines()
    response = ''.join(outlines)
    print(response)
    return (response)

