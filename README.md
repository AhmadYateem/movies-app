# Video Store (EECE430)

This repository contains a Django-based Video Store application used for EECE430 course assignments. It provides a simple CRUD interface to manage a small video inventory (movies), including listing, searching, viewing details, creating, editing, and deleting videos.

Author: Ahmad Yateem

What it does
- Defines a `Video` model with basic movie metadata (title, actors, director, genre, year).
- Provides custom forms and templates for full CRUD without relying on Django admin.

How to run (Windows PowerShell)
1. Activate your Python virtual environment that has Django installed. Example (adjust path to your env):
   ```powershell
   & "C:\Users\ahmad\OneDrive\Desktop\EECE430-Github\video store\myenv\Scripts\Activate.ps1"
   ```
2. Change to the project `website` folder and run the dev server:
   ```powershell
   Set-Location "C:\Users\ahmad\OneDrive\Desktop\EECE430-Github\video store\website"
   python manage.py migrate
   python manage.py runserver
   ```
3. Open http://127.0.0.1:8000/ in your browser and navigate to the Videos section.

Notes and troubleshooting
- The project uses a local `db.sqlite3` file. To reset the database, remove `db.sqlite3` and run `python manage.py migrate`.
- Ensure required Python packages from `requirements.txt` are installed into the activated environment.

If you want, I can also add a quick developer guide and tests in a follow-up.