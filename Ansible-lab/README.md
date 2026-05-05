#  Ansible‑Lab – Automated Web Server with SELinux

This project uses **Ansible** to configure a Rocky Linux 9 server as a production‑ready web server – idempotently, securely, and repeatably. It’s part of my self‑guided journey from Linux administration to Cloud & DevOps.

##  What This Playbook Does

- Installs and starts **nginx** + **firewalld**
- Creates a custom webroot (`/webroot/html`)
- Deploys a custom HTML page (SELinux context demo)
- Manages **SELinux** file contexts the enterprise way (no `setenforce 0`)
- Opens HTTP port 80 in **firewalld**
- Starts and enables services so they survive reboots

After running this playbook, the server is fully configured – no manual SSH steps required. Break the server, run the playbook again, and it **self‑heals**.

##  Tools & Concepts

| Area                | Technology / Idea                        |
|---------------------|------------------------------------------|
| Automation          | Ansible (agentless, SSH‑based)           |
| Operating System    | Rocky Linux 9                            |
| Connectivity        | Tailscale mesh VPN (private IP)          |
| Web Server          | Nginx                                    |
| Firewall            | firewalld                                |
| Security            | SELinux (`httpd_sys_content_t`)          |
| Idempotence         | All tasks can run multiple times safely  |
| Validation          | `curl -I`, Playwright / pytest           |

##  Project Structure
Ansible-lab/
├── inventory.ini # Hosts definition
├── site.yml # The main Ansible playbook
├── selinux-demo.html # The webpage to deploy
README.md


##  Prerequisites

- **Control node:** Ubuntu (WSL2) with Ansible installed
- **Managed node:** Rocky Linux 9 reachable via SSH (Tailscale IP `100.72.14.56`)
- Tailscale installed and authenticated on both control and managed nodes
- SSH key or password access to the managed node
- Password‑less `sudo` on the managed node **or** pass the become password on the command line

##  Installation & Setup

### 1. Install Ansible on the control node (Ubuntu WSL)

```bash
sudo apt update
sudo apt install ansible -y
ansible --version
```
### 2. Clone the repository and enter the project directory

```bash
git clone https://github.com/Mayankk0608/DevOps-Worklab.git
cd DevOps_Projects/Ansible-lab
```
### 3. Update the inventory file with your managed node’s Tailscale IP
```bash
Open `inventory.ini` and replace `
[webservers]
100.72.14.56 ansible_user=mayank` with your actual Tailscale IP address.
```

##  Usage and Validation

### Run the Ansible playbook
```bash
ansible-playbook -i inventory.ini site.yml --ask-become-pass
```
If you haven't set up password‑less sudo, add --ask-become-pass:

```bash
ansible-playbook -i inventory.ini site.yml --ask-become-pass
```

### Verify the web server is running
```bash
curl -I http://100.72.14.56
```

##  Breaking & Self‑Healing Test
```bash
ssh mayank@100.72.14.56
sudo dnf remove nginx firewalld -y
sudo rm -rf /webroot/html
exit
ansible-playbook -i inventory.ini site.yml
curl -I http://100.72.14.56    # 200 OK again!
```

## Playbook Breakdown (site.yml)

Task	                                   Module	                      Purpose
Install nginx       	                    dnf	                Ensure the Nginx package is present
Create webroot directory                	file	            Create /webroot/html if missing
Deploy SELinux demo page	                copy	            Copy the local HTML file to the server
Ensure proper SELinux context	            sefcontext	        Permanently set httpd_sys_content_t for the webroot; triggers restorecon
Install firewalld	                        dnf	                Ensure firewalld is present
Start & enable firewalld	                systemd	            Start firewalld and enable it at boot
Open HTTP port	                            firewalld	        Allow HTTP traffic (port 80) permanently
Start & enable nginx	                    systemd	            Start Nginx and enable it at boot
Handler: restorecon	                        command	            Relabel files under /webroot/html according to SELinux policy

## Common Issues Encountered & Solutions

Problem	Cause	Fix
Missing sudo password	The playbook uses become: true but Ansible has no password	Use --ask-become-pass or enable password‑less sudo on the target
src: selinux-demo.html not found	The file must exist on the control node, not the remote server	scp the file from Rocky to the Ansible project directory
Playwright test fails on Windows but passes in WSL	Tailscale is only installed inside WSL2, not on the Windows host	Install Tailscale on Windows or use the LAN IP for local testing

## End‑to‑End Validation (Playwright)

```python
from playwright.sync_api import expect
def test_selinux(page):
    page.goto("http://100.72.14.56")
    expect(page).to_have_title("SELinux Contexts | Rocky Linux 9 Demo")
```

## What I Learned

1. Ansible’s agentless architecture and idempotent modules.
2. The correct (RHEL‑way) to manage SELinux file contexts with sefcontext and restorecon.
3. Handling privilege escalation with become.
4. The importance of keeping source files (HTML, configs) inside the project directory.
5. Debugging cross‑platform network issues between WSL, Windows, and Tailscale.
6. How a single playbook can heal a server after deliberate destruction.

## Future Plans

1. Use variables and templates to make the playbook reusable across multiple servers.
2. Add roles for a Django app, database, and monitoring.
3.  Integrate with Terraform to provision cloud instances and then configure them with Ansible.