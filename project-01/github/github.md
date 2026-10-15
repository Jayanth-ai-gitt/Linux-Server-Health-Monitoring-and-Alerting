# 🐙 Git & GitHub for DevOps Freshers

Git tracks changes to your code; GitHub hosts it and lets teams collaborate. Every CI/CD pipeline you will ever touch starts from a Git push.

## 📑 Contents
1. [Core Concepts](#1-core-concepts)
2. [First-Time Setup](#2-first-time-setup)
3. [Daily Workflow](#3-daily-workflow)
4. [Branching](#4-branching)
5. [Pull Requests](#5-pull-requests)
6. [Merge Conflicts](#6-merge-conflicts)
7. [Undoing Things Safely](#7-undoing-things-safely)
8. [SSH Keys](#8-ssh-keys)
9. [.gitignore & Secrets](#9-gitignore--secrets)
10. [Merge vs Rebase](#10-merge-vs-rebase)
11. [Best Practices](#11-best-practices)
12. [Practice Tasks](#12-practice-tasks)

---

## 1. Core Concepts

```
Working Directory ──git add──▶ Staging Area ──git commit──▶ Local Repo ──git push──▶ GitHub (remote)
        ▲                                                         │
        └────────────────────── git pull / git fetch ◀────────────┘
```

| Term | Meaning |
|------|---------|
| **Repository (repo)** | The project folder + its full history |
| **Commit** | A saved snapshot with a message |
| **Branch** | An independent line of work inside a repo |
| **Remote** | The copy hosted on GitHub (usually called `origin`) |
| **Pull Request (PR)** | A request to merge your branch into another, with review |

**Repo vs branch:** a repository holds the whole project and history; a branch is an isolated workspace *inside* that repo.

---

## 2. First-Time Setup

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase true       # optional: tidy history on pull
```

Start a project:
```bash
git init                         # new repo from scratch
git clone <repository-url>       # or copy an existing one
```

---

## 3. Daily Workflow

```bash
git status                       # what changed? (run this constantly)
git diff                         # see exact changes
git add file.txt                 # stage one file  (avoid blind `git add .`)
git commit -m "Add health check endpoint"
git push origin feature/health-check
git pull --rebase origin main    # sync with latest main
git log --oneline --graph        # compact history
git stash / git stash pop        # park unfinished work temporarily
```

✍️ **Good commit messages** are short and say *what* and *why*:
- ✅ `Fix crash when config file is missing`
- ❌ `changes`, `fix`, `asdf`

---

## 4. Branching

```bash
git switch -c feature/login      # create + switch (modern; same as checkout -b)
git switch main                  # switch back
git branch                       # list local branches
git merge feature/login          # merge into the branch you are on
git branch -d feature/login      # delete after merge
```

**Typical flow:** `main` is always deployable → create a branch per task → open a PR → review → merge → CI/CD deploys.

Naming: `feature/<name>`, `bugfix/<name>`, `hotfix/<name>`.

---

## 5. Pull Requests

1. Push your branch: `git push -u origin feature/login`
2. On GitHub click **Compare & pull request**.
3. Write a clear title/description, link the issue (`Closes #12`).
4. Wait for the **CI checks** (tests, lint) to go green.
5. Get a review, address comments, then **Merge**.

💡 Turn on **branch protection** for `main` (Settings → Branches): require PR + passing checks before merge.

---

## 6. Merge Conflicts

A conflict happens when two branches change the same lines. Git marks the file:

```
<<<<<<< HEAD
port = 8080
=======
port = 9090
>>>>>>> feature/login
```

Fix: edit the file, keep the correct version, **delete the markers**, then:
```bash
git add config.txt
git commit          # (or `git rebase --continue` if rebasing)
```

---

## 7. Undoing Things Safely

| Situation | Command |
|-----------|---------|
| Unstage a file | `git restore --staged file.txt` |
| Discard local edits to a file | `git restore file.txt` ⚠️ cannot be undone |
| Undo last commit, **keep** changes | `git reset --soft HEAD~1` |
| Undo last commit, **discard** changes | `git reset --hard HEAD~1` ⚠️ destructive |
| Undo a commit that is **already pushed** | `git revert <commit-hash>` ✅ safe, makes a new commit |
| Fix last commit message | `git commit --amend` (only if not pushed) |

🔑 **Rule:** never rewrite history (`reset`, `--amend`, force-push) on branches other people use. Use `revert` there.

Lost something? `git reflog` shows where HEAD has been — you can often recover.

---

## 8. SSH Keys

Authenticate to GitHub without typing a password.

```bash
ssh-keygen -t ed25519 -C "you@example.com"   # press Enter for defaults
cat ~/.ssh/id_ed25519.pub                    # copy this PUBLIC key
```
GitHub → **Settings → SSH and GPG keys → New SSH key** → paste.

```bash
ssh -T git@github.com            # test: should greet you by username
git clone git@github.com:<user>/<repo>.git
```
🔒 Never share or commit the **private** key (`id_ed25519`, no `.pub`).

---

## 9. .gitignore & Secrets

Files that should **not** be in Git: passwords, API keys, `.env`, `*.pem`, `node_modules/`, `__pycache__/`, build output.

```gitignore
.env
*.pem
__pycache__/
node_modules/
*.log
```

⚠️ If you accidentally commit a secret, **deleting it in a new commit is not enough** — it stays in history. Rotate/revoke the secret immediately.

---

## 10. Merge vs Rebase

| | `git merge` | `git rebase` |
|--|-------------|--------------|
| History | Keeps full branch history, adds a merge commit | Linear, "replays" your commits on top |
| Safe on shared branches? | ✅ Yes | ❌ No (rewrites history) |
| Use when | Merging a PR into `main` | Updating *your own* branch with latest `main` |

---

## 11. Best Practices

- One branch per task; small, focused commits.
- Never commit directly to `main` — use PRs.
- `git pull --rebase` before you push to avoid noisy merge commits.
- Never commit secrets.
- Let **GitHub Actions** run tests on every PR (see [`../ci-cd-tools/ci-cd-tools.md`](../ci-cd-tools/ci-cd-tools.md)).

---

## 12. Practice Tasks

1. Create a repo, add a `README.md`, push it.
2. Create `feature/add-script`, add a script, open a PR to `main` and merge it.
3. Create a deliberate merge conflict in two branches and resolve it.
4. Make a bad commit, then undo it with `git revert`.
5. Add a `.gitignore` and prove a `.env` file is ignored (`git status`).
