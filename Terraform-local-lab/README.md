# Day 19: Terraform Local Lab – First IaC Workflow

This project is my first contact with **Terraform**, using the `local_file` provider to create and manage a local text file. No cloud credentials required – just the fundamental `init → plan → apply → destroy` cycle.

## 📌 What This Project Does

- Defines a local file resource (`hello.txt`) with dynamic content (timestamp).
- Outputs the file path after creation.
- Demonstrates idempotence: deleting the file manually and re‑applying re‑creates it instantly.

## 🧰 Tools & Concepts

| Area               | Technology       |
|--------------------|------------------|
| Provisioning       | Terraform (HCL)  |
| Provider           | `local`           |
| Workflow           | `init`, `plan`, `apply`, `destroy` |
| Infrastructure as Code | Yes – declarative desired state |

## 📁 Project Structure

terraform-local-lab/
├── main.tf # Terraform configuration
├── hello.txt # Created by Terraform (not committed)
└── README.md


## 🔧 Prerequisites

- Terraform ≥ 1.0 installed on your machine.
- A Unix‑like terminal (Linux, WSL, macOS).

## ⚙️ Installation (Terraform)

On Ubuntu / WSL:

```bash
sudo apt update && sudo apt install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform -y
terraform -version
```
## 🚀 Usage

1. Clone this repository, then enter the project directory:
```bash
cd terraform-local-lab
```
2. Initialize (download local provider):
```bash
terraform init   
```
3. Plan the changes (see what will be created):
```bash
terraform plan  
```
4. Apply the changes (create `hello.txt`):
```bash
terraform apply -auto-approve 
```
5. Verify the file was created:
```bash
cat hello.txt 
```
    You’ll see content like:
    Hello from Terraform! This file was created at 2026-05-08T17:23:45Z.

6. Delete the file manually and re‑apply to prove self‑healing:
```bash
rm hello.txt
terraform apply -auto-approve
cat hello.txt   # file is back
```
7. Finally, clean up by destroying the resource:
```bash
terraform destroy -auto-approve 
```

## 📖 What I Learned
1. The terraform init step downloads the required provider(s).
2. plan shows what will happen without making changes.
3. apply enforces the desired state.
4. Terraform is idempotent – running it multiple times doesn’t duplicate resources.
5. The terraform destroy command removes everything that was created.


## Next Steps
1. Replace the local_file with the AWS provider and define an EC2 instance.
2. Add variables for instance type, AMI, and region.
3. Integrate with Ansible to configure the instance after provisioning.
4. Run the same workflow in a GitLab CI pipeline.


## Day 19 Summary
This local lab was a great introduction to Terraform’s core workflow. I now understand how to define infrastructure as code, manage resources, and ensure idempotence. The next step is to apply these concepts to real cloud resources and integrate with configuration management tools like Ansible.

----

# Day 20: Terraform AWS Lab – EC2 Instance Definition

This project contains a **Terraform configuration** that defines an AWS EC2 instance with a security group, an AMI lookup, and a startup script (user_data) that installs Nginx.

**Currently the configuration is validated but not applied**, because AWS credentials are needed for `terraform plan` / `apply`. It will be provisioned after my exams.

## 📌 What This Configuration Does

- Defines the AWS provider (region `us-east-1`).
- Looks up the latest Amazon Linux 2023 AMI with a data source.
- Creates a security group allowing SSH (22) and HTTP (80) from anywhere.
- Creates a `t2.micro` EC2 instance (free tier eligible) with:
  - The AMI from the data source.
  - A simple `user_data` script that installs and starts Nginx.
- Outputs the public IP and a ready‑to‑use SSH command.

## 🧰 Tools & Concepts

| Area                | Technology                 |
|---------------------|----------------------------|
| Provisioning        | Terraform (HCL)            |
| Provider            | `hashicorp/aws` (~> 5.0)  |
| Resources           | `aws_instance`, `aws_security_group` |
| Data Source         | `aws_ami`                  |
| Outputs             | `public_ip`, `ssh_command` |

## 📁 Project Structure

terraform-aws-lab/
├── main.tf # Terraform configuration
└── README.md


## 🔧 Prerequisites

- Terraform ≥ 1.0 installed.
- An AWS account and valid credentials configured (for future `apply`).

## 🚀 Usage (after credentials are set)

1. Clone the repository and enter this directory:
```bash
   cd terraform-aws-lab
```
2. Initialize Terraform (download AWS provider):
```bash
    terraform init
```
3. Plan the changes (see what will be created):
```bash
    terraform plan
```
4. Apply the changes (provision the EC2 instance):
```bash
    terraform apply -auto-approve
```
5. Wait a minute, then check the website:
    - curl http://<public_ip>
    You should see: This instance is managed by Terraform.

6. SSH into the instance:
```bash
    ssh -i <your_key.pem> ec2-user@<public_ip>
```
7. Finally, clean up by destroying the resources:
```bash
    terraform destroy -auto-approve
```

## 🧪 Validation (Playwright)
A Playwright test is prepared in the sister PlayWrightCode repository:

```python
def test_ec2_nginx(page):
    url = os.environ.get("EC2_PUBLIC_IP", "http://localhost")
    page.goto(url)
    expect(page.locator("h1")).to_contain_text("This instance is managed by Terraform")
This test will be run after the EC2 instance is provisioned, using the public IP output by Terraform.
```

## 📖 What I Learned
1. terraform validate checks the syntax and completeness of the configuration without needing credentials.
2. terraform plan connects to the real API to resolve data sources and validate the full plan, so it requires authenticated access.
3. The AWS provider’s user_data argument can run bootstrap scripts that replace manual SSH configuration.
4. This configuration is a direct cloud counterpart to the Ansible playbook I wrote earlier – together they form a complete Infrastructure as Code pipeline.

## Next Steps
1. Set up AWS Free Tier after exams.
2. Run terraform apply and see the EC2 instance in the AWS console.
3. Use Ansible to customize the instance further (e.g., deploy the SELinux demo page).
4. Run Playwright tests from a GitLab CI pipeline against the live public IP.