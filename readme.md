
# Recipe Site – Setup Guide

This guide walks you through setting up the development environment, installing dependencies, preparing the database, and running the Flask app.

---

## 1. Set Up a Virtual Environment

Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

---

## 2. Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

## 3. Set Up the Database

Run the setup script to:

- Drop and recreate the database
- Apply the schema
- Import food data
- Populate sample recipes

```bash
./import_data.sh
```

> Make sure PostgreSQL is running and that you have permission to create databases.

---

## 4. Run the Flask App

Set the Flask app environment variable and start the server:

```bash
flask run
```
---

## 5. Access the App

Open your web browser and go to:

```
http://127.0.0.1:5000
```

This will load the locally running Flask application.
