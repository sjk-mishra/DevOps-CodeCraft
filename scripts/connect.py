from dependency import *

class Network:
    def __init__(self):
        self.ip=config["SERVER_IP"]
        self.username=config["SERVER_USERNAME"]
        self.pwd= config["SERVER_PWD"]
        
    def network_connect(self):
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=self.ip, username=self.username, password=self.pwd, timeout=5)
            _,stdout,stderr= ssh_client.exec_command("ls")
            stdout.channel.recv_exit_status()
            print("inside network",          stdout.read().decode())
            message="Able to connect"
        except:
            return False, "Not Able to connect"
        return True, ssh_client
    
