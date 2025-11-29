# fastapi-chatbot

This repository contains a simple FastAPI backend for a chatbot using Groq's LLM.

Important: Do NOT commit secrets (API keys, passwords) into this repository. This project now includes a `.gitignore` to exclude `.env` and the virtual environment.

Setup
1. Copy `backend/.env.example` to `backend/.env` and fill in your real API key locally.
2. Create a virtual environment and install requirements:

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r backend\requirements.txt
```

3. Run the app:

```powershell
python backend\app.py
```

Preparing to push to GitHub (recommended)
- Make sure `.env` is in your local `.gitignore` (already added).
- If you previously committed secrets, remove them from the git history (see instructions below).

Removing secrets from git history
1. If you accidentally committed a secret, remove it from the latest commit and untrack the file:

```powershell
git rm --cached backend/.env
git commit -m "Remove backend .env from repository"
```

2. To purge the secret from the entire history, use the BFG Repo Cleaner or `git filter-branch`. Example with BFG:

```powershell
# Install BFG: https://rtyley.github.io/bfg-repo-cleaner/
bfg --delete-files backend/.env
git reflog expire --expire=now --all; git gc --prune=now --aggressive
```

Creating a GitHub repository and pushing
1. Create an empty repo on GitHub (via the website or `gh` CLI).
2. Add the remote and push:

```powershell
git remote add origin https://github.com/<your-username>/<repo>.git
git branch -M main
git push -u origin main
```

Security tips
- Use environment variables and `.env` files locally.
- Use GitHub Secrets for CI/CD and deployments.
- Consider using a secret scanner (GitHub Advanced Security or third-party tools) to detect accidental leaks.
