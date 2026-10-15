# 🔁 CI/CD Tools for DevOps Freshers

## 1. What are CI and CD?

| Term | Meaning | Example |
|------|---------|---------|
| **CI** – Continuous Integration | Every code push is automatically built and tested | PR triggers lint + unit tests |
| **CD** – Continuous Delivery | Every passing build is *ready* to deploy (one click) | Image pushed to registry, deploy is manual approval |
| **CD** – Continuous Deployment | Every passing build is deployed *automatically* | Merge to `main` → live in production |

**Why?** Catch bugs early, release smaller changes more often, remove manual (error-prone) steps.

## 2. A typical pipeline

```
Commit ─▶ Build ─▶ Test ─▶ Package (Docker image) ─▶ Push to registry ─▶ Deploy ─▶ Monitor
```

| Stage | Tools |
|-------|-------|
| Source | Git, GitHub, GitLab |
| Build/Test | Maven, npm, pytest |
| Package | Docker |
| Registry | Docker Hub, AWS ECR |
| Deploy | AWS ECS/EC2, Kubernetes, Ansible |
| Provision | Terraform, CloudFormation |
| Monitor | Prometheus, Grafana, CloudWatch |

## 3. GitHub Actions (start here — it's free and built into GitHub)

**Vocabulary**
- **Workflow** – a YAML file in `.github/workflows/`
- **Event / trigger** – what starts it (`push`, `pull_request`, `schedule`)
- **Job** – a group of steps running on one runner (machine)
- **Step** – one command (`run:`) or a reusable action (`uses:`)
- **Runner** – the VM that executes the job (`ubuntu-latest`)
- **Secrets** – encrypted values (Settings → Secrets and variables → Actions)

**Minimal example**
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements-dev.txt
      - run: pytest -v
```

**Using a secret safely**
```yaml
- name: Login to Docker Hub
  run: echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u "${{ secrets.DOCKERHUB_USER }}" --password-stdin
```
Never hardcode passwords in YAML.

➡️ A working example: [`project-02-dockerized-app-cicd`](../../.github/workflows/project-02-ci.yml)

## 4. Jenkins (very common in companies)

Jenkins is a self-hosted automation server. Pipelines are written in a `Jenkinsfile`.

```groovy
pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test')     { steps { sh 'pip install -r requirements-dev.txt && pytest' } }
    stage('Build')    { steps { sh 'docker build -t myapp:${BUILD_NUMBER} .' } }
  }
  post {
    failure { echo 'Build failed!' }
  }
}
```

Run Jenkins quickly with Docker:
```bash
docker run -d -p 8080:8080 -v jenkins_home:/var/jenkins_home --name jenkins jenkins/jenkins:lts
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## 5. GitHub Actions vs Jenkins

| | GitHub Actions | Jenkins |
|--|----------------|---------|
| Hosting | Managed by GitHub | You install & maintain |
| Config | YAML in repo | `Jenkinsfile` (Groovy) |
| Setup effort | Very low | Higher |
| Flexibility / plugins | Marketplace actions | Huge plugin ecosystem |
| Good for | Projects on GitHub | Large/custom enterprise setups |

## 6. Best practices
- Keep pipelines **fast** (cache dependencies, run lint before slow tests).
- **Fail fast** and make the failure message obvious.
- Store secrets in the CI secret store — never in Git.
- Pin versions (`actions/checkout@v4`, `python:3.12-slim`) for repeatable builds.
- Tag images with the commit SHA, not only `latest`.
- Require passing CI before merging (branch protection).

## 7. Practice
1. Create a workflow that prints "Hello CI" on every push.
2. Add a test job; break a test and watch the pipeline fail.
3. Add a `docker build` job that runs only after tests pass (`needs:`).
4. Install Jenkins in Docker and create a "Freestyle" job that runs `echo hello`.
