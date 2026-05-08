
### Day 1 – 2026-04-19

**Project:** homelab (Rocky Linux 9)  

**What I did:** Installed Rocky Linux 9 as a virtual machine. Learned SELinux basics: contexts, DAC vs MAC, and commands `ls -lZ`, `ps axZ`. Deployed a custom Nginx page from `/webroot/html/`. Hit a 403 Forbidden error because the file lacked the `httpd_sys_content_t` type. Used `semanage fcontext` and `restorecon` to fix it permanently.  

**Key commands:** `ls -lZ /webroot/html/index.html`, `semanage fcontext -a -t httpd_sys_content_t "/webroot/html(/.*)?"`, `restorecon -Rv /webroot/html`, `ausearch -m avc -ts recent`  

**What I learned:** SELinux denials are logged in `/var/log/audit/audit.log`, not `journalctl`. Always restore contexts instead of disabling SELinux.  

**Next:** SSH and firewalld hardening.

----

### Day 2 – 2026-04-20

**Project:** homelab (Rocky Linux 9)  

**What I did:** Configured SSH access. Switched VM network from NAT to Bridged for direct connectivity. Set up SSH key‑based authentication from Windows PowerShell and disabled password login. Used firewalld to open HTTP and restricted SSH to a single management IP with a rich rule.  

**Key commands:** `ssh-keygen -t ed25519`, `ssh-copy-id mayank@192.168.1.13`, `systemctl restart sshd`, `firewall-cmdpermanentadd-rich-rule='rule family="ipv4" source address="192.168.1.12" service name="ssh" accept'`, `firewall-cmdreload`  

**What I learned:** SSH is bidirectional if the firewall allows it; Windows Firewall blocked incoming SSH until I enabled OpenSSH Server. Firewalld rich rules create zero‑trust access.  

**Next:** Users, groups, and sudoers.

----

### Day 3 – 2026-04-21

**Project:** homelab (Rocky Linux 9)  

**What I did:** User and group administration. Created users Alice, Bob, Charlie and assigned them to groups `developers`, `webadmins`, `wheel`. Explored `/etc/passwd`, `/etc/shadow`, `/etc/group`. Applied password aging with `chage` and locked/unlocked accounts with `usermod`.

**Key commands:** `useradd -m -g developers -s /bin/bash alice`, `groupadd developers`, `usermod -L alice`, `chage -M 90 alice`, `cat /etc/passwd`, `cat /etc/shadow` 

**What I learned:** One `useradd` updates multiple files. The shadow file stores hashed passwords; only root can read it. 

**Next:** System monitoring and logs.

----

### Day 4 – 2026-04-22

**Project:** homelab (Rocky Linux 9) 

**What I did:** Installed `htop`, `ncdu`, `glances` for real‑time monitoring. Analyzed logs with `journalctl` (priority filters, time ranges, failed SSH attempts). Parsed Nginx access logs with `awk` after discovering the log was empty – first needed to generate traffic with `curl`. Wrote a disk usage alert script and scheduled it via `cron`.  

**Key commands:** `journalctl -p 3 -b`, `awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr`, `crontab -e`, `/usr/local/bin/check_disk.sh`  

**What I learned:** An empty log isn’t broken; the service simply hadn’t received requests. Monitoring requires both real‑time tools and automated alerts. 

**Next:** Log rotation and backups.

----

### Day 5 – 2026-04-23

**Project:** homelab (Rocky Linux 9)  

**What I did:** Configured `logrotate` for Nginx logs (daily rotation, 14‑day retention, compression, postrotate script). Wrote a backup script that creates a timestamped `.tar.gz` of `/webroot/html`, Nginx config, and logrotate config, then copies it to Windows via `scp`. Scheduled the backup in `crontab`.  

**Key commands:** `logrotate -f /etc/logrotate.conf`, `tar -czf backup.tar.gz /webroot/html`, `scp backup.tar.gz mayank@192.168.1.12:C:/Users/mayank/Desktop/backups/`, `crontab -e`  

**What I learned:** Backups must leave the server. `logrotate` prevents disk bloat. The backup script must be executable and use absolute paths.  

**Next:** Cron vs systemd timers, bulk user creation.

----

### Day 6 – 2026-04-24

**Project:** homelab & Ansible prep  

**What I did:** Scheduled the backup script with both `cron` and a `systemd` timer. Created a bulk user creation script that reads a CSV file (`users.csv`), creates groups if missing, adds users, sets temporary passwords, and forces password expiry. 

**Key commands:** `systemctl enable backup-web.timer`, `systemctl start backup-web.timer`, `bash /usr/local/bin/bulk-user-create.sh`, `chpasswd`, `passwdexpire`  

**What I learned:** Systemd timers are a modern cron alternative with better logging and handling of missed runs. Scripts for user provisioning are the first step toward Infrastructure as Code.  

**Next:** Git & GitHub for homelab scripts.

----

### Day 7 – 2026-04-26

**Project:** homelab & Git  

**What I did:** Initialized a Git repository `linux-homelab` containing all scripts and the SELinux demo page. Pushed to GitHub and mirrored to GitLab. Added a `.gitignore` and `README.md`.  

**Key commands:** `git init`, `git remote add origin https://github.com/Mayankk0608/linux-homelab.git`, `git push -u origin main`, `git remote add gitlab https://gitlab.com/Mayankk0608/linux-homelab.git`, `git push gitlab main`  

**What I learned:** Version control turns a local homelab into a public portfolio. Multiple remotes allow separate workflows (GitHub for visibility, GitLab for CI/CD).  

**Next:** LVM – disk management.

----

### Day 8 – 2026-04-28

**Project:** homelab (Rocky Linux 9)  

**What I did:** Added a second virtual disk (1 GB) to the Rocky VM for LVM practice. Discovered the disk naming flipped: new disk became `sda`, original system disk `sdb`. Safely created a Physical Volume, Volume Group, and Logical Volume. Extended the LV and resized the filesystem live.  

**Key commands:** `pvcreate /dev/sda`, `vgcreate vg_data /dev/sda`, `lvcreate -L 500M -n lv_webdata vg_data`, `lvextend -L 900M /dev/vg_data/lv_webdata`, `resize2fs /dev/vg_data/lv_webdata`  

**What I learned:** Always check `lsblk` before running destructive commands. LVM allows online disk growth without reboot – critical for cloud VMs.  

**Next:** cgroups – container resource limits.

----

### Day 9 – 2026-04-29

**Project:** homelab (Rocky Linux 9)  

**What I did:** Explored cgroups v2. Checked my shell’s cgroup path via `/proc/self/cgroup`. Ran a process with a memory cap using `systemd-run MemoryMax=50M`. Observed the kernel enforce the limit.  

**Key commands:** `cat /proc/self/cgroup`, `ls /sys/fs/cgroup/`, `systemd-cgls`, `sudo systemd-runscope -p MemoryMax=50M bash`  

**What I learned:** Docker’s memory` flag relies on cgroups. Understanding cgroups helps debug OOM kills in Kubernetes.  

**Next:** `strace` – tracing system calls.

----

### Day 10 – 2026-04-30

**Project:** homelab (Rocky Linux 9)  

**What I did:** Attached `strace` to nginx workers. First attachment showed nothing because the `curl` hit the other worker. Learned that `-f` on the master doesn’t trace existing children. Finally started nginx under `strace` and captured the full HTTP lifecycle in real time.  

**Key commands:** `strace -p $(pgrep -f "nginx: worker" | head -1) -e trace=accept,read,write`, `sudo strace -f -e trace=accept4,read,write nginx -g "daemon off;"`, `curl http://localhost` 

**What I learned:** `strace` only shows syscalls as they happen. Multi‑process services require tracing all workers or starting under strace. Cleanly detach with Ctrl+C.  

**Next:** `lsof` and `fuser` for port/file detection.

----

### Day 11 – 2026-05-01

**Project:** homelab (Rocky Linux 9)  

**What I did:** Used `lsof` and `fuser` to list processes using port 80 and the nginx access log. Ignored harmless FUSE warnings. Verified that after stopping nginx, the port was free. 

**Key commands:** `sudo lsof -i :80`, `sudo lsof /var/log/nginx/access.log`, `sudo fuser -v 80/tcp`, `sudo systemctl stop nginx && sudo lsof -i :80`  

**What I learned:** `lsof` and `fuser` are the quickest ways to identify which process holds a port or file. The FUSE warnings are cosmetic.  

**Next:** iptables/nftables and firewall internals.

----

### Day 12 – 2026-05-02

**Project:** homelab (Rocky Linux 9)  

**What I did:** Explored `iptables` and discovered that Rocky 9 uses `nftables` natively. `iptables -L` showed empty chains; `nft list table inet firewalld` revealed the real rules. Added an IPv4 DROP rule for port 80 but `curl` still succeeded because IPv6 traffic bypassed it.  

**Key commands:** `sudo iptables -L -n -v`, `sudo nft list table inet firewalld`, `sudo iptables -A INPUT -p tcpdport 80 -j DROP`, `curl -6 http://localhost`, `sudo ip6tables -A INPUT -p tcpdport 80 -j DROP`  

**What I learned:** Firewall rules must cover both IPv4 and IPv6. Firewalld writes native nftables rules, not legacy iptables. 

**Next:** Remote access with Tailscale mesh VPN.

----

### Day 13 – 2026-05-02 (continued)

**Project:** homelab networking  

**What I did:** Furthered the iptables/nftables session. Created a `ufw` rule to allow Tailscale SSH. Verified that `firewall-cmdlist-all` shows front‑end policies, while the backend is nftables.  

**Key commands:** `sudo ufw allow from 100.0.0.0/8 to any port 22 proto tcp`, `sudo ufw status verbose`, `sudo firewall-cmdremove-service=sshpermanent`, `sudo firewall-cmdreload`  

**What I learned:** Tailscale’s interface is automatically in the trusted zone on Rocky, but Ubuntu’s `ufw` requires explicit rules.  

**Next:** Tailscale global homelab.

----

### Day 14 – 2026-05-03

**Project:** Tailscale & cross‑machine SSH  

**What I did:** Installed Tailscale on Rocky VM, Ubuntu WSL, and Windows. Initially machines couldn’t see each other because Rocky used a GitHub login and Ubuntu used a Gmail login – two separate tailnets. Unified the accounts. Ubuntu’s `ufw` blocked inbound Tailscale SSH; allowed the 100.0.0.0/8 range. Direct `tailscale ping` timed out due to NAT, but traffic relayed through DERP and SSH worked in both directions.  

**Key commands:** `sudo tailscale up`, `tailscale status`, `tailscale ip -4`, `sudo ufw allow from 100.0.0.0/8 to any port 22 proto tcp`, `ssh mayank@100.72.14.56`, `tailscale ping 100.72.14.56`  

**What I learned:** Tailscale’s IP changes on logout/login. `tailscale ping` tests direct WireGuard; relayed connections still work. A mesh VPN makes the homelab global without port forwarding.  

**Next:** Network namespaces (container networking).

----

### Day 15 – 2026-05-04

**Project:** homelab (Linux kernel)  

**What I did:** Created two network namespaces (`blue` and `red`), a `veth` pair, assigned IPs, and pinged across them. Verified the host could not see the namespace IPs. Cleaned up with `ip netns delete`.  

**Key commands:** `sudo ip netns add blue`, `sudo ip link add veth-blue type veth peer name veth-red`, `sudo ip netns exec blue ip addr add 10.0.0.1/24 dev veth-blue`, `sudo ip netns exec blue ping 10.0.0.2`, `sudo ip netns delete blue red`  

**What I learned:** Docker / Kubernetes use exactly this mechanism (namespaces + veth pairs) to give containers their own network stacks.  

**Next:** Playwright & test automation.

----

### Day 16 – 2026-05-05

**Project:** PlayWrightCode 

**What I did:** Built a Playwright‑pytest automation suite in a Python venv. Wrote `conftest.py` with `yield`‑based fixtures, a test to search Google, a script to hit my containerised Django app by IP. Installed all dependencies, froze them to `requirements.txt`, generated HTML reports. Pushed to GitHub and GitLab.  

**Key commands:** `pip install -r requirements.txt`, `playwright install`, `pytest tests/test_google.pyheadedbrowser=chromiumhtml=report.html`, `git push`, `pip freeze > requirements.txt`  

**What I learned:** Cross‑platform Python requires different activation commands. Playwright can validate not just apps but infrastructure endpoints – synthetic monitoring.  

**Next:** Ansible – Infrastructure as Code.

----

### Day 17 – 2026-05-06

**Project:** Ansible-lab  

**What I did:** Wrote an Ansible playbook to configure Rocky VM: install nginx, firewalld, create webroot, deploy SELinux demo page, set SELinux contexts, open HTTP, start services. Overcame `Missing sudo password` with ask-become-pass`. Found that `copy` module `src` must exist on the control node, so pulled the HTML from Rocky via `scp`. Deliberately destroyed nginx and firewalld, re‑ran the playbook, and the server self‑healed. Validated with Playwright.  

**Key commands:** `ansible-playbook -i inventory.ini site.ymlask-become-pass`, `curl -I http://100.72.14.56`, `scp mayank@100.72.14.56:/webroot/html/index.html ./selinux-demo.html`, `pytest tests/test_selinux.py`  

**What I learned:** Ansible is idempotent; a playbook can repair a broken server. The control node must have all source files.

**Next:** Variables and templates.

----

### Day 18 – 2026-05-07

**Project:** Ansible-lab & PlayWrightCode  

**What I did:** Refactored the playbook with variables in `group_vars/rocky.yml`. Converted the static HTML to a Jinja2 template that inserts the server’s hostname. Fixed the Nginx root path persistence with `lineinfile`. Added a `reload nginx` handler. Updated Playwright test to assert the hostname – test passed after the config fix. 

**Key commands:** `ansible-playbook -i inventory.ini site.yml`, `pytest tests/test_selinux2.py`, `lineinfile` module, `template` module, creation of `group_vars/rocky.yml` and `templates/index.html.j2`  

**What I learned:** Every manual edit must be a playbook task. Variables and templates make the playbook portable and reusable. Handlers apply configuration changes safely.  

**Next:** Cross‑platform roles (Rocky + Ubuntu).

----

### Day 19 – 2026-05-08

**Project:** terraform-local-lab & PlayWrightCode

**What I did:** Installed Terraform on Ubuntu WSL. Created a local Terraform project with a `local_file` resource – no cloud provider needed. Ran the full workflow: `init`, `plan`, `apply`, verified the file was created, manually deleted it, re‑applied to prove self‑healing, then `destroy`. Set up a placeholder Playwright test for future infrastructure endpoints.

**Key commands:** `terraform init`, `terraform plan`, `terraform apply -auto-approve`, `terraform destroy -auto-approve`, `cat hello.txt`

**What I learned:** The Terraform workflow is identical whether managing local files or cloud resources. Infrastructure as Code means declaring the desired state; the tool figures out how to achieve it.

**Next:** Write a Terraform config for an AWS EC2 instance (free tier) and plan it without applying.

----

### Day 20 – 2026-05-09

**Project:** terraform-aws-lab & PlayWrightCode

**What I did:** Created a Terraform configuration for an AWS EC2 instance with a security group, AMI data source, and user_data script to install Nginx. Ran `terraform init` and `terraform validate` successfully. Learned that `terraform plan` requires valid AWS credentials because it queries live APIs. Prepared a Playwright test to verify the deployed instance once live.

**Key commands:** `terraform init`, `terraform validate`, `terraform plan` (intentionally failed), creation of `main.tf`, `variables.tf`

**What I learned:** Terraform separates syntax validation (`validate`) from infrastructure planning (`plan`). Real cloud provisioning needs authenticated API access. Declarative configuration maps exactly to what will exist in the cloud.

**Next:** After exams – AWS account setup + `terraform apply` with real resources.