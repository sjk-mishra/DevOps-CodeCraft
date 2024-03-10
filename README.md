# DevOps-CodeCraft
Welcome to my DevOps project repository! This project utilizes Terraform to provision infrastructure resources, and is integrated with a Python Flask framework for automation.

Overview
This project aims to automate the provisioning and management of infrastructure resources using Terraform and Flask. By leveraging Terraform's Infrastructure as Code (IaC) capabilities and Flask's web framework, we enable seamless deployment and scaling of resources in a cloud environment.

Features
Provisioning of EC2 instances and VPC as well as a Internet Gateway using Terraform.
Creating two subnets and cnnecting them with a Loadbalancer to manage the traffic
Integration of Terraform scripts with Python Flask for automation.
Automate customization of the terraform scripts via environment variables
Scalable architecture for managing infrastructure resources.
Simplified deployment and maintenance process.
Getting Started
To get started with this project, follow these steps:

Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/sjk-mishra/devops-codecraft.git
Install Terraform on your system. Refer to the Terraform documentation for installation instructions.
Install AWS CLI and run 'aws configure' cmd to set the Access ID here .
Install Python and Flask on your system if you haven't already. You can use Python's package manager, pip, to install Flask:
Create a .env file acording to the .env.txt

bash
Copy code
pip install Flask
Navigate to the terraform/ directory and set the environment in the .env file. It requires the serve credentials on which the project will run or you wish to creat the resources and the resource details.

Start the Flask application by running the following command from the project root directory:

bash
Copy code
python app.py
Access the Flask application in your web browser at http://localhost:5000 and interact with the provided endpoints to trigger Terraform scripts.

Directory Structure
aws_terraform/: Contains Terraform scripts for provisioning infrastructure resources.
app.py: Main Flask application file with route definitions.
scripts/: Includes python files for flask application.