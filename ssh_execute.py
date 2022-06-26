import paramiko

def service(service,command):
    import paramiko
    ip = '10.1.16.55'
    port = 22
    username = 'aeonixadmin'
    password = 'anx'

    cmd = 'sudo service ' + ' ' + service + ' ' + command

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.readlines()
    response = ''.join(outlines)
    return (response)
