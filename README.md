# Computer Equipment Management System

A Flask-based web application for managing computer equipment, users, and reporting.

## Features
- Admin authentication with login/logout
- Dashboard with equipment statistics
- CRUD operations for devices
- Search and filtering
- Charts for equipment by type and status
- SQLite database with automatic initialization

## Requirements
- Python 3.10+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Bootstrap 5

## Installation
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python app.py
   ```
   The app creates the SQLite database automatically on first run.

## Default Admin Credentials
- Username: `admin`
- Password: `admin123`

## Sample Data
You can populate the database with sample equipment by running:
```bash
python seed_data.py
```

## Project Structure
- `app.py` - Main application entry point
- `models.py` - SQLAlchemy models
- `templates/` - HTML templates
- `static/` - CSS assets
- `database.db` - SQLite database (created automatically)
