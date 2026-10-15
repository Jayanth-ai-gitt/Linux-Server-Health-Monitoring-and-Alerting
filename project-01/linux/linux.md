# 🐧 Linux Fundamentals for DevOps Freshers

Linux runs most servers, containers and CI runners. If you can move around a terminal, read logs and fix a broken service, you are already ahead of most freshers.

> 💡 **How to use this guide:** open a terminal (Ubuntu VM, WSL, or an EC2 instance) and *type every command yourself*. Reading is not enough.

## 📑 Table of Contents
1. [Files & Directories](#1-files--directories)
2. [Viewing & Searching Files](#2-viewing--searching-files)
3. [Permissions & Ownership](#3-permissions--ownership)
4. [Disk, Memory & CPU](#4-disk-memory--cpu)
5. [Processes](#5-processes)
6. [Services (systemd)](#6-services-systemd)
7. [Networking & Remote Access](#7-networking--remote-access)
8. [Text Processing: grep, awk, sed](#8-text-processing-grep-awk-sed)
9. [Redirection & Pipes](#9-redirection--pipes)
10. [Package Management](#10-package-management)
11. [Cron Jobs](#11-cron-jobs)
12. [Mounting Disks](#12-mounting-disks)
13. [Troubleshooting Checklist](#13-troubleshooting-checklist)
14. [Practice Tasks](#14-practice-tasks)

---

## 1. Files & Directories

| Command | What it does |
|---------|--------------|
| `pwd` | Show current directory |
| `ls -lah` | List files (long, all, human-readable sizes) |
| `cd /var/log` | Change directory (`cd ~` home, `cd -` previous) |
| `mkdir -p app/logs` | Create nested directories |
| `touch notes.txt` | Create empty file |
| `cp -r src/ backup/` | Copy a directory |
| `mv old.txt new.txt` | Move / rename |
| `rm file.txt` / `rm -r dir/` | Delete file / directory |
| `cat /etc/os-release` | Show OS details |

⚠️ **Careful:** there is no recycle bin. Never run `rm -rf /` or `rm -rf *` unless you are 100% sure where you are (`pwd` first!).

---

## 2. Viewing & Searching Files

```bash
cat file.txt            # print whole file
less big.log            # scroll (q to quit)
head -n 20 file.txt     # first 20 lines
tail -n 50 app.log      # last 50 lines
tail -f app.log         # follow a log live  ← used daily in DevOps
find /var/log -name "*.log" -mtime -1   # log files changed in last day
grep -rn "ERROR" /var/log/app/          # search text recursively
```

✅ **Real-world:** `tail -f` + `grep` is how you watch a deployment for errors in real time:
```bash
tail -f /var/log/nginx/error.log | grep -i "upstream"
```

---

## 3. Permissions & Ownership

```bash
ls -l
# -rwxr-xr-- 1 ubuntu devs 1234 Jan 1 12:00 deploy.sh
#  │└┬┘└┬┘└┬┘
#  │ │  │  └─ others: r--  (read)
#  │ │  └──── group:  r-x  (read + execute)
#  │ └─────── owner:  rwx  (read + write + execute)
#  └───────── file type (- file, d directory)
```

Numeric form: **r = 4, w = 2, x = 1**

| Mode | Meaning | Typical use |
|------|---------|-------------|
| `755` | owner rwx, others r-x | scripts, directories |
| `644` | owner rw-, others r-- | normal files |
| `600` | owner rw- only | **SSH private keys** |

```bash
chmod +x deploy.sh            # make a script executable
chmod 600 ~/.ssh/id_ed25519   # SSH refuses keys that are too open
chown ubuntu:devs deploy.sh   # change owner:group
sudo <command>                # run as root (use sparingly)
```

---

## 4. Disk, Memory & CPU

```bash
df -h            # disk space per filesystem
du -sh /var/log/*   # which folder is eating space?
free -m          # RAM in MB (look at "available", not "free")
top              # live processes (q to quit)   — htop is nicer if installed
uptime           # load average
lscpu            # CPU info
nproc            # number of CPU cores
```

**Reading `df -h`:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/xvda1       50G   20G   30G  40% /
```
If `Use%` is near 100% services start failing (logs can't be written, DB crashes). Check disk **before** a deployment.

**Disk full? Find the culprit:**
```bash
sudo du -ah /var | sort -rh | head -n 10
```

---

## 5. Processes

```bash
ps aux                       # all processes
ps aux | grep nginx          # find a specific one
kill 1234                    # polite stop (SIGTERM)  ← try this first
kill -9 1234                 # force kill (SIGKILL)   ← last resort
pkill -f myscript.sh         # kill by name
nohup ./script.sh > out.log 2>&1 &   # run in background, survive logout
jobs                         # background jobs in this shell
```

⚠️ **Why not always `kill -9`?** It gives the process no chance to close files or connections cleanly, which can corrupt data. Use plain `kill` first.

---

## 6. Services (systemd)

Most modern Linux distros manage services with `systemctl`.

```bash
sudo systemctl status nginx      # is it running? last log lines
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl enable nginx      # start automatically on boot
journalctl -u nginx -n 50        # last 50 log lines for that service
journalctl -u nginx -f           # follow live
journalctl -xe                   # recent system errors
```

---

## 7. Networking & Remote Access

```bash
ip a                      # IP addresses
ping -c 4 google.com      # basic connectivity (4 packets)
curl -I https://example.com        # HTTP headers only
curl -s localhost:5000/health      # test an API from the server itself
ss -tulnp                 # open/listening ports (modern replacement for netstat)
nslookup example.com      # DNS lookup
traceroute example.com    # path packets take
ssh -i key.pem ubuntu@<server-ip>              # log in remotely
scp -i key.pem app.tar.gz ubuntu@<server-ip>:/home/ubuntu/   # copy file to server
```

**"Port 80 not reachable" checklist:**
1. Is the service running? → `systemctl status`
2. Is it listening? → `ss -tulnp | grep :80`
3. Is a firewall / **AWS Security Group** blocking it?

---

## 8. Text Processing: grep, awk, sed

```bash
grep "ERROR" app.log                 # lines containing ERROR
grep -c "ERROR" app.log              # count them
grep -i -v "debug" app.log           # ignore case, exclude "debug"
awk '{print $1}' access.log          # print column 1 (e.g. client IP)
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head   # top 10 IPs
sed 's/old/new/g' file.txt           # replace (prints result)
sed -i 's/8080/9090/g' config.conf   # replace IN the file
```

✅ **Real-world:** quickly find which IPs hit your server most, or change a port across a config file.

---

## 9. Redirection & Pipes

| Syntax | Meaning |
|--------|---------|
| `cmd > file` | write output (overwrite) |
| `cmd >> file` | append output |
| `cmd 2> err.log` | write only errors |
| `cmd > out.log 2>&1` | write output **and** errors to same file |
| `cmd1 \| cmd2` | send output of cmd1 into cmd2 |

---

## 10. Package Management

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y nginx

# RHEL / CentOS / Amazon Linux
sudo yum install -y nginx      # (dnf on newer versions)
```
Always run `apt update` first so you get the latest package list.

---

## 11. Cron Jobs

```bash
crontab -e     # edit your schedule
crontab -l     # list it
```

```
* * * * *  /path/to/command
│ │ │ │ │
│ │ │ │ └── day of week (0-6, Sunday = 0)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```

| Entry | Runs |
|-------|------|
| `0 2 * * * /opt/backup.sh` | every day at 2:00 AM |
| `*/5 * * * * /opt/check.sh` | every 5 minutes |
| `0 0 * * 0 /opt/weekly.sh` | every Sunday midnight |

💡 Always use **full paths** in cron and redirect output so you can debug: `... >> /var/log/backup.log 2>&1`

---

## 12. Mounting Disks

```bash
lsblk                         # list disks (find the new one, e.g. /dev/xvdf)
sudo mkfs -t ext4 /dev/xvdf   # format (ONLY for a brand-new empty disk!)
sudo mkdir /data
sudo mount /dev/xvdf /data    # mount now
df -h                         # verify
```
To survive reboot, add a line to `/etc/fstab`, then test it with `sudo mount -a`:
```
UUID=<uuid-from-blkid>  /data  ext4  defaults,nofail  0  2
```
> ⚠️ A typo in `/etc/fstab` can stop the server from booting. Always use `nofail` and run `sudo mount -a` before rebooting.

---

## 13. Troubleshooting Checklist

When "something is broken", work top to bottom:

| Step | Command | Question |
|------|---------|----------|
| 1 | `df -h` | Is the disk full? |
| 2 | `free -m`, `top` | Out of memory / CPU maxed? |
| 3 | `systemctl status <svc>` | Is the service running? |
| 4 | `journalctl -u <svc> -n 50` / `tail app.log` | What do the logs say? |
| 5 | `ss -tulnp` | Is the port listening? |
| 6 | `curl localhost:<port>` | Does it work locally? |
| 7 | `ping` / Security Group / firewall | Is the network blocking it? |
| 8 | `dmesg \| tail` | Kernel-level errors (OOM killer, disk errors)? |

Advanced: `strace -p <PID>` shows the system calls of a running process.

---

## 14. Practice Tasks

Do these on a VM and keep a note of what you learned:

1. Create `~/practice/logs` and a file `app.log` with 10 lines (some containing `ERROR`). Count the errors with `grep`.
2. Write a script `hello.sh` that prints the date, make it executable and run it.
3. Schedule it with cron to run every minute, and confirm via the output file.
4. Install `nginx`, start it, enable it on boot, and `curl localhost`.
5. Stop nginx, then find the reason using `systemctl status` and `journalctl`.
6. Find the 5 largest folders under `/var` using `du`.
7. Set permissions `600` on a file and verify with `ls -l`.

➡️ Next: put these skills to use in [`project-02`](../../project-02-dockerized-app-cicd/) — a Dockerized app with a CI pipeline and a health-check script.
