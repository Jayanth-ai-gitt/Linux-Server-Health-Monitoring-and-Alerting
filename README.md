# DevOps Fresher Projects 🚀

A beginner-friendly learning path for DevOps freshers: concise notes, interview questions, and one hands-on project you can run and put on your resume.

## 🗺️ Learning Path

| Step | What | Where |
|------|------|-------|
| 1 | Linux commands & troubleshooting | [`project-01/linux`](project-01/linux/linux.md) |
| 2 | Git & GitHub workflow | [`project-01/github`](project-01/github/github.md) |
| 3 | AWS foundation services | [`project-01/aws-cloud`](project-01/aws-cloud/aws-cloud.md) |
| 4 | CI/CD concepts, GitHub Actions, Jenkins | [`project-01/ci-cd-tools`](project-01/ci-cd-tools/ci-cd-tools.md) |
| 5 | **Hands-on:** Dockerized app + CI pipeline | [`project-02-dockerized-app-cicd`](project-02-dockerized-app-cicd/README.md) |
| 6 | Interview practice | [`project-01/sample-intw-questions`](project-01/sample-intw-questions/intw.md) |

## 📁 Repository Structure
```
.
├── .github/workflows/project-02-ci.yml   # CI pipeline (lint → test → docker build → smoke test)
├── project-01/                           # Theory notes
│   ├── linux/
│   ├── github/
│   ├── aws-cloud/
│   ├── ci-cd-tools/
│   └── sample-intw-questions/
└── project-02-dockerized-app-cicd/       # Hands-on project
    ├── app/  tests/  scripts/
    ├── Dockerfile  docker-compose.yml
    └── README.md
```

## 🚀 Getting Started
```bash
git clone <your-fork-url>
cd devops-fresher-projects-main
```
You need: a Linux/WSL/macOS terminal, Git, Python 3.10+, and Docker. An AWS free-tier account helps for the cloud notes.

## 🧠 How to Study
1. Read a notes file, then do its **Practice Tasks** in a terminal — don't just read.
2. Build `project-02`, then finish the challenges at the end of its README.
3. Push your work to your own GitHub so recruiters can see the commit history and green CI checks.
4. Rehearse the interview questions out loud.

## 🔭 What to learn next
Terraform (IaC) · Kubernetes · Ansible · Prometheus + Grafana · AWS ECS/EKS · Helm.

## 🤝 Contributing
Found a typo or have an improvement? Open an issue or PR — see the Git notes for the workflow.
