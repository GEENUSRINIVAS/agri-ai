# Hosting Guide: GitHub + Render + Netlify

This guide explains how to deploy your Flask web application online using:
- **GitHub** for source code hosting
- **Render** for the Flask backend
- **Netlify** for optional static front-end or landing page hosting

---

## 1. Prepare Your Project for Deployment

### 1.1 Required files
Make sure the following files exist in your project root:
- `app.py`
- `requirements.txt`
- `Procfile`
- `.gitignore`
- `models/xgboost_model.pkl`
- `models/label_encoders.pkl`
- `templates/` directory
- `static/` directory

### 1.2 Optional deployment files
Add or verify these files:
- `runtime.txt` (recommended)
- `.env` (local secret config only, do not push)

### 1.3 Create `runtime.txt`
Use the Python version supported by Render and your environment.

Create `runtime.txt` with:
```
python-3.11.8
```

---

## 2. Update `app.py` for production readiness

### 2.1 Use environment variables
Replace hard-coded secrets with environment-based configuration.

Your project already includes this setup:
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mca_project_secret_key_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///agricultural_db.sqlite3'
)
```

### 2.2 Run on all network interfaces
This is already updated in `app.py`:
```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug_mode)
```

---

## 3. Configure `.gitignore`

Ensure local development and secret files are excluded from Git.

Your `.gitignore` should include:
```
venv/
__pycache__/
*.pyc
instance/
*.sqlite3
.DS_Store
.env
```

---

## 4. Push the project to GitHub

### 4.1 Create a GitHub repository
1. Sign in to GitHub
2. Create a new repository, e.g. `agripredict-ai`
3. Do not add README or license if you already have local repo contents

### 4.2 Initialize Git and push
Run in project root:
```powershell
cd d:\srinu\mca_project
git init
git add .
git commit -m "Initial deploy-ready commit"
git branch -M main
git remote add origin https://github.com/<your-username>/agripredict-ai.git
git push -u origin main
```

> Replace `<your-username>` with your GitHub username.

---

## 5. Deploy the backend on Render

Render is recommended because it supports Python web apps with GitHub integration.

### 5.1 Create Render account
1. Visit https://render.com
2. Sign in with GitHub
3. Authorize access to your repository

### 5.2 Create a new Web Service

1. Click **New** → **Web Service**
2. Choose your GitHub repo
3. Branch: `main`
4. Name: `agripredict-ai`
5. Region: closest to you
6. Environment: `Python 3`
7. Build Command: `pip install -r requirements.txt`
8. Start Command: `gunicorn app:app`
9. Root Directory: leave blank if app.py is in repo root

### 5.3 Configure environment variables
Under Render service settings, add:
- `SECRET_KEY` = `a-secure-random-string`
- `FLASK_DEBUG` = `false`

### 5.4 Deploy
After setup, Render will build and deploy automatically.

### 5.5 Verify
Open the Render URL, for example:
```
https://agripredict-ai.onrender.com
```

If the app loads, the backend is live.

---

## 6. Deploy a static site on Netlify (optional)

Netlify cannot host the Flask backend directly. Use Netlify only for a static landing page or separate SPA.

### 6.1 When to use Netlify
Use Netlify if you want:
- A marketing site for the app
- A frontend-only React/Vue/HTML site
- A separate homepage that calls your Render API

### 6.2 Example: Host a static landing page
If you keep your current Flask templates on Render, Netlify is optional.

If you want to add a static landing page in this repo, create a separate folder such as `frontend/` and add:
- `index.html`
- `styles.css`
- `scripts.js`

Deploy that folder to Netlify using GitHub.

### 6.3 Configure API URL in static frontend
If your Netlify frontend calls the backend, set the backend base URL in JavaScript.

Example:
```js
const BACKEND_URL = 'https://agripredict-ai.onrender.com';
```

Then call API endpoints like:
```js
fetch(`${BACKEND_URL}/predict`, {
  method: 'POST',
  body: formData,
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
})
```

---

## 7. Connect GitHub, Render, and Netlify

### 7.1 GitHub is source control
- Store app code
- Track changes
- Trigger auto-deploy on Render and Netlify

### 7.2 Render serves the Flask backend
- Build from GitHub branch `main`
- Run `gunicorn app:app`
- Provide live backend URL

### 7.3 Netlify serves static frontend
- Optional
- Use site URL for website landing pages
- Call Render backend via full URL

---

## 8. Example deployment architecture

```
GitHub Repo
   ├─ app.py
   ├─ requirements.txt
   ├─ Procfile
   ├─ models/
   │   ├─ xgboost_model.pkl
   │   └─ label_encoders.pkl
   ├─ templates/
   ├─ static/
   └─ hosting.md

        ↓

Render Backend
   ├─ Runs Flask app
   ├─ Serves HTML pages
   ├─ Handles predictions
   └─ Uses environment variables

Optional Netlify Frontend
   ├─ Hosts static landing page
   ├─ Calls Render backend with fetch()
   └─ Adds faster static hosting for marketing pages
```

---

## 9. Useful deployment commands

### Local test before deployment
```powershell
python app.py
```

### Build and push to GitHub
```powershell
git add .
git commit -m "Deployment config"
git push origin main
```

---

## 10. Troubleshooting

### App fails to start on Render
- Confirm `requirements.txt` installs successfully
- Confirm `Procfile` is present
- Confirm `app.py` in repo root
- Confirm `gunicorn app:app` works locally
- Set `FLASK_DEBUG` to `true` temporarily for logs

### Model loading error
- Ensure `models/xgboost_model.pkl` exists in GitHub repo
- Ensure `models/label_encoders.pkl` exists
- Confirm model files are not excluded by `.gitignore`

### Database issues
- `DATABASE_URL` is optional on Render
- Local SQLite still works if no remote DB is configured
- For production, consider switching to PostgreSQL later

---

## 11. Optional improvements after deployment

1. Add **real weather API** integration
2. Use **hashed passwords** instead of plain text
3. Replace SQLite with **PostgreSQL** on Render
4. Add **HTTPS enforcement** and security headers
5. Add **logging** and error monitoring
6. Add **CI pipeline** with GitHub Actions

---

## 12. Final notes

- Use **Render** for your live Flask app
- Use **GitHub** for source control
- Use **Netlify** only for static content or separate front-end sites
- Keep **`app.py`** and model files in the main repo root
- Do not push `.env` or local database files to GitHub

Good luck with deployment! If you want, I can also generate a ready-to-use `netlify.toml` and a small static landing page example for this project.