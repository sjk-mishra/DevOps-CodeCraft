from dependency import *

class Terraform_build:
    def __init__(self, file):
        self.filepath=file
        ssh_client=0
        
    def terraform_manipulate(self):
        net=connect.Network()
        status,self.ssh_client= net.network_connect()

        _,stdout, _ = self.ssh_client.exec_command("ls")
        if "aws_terraform" not in stdout.read().decode():
            _,stdout,_ = self.ssh_client.exec_command(f"sshpass -p {config['SERVER_PWD']} scp -r aws_terraform {config['SERVER_USERNAME']}@{config['SERVER_IP']}:/home/{config['SERVER_USERNAME']}")
            _,stdout,_ = self.ssh_client.exec_command(f"sshpass -p {config['SERVER_PWD']} scp -r config_scripts {config['SERVER_USERNAME']}@{config['SERVER_IP']}:/home/{config['SERVER_USERNAME']}")
        
        filepath = self.filepath +"/files.tf"
        print(self.filepath)
        command = [f"""sed -i "s/%sg%/{config['SECURITY_GRP']}/g" {filepath}""", 
                   f"""sed -i "s/%tg%/{config['TARGET_GROUP']}/g" {filepath}""",
                    f"""sed -i "s/%bucket-name%/{config['BUCKET_NAME']}/g" {filepath}""", 
                    f"""sed -i "s/%lb%/{config['LOAD_BALANCER']}/g" {filepath}""",
                    f"""sed -i "s/%cidr_block1%/{config['cidr_block1']}/g" {filepath}""",
                    f"""sed -i "s/%cidr_block2%/{config['cidr_block2']}/g" {filepath}""",
                    f"""sed -i "s/%availability_zone1%/{config['AVAILABILITY_ZONE_SUBNET1']}/g" {filepath}""",
                    f"""sed -i "s/%availability_zone2%/{config['AVAILABILITY_ZONE_SUBNET2']}/g" {filepath}""",]
        
        for cmd in command:
            _, stdout, stderr = self.ssh_client.exec_command(cmd)
            print(stderr.read().decode() )
            print(cmd)
        self.ssh_client.close()
        return True

    def terraform_run(self):
        net=connect.Network()
        status,self.ssh_client= net.network_connect()
        if status== False:
            return "Network Failed"
      
        # _,stdout,_ = self.ssh_client.exec_command(f"cd {self.filepath} && terraform state list")
        # resouces = stdout.read().decode()
        # if config["BUCKET_NAME"] in resouces:
        #     return "THE RESOURCECS ARE ALREADY CREATED , RUN THE destroy/ route to delete the resources"
        
        # _,stdout,stderr = self.ssh_client.exec_command(f"cd {self.filepath} && terraform init")
        # stdout.channel.recv_exit_status()
        # print("init error",stderr.read().decode())
        # print("OUTPUT INIT   ",stdout.read().decode())

        # _,stdout,stderr = self.ssh_client.exec_command(f"cd {self.filepath} && terraform validate")
        # stdout.channel.recv_exit_status()
        # print("validate error",stderr.read().decode())
        # print("OUTPUT Validate   ",stdout.read().decode())

        # _,stdout,stderr = self.ssh_client.exec_command(f"cd {self.filepath} && terraform plan -out=tfplan -input=false")
        # stdout.channel.recv_exit_status()
        # print("plan error",stderr.read().decode())
        # output_plan= stdout.read().decode()
        # print("OUTPUT plan   ",output_plan)

        # if "No changes. Your infrastructure matches the configuration" in output_plan:
        #     _,stdout,stderr = self.ssh_client.exec_command(f"cd {self.filepath} && terraform state list")
        #     stdout.channel.recv_exit_status()
        #     resource_output= stdout.readlines()
        #     return "Resources are already created"
        
        # _,stdout,_ = self.ssh_client.exec_command(f"cd {self.filepath} && terraform apply -input=false -auto-approve tfplan ")
        # stdout.channel.recv_exit_status()
        # apply_output= stdout.read().decode()
        # print("OUTPUT apply",apply_output)

    
        _,stdout,stderr = self.ssh_client.exec_command(f"cd {self.filepath} && terraform state list")
        stdout.channel.recv_exit_status()
        resource_output= stdout.read().decode()
        print("resource_output",resource_output)
        self.ssh_client.close()
        return resource_output
        
        
    def terraform_show(self):
        net=connect.Network()
        status,self.ssh_client= net.network_connect()
        _,stdout,self.ssh_client = self.ssh_client_exec_command(f"cat tfplan")
        return stdout.read().decode()
    
    def terraform_revert_changes(self):
        net=connect.Network()
        status,self.ssh_client= net.network_connect()
        filepath = self.filepath +"/files.tf"
        command = [f"""sed -i "s/{config['SECURITY_GRP']}/%sg%/g" {filepath}""", 
                   f"""sed -i "s/{config['TARGET_GROUP']}/%tg%/g" {filepath}""",
                    f"""sed -i "s/{config['BUCKET_NAME']}/%bucket-name%/g" {filepath}""", 
                    f"""sed -i "s/{config['LOAD_BALANCER']}/%lb%/g" {filepath}""",
                    f"""sed -i "s/{config['cidr_block1']}/%cidr_block1%/g" {filepath}""",
                    f"""sed -i "s/{config['cidr_block2']}/%cidr_block2%/g" {filepath}""",
                    f"""sed -i "s/{config['AVAILABILITY_ZONE_SUBNET1']}/%availability_zone1%/g" {filepath}""",
                    f"""sed -i "s/{config['AVAILABILITY_ZONE_SUBNET2']}/%availability_zone2%/g" {filepath}""",]
        
        for cmd in command:
            _, stdout, stderr = self.ssh_client.exec_command(cmd)
            print(cmd)

    
    def terraform_destroy(self):
        net=connect.Network()
        status,self.ssh_client= net.network_connect()
        if status== False:
            return "Network Failed"
        
        _, stdout, stderr = self.ssh_client.exec_command(f"cd {self.filepath} && rm -rf tfplan")
        _,stdout,_ = self.ssh_client.exec_command(f"cd {self.filepath} && terraform destroy -input=false -auto-approve")
        stdout.channel.recv_exit_status()
        destroy_output= stdout.readline()
        print("OUTPUT destroy   ",destroy_output)
        self.terraform_revert_changes()
        return destroy_output
        