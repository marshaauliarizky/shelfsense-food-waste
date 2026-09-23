# ShelfSense Deployment Checklist

## Local verification

Run the following commands before publishing:

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

## Streamlit Community Cloud

1. Create a GitHub repository for the project.
2. Upload the application source, `requirements.txt`, `app.py`, `src`, `assets`, `data/sample_food_waste.xlsx`, `docs`, and `exports`.
3. Do not upload `data/shelfsense.db`. The application can create the local database when it starts.
4. Do not upload `__pycache__`, `.pytest_cache`, test databases, `secrets.toml`, or temporary render files.
5. Set the main file to `app.py`.
6. Confirm the app uses simulated demo data and does not contain private business data.
7. Open the deployed URL and test the sidebar, dashboard pages, Excel import, workbook download, and chatbot.

## Before using real business data

The current project is a local portfolio MVP. A production deployment should add authentication, a managed database, backups, audit logging, input limits, and secret management. SQLite is suitable for this demo but not for simultaneous multiuser writes.

## Recommended GitHub contents

Keep the repository focused on the project story. Include the source code, tests, screenshots, documentation, sample workbook, and exported workbook. Keep generated database files and temporary test artifacts excluded through `.gitignore`.
