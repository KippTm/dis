
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


# How to interact with the app
## Creating a user
- You need a user to interact with the app. You can create one using the register button. Please note that the password needs at least 8 characters.
## Navigating recipes
- Once you have a created user, you can login to the website. Here you can see others created recipes, as well as our own
- You can search recipes on the find recipe button, or add your own using the add recipe button. 
- The autocomplete/search on the add recipe page matches food-stuff in our database. This means it won't match unless it is exact. Thus sometimes, certain words have to be looked at individually to find the food
    - An example is "hakket oksekød" resulting in no matches, but "hakket" result in many mince-meats, among them, "hakket oksekød". 
        - An improvement, albeit significantly more computationally and advanced option would be to use an optimal substring-pattern to match.



