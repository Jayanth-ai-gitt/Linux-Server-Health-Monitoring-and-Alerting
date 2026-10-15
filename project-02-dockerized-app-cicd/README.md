# 🐳 Project 02 — Dockerized App with CI Pipeline

A small, complete DevOps workflow you can finish in an afternoon:

```
 code ──▶ git push ──▶ GitHub Actions ──▶ lint ──▶ tests ──▶ docker build ──▶ smoke test
                                                                    │
                                        run locally with docker compose + health-check script
```

## 🧰 What you will practise
| Skill | Where |
|-------|-------|
| Git branching & PRs | your workflow around this repo |
| Python app + unit tests | `app/`, `tests/` |
| Docker (non-root, layer caching, HEALTHCHECK) | `Dockerfile` |
| Docker Compose | `docker-compose.yml` |
| Bash scripting & cron | `scripts/healthcheck.sh` |
| CI with GitHub Actions | `../.github/workflows/project-02-ci.yml` (repo root) |

## 📁 Structure
```
project-02-dockerized-app-cicd/
├── app/                  # Flask API (/, /health, /time)
├── tests/                # pytest tests
├── scripts/healthcheck.sh
├── Dockerfile
├── docker-compose.yml
└── requirements-dev.txt
```

## ▶️ Step-by-step

### 1. Run it locally (no Docker)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python app/app.py                 # open http://localhost:5000
```

### 2. Run the tests and linter
```bash
pytest -v
flake8 app tests --max-line-length=100
```

### 3. Run with Docker
```bash
docker build -t devops-demo .
docker run -d --name demo -p 5000:5000 devops-demo
curl localhost:5000/health        # {"status":"ok","version":"1.0.0"}
docker ps                         # STATUS shows (healthy) after a few seconds
docker logs demo
docker stop demo && docker rm demo
```

### 4. Or with Docker Compose
```bash
docker compose up -d --build
docker compose logs -f
docker compose down
```

### 5. Monitor it with the health-check script
```bash
./scripts/healthcheck.sh                       # exit code 0 = healthy
./scripts/healthcheck.sh http://localhost:5000/health
echo $?                                        # check the exit code
```
Run it every minute with cron:
```bash
crontab -e
* * * * * /full/path/to/scripts/healthcheck.sh >> /tmp/hc-cron.log 2>&1
```

### 6. See CI in action
1. Push this repo to GitHub. The workflow lives at the repo root in `.github/workflows/project-02-ci.yml` (GitHub only reads workflows from there) and runs inside this folder.
2. Open the **Actions** tab and watch `test` → `docker` run.
3. Break a test on purpose, push a PR, and see the check fail. Fix it and see it go green.

## 🧪 Challenges (make it yours)
1. Add a `/version` endpoint + a test for it.
2. Make `APP_ENV=prod` change the message on `/`.
3. Add a CI step that scans the image with `trivy` or `docker scout`.
4. Push the image to Docker Hub or **AWS ECR** from CI using GitHub Secrets.
5. Deploy the container on an **EC2** instance and test it through its Security Group.
6. Add Prometheus-style metrics (`prometheus_client`) at `/metrics`.

## 🧯 Troubleshooting
| Problem | Fix |
|---------|-----|
| `port is already allocated` | something uses 5000: `ss -tulnp \| grep 5000` or change `-p 5001:5000` |
| Container exits immediately | `docker logs demo` |
| `permission denied` on script | `chmod +x scripts/healthcheck.sh` |
| CI does not start | the workflow must be in `<repo root>/.github/workflows/` |
