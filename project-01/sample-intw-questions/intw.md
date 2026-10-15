# 🎤 DevOps Fresher Interview Questions (with short answers)

Practise answering **out loud** in your own words. Short answers below are a starting point.

## Linux
**1. How do you check disk space and find what's using it?**
`df -h` for filesystems, `du -sh /var/* | sort -rh | head` for the biggest folders.

**2. A service isn't responding. What do you do?**
`systemctl status <svc>` → `journalctl -u <svc> -n 50` → `ss -tulnp` (is the port listening?) → `curl localhost:<port>` → check firewall/Security Group.

**3. Difference between `kill` and `kill -9`?**
`kill` sends SIGTERM (graceful shutdown). `kill -9` sends SIGKILL, which cannot be handled — use only if the process ignores SIGTERM.

**4. What does `chmod 755` mean?**
Owner read/write/execute (7), group and others read/execute (5).

**5. How do you watch a log live and filter for errors?**
`tail -f app.log | grep -i error`

**6. What's a cron job? Run a script daily at 2 AM.**
A scheduled task. `0 2 * * * /path/script.sh >> /var/log/script.log 2>&1`

## Git / GitHub
**7. `git merge` vs `git rebase`?**
Merge keeps history and adds a merge commit; rebase replays commits for a linear history. Don't rebase shared branches.

**8. `git reset` vs `git revert`?**
`reset` moves history back (rewrites it); `revert` adds a new commit that undoes a change — safe for pushed commits.

**9. How do you resolve a merge conflict?**
Open the file, choose the right code, remove `<<<<<<<` markers, `git add`, then commit/continue.

**10. You committed a password by mistake. What now?**
Rotate/revoke the password immediately, remove it from the code, and clean history if needed. Deleting it in a later commit isn't enough.

## CI/CD
**11. What is CI/CD?**
CI automatically builds/tests every change; CD automatically delivers or deploys passing builds.

**12. Describe a pipeline you built.**
(Use project-02) "On every PR, GitHub Actions lints, runs pytest, builds the Docker image and smoke-tests `/health`."

**13. How do you handle secrets in a pipeline?**
CI secret store (GitHub Secrets / Jenkins credentials), injected as environment variables; never committed.

**14. GitHub Actions vs Jenkins?**
Actions is managed and YAML-based inside GitHub; Jenkins is self-hosted, highly customisable, needs maintenance.

## Docker
**15. Image vs container?**
Image = read-only template; container = running instance of an image.

**16. Why copy `requirements.txt` before the rest of the code in a Dockerfile?**
Layer caching: dependencies are reinstalled only when requirements change.

**17. Why run containers as non-root?**
Limits damage if the app is compromised.

**18. `CMD` vs `ENTRYPOINT`?**
`CMD` = default command (easily overridden); `ENTRYPOINT` = fixed executable, `CMD` supplies default arguments.

**19. How do you debug a container that keeps exiting?**
`docker ps -a`, `docker logs <name>`, `docker inspect`, run with `docker run -it <image> sh`.

## AWS
**20. Security Group vs NACL?**
Security Group: stateful, instance-level, allow rules only. NACL: stateless, subnet-level, allow and deny.

**21. IAM user vs role?**
User = long-term identity with credentials; role = temporary permissions assumed by services/users (e.g. EC2 reading S3 without keys).

**22. Public vs private subnet?**
Public has a route to an Internet Gateway; private doesn't (uses a NAT Gateway for outbound).

**23. What are EBS snapshots used for?**
Point-in-time backups of volumes, stored in S3, can create new volumes/AMIs.

**24. What does an Auto Scaling Group do?**
Keeps the desired number of healthy instances and scales in/out based on policies.

**25. S3 storage classes?**
Standard, Intelligent-Tiering, Standard-IA, Glacier tiers — cheaper for less frequent access.

## Scenario questions
- *Website is down after deployment* → check recent change, logs, service status, roll back (revert/previous image tag).
- *Server disk is 100% full* → `df -h`, `du` to find culprit, clear/rotate logs, extend EBS volume.
- *Can't SSH into EC2* → Security Group port 22, key permissions (`chmod 600`), correct user (`ubuntu`/`ec2-user`), public IP, instance status checks.
