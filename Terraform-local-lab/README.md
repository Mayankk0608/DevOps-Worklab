# 🧱 Terraform Local Lab – First IaC Workflow

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
