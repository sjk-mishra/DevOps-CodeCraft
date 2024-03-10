from flask import Flask , url_for
from dependency import *

from dotenv import dotenv_values 

# from paramiko import channel
app = Flask(__name__)
config=dotenv_values(".env")
ssh_client=0
print(__name__)


#This checks the availability , i.e, Terraform and AWS CLI on the remote server.
#These are the core requirements for the processes that will be taken further on in this project 
@app.route('/')
def sys_requirements(): 
    
    net=connect.Network()
    status,ssh_client= net.network_connect()
    if status ==False:
        return "Connection Failed, Goodbye"
    _,stdout,_= ssh_client.exec_command("aws --version")
    print(stdout.read().decode())
    aws_response = stdout.read().decode()
    if "NotFound" in aws_response:
        aws_response = "Installed AWS on the system, run the aws --configure command to move further"
    _,stdout,stderr= ssh_client.exec_command("terraform --version")
    terraform_response = stdout.read().decode() + "/n" + "Server has the requirments to Build resource"
    if "NotFound" in terraform_response:
        terraform_response = "Installed Terraform on the Server"
    response = aws_response + "/n"+ terraform_response
    return response
    
        

@app.route('/build-resources')
def build_resouces():
    filepath= config['TERRAFORM_FILE']
    res=Build.Terraform_build(filepath)
    status= res.terraform_manipulate()
    data= res.terraform_run()
    return data

@app.route('show-resources/')
def show_resource():
    pass 

@app.route('/destroy-resources')
def destroy_resources():
    filepath= config['TERRAFORM_FILE']
    res=Build.Terraform_build(filepath)
    status= res.terraform_destroy()
    return status

if __name__ == "__main__":
    app.run()

