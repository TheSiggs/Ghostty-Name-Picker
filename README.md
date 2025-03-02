# Ghostty Picker

## Overview
Ghostty Picker is a Flask-based web application that allows users to log in via Google authentication and select or modify ghost names. The application is deployed on **Google App Engine** and uses **Google Cloud Datastore (NDB)** for storage.

## Features
- **Google OAuth 2.0 Authentication**
- **Secure Flask Application with Flask-Talisman**
- **Data Storage using Google Cloud Datastore (NDB)**
- **HTMX-Free Traditional Form Handling**
- **Deployment on Google App Engine with Gunicorn**

## Tech Stack
- **Backend:** Flask, Flask-Login, Flask-Talisman
- **Database:** Google Cloud Datastore (NDB)
- **Authentication:** Google OAuth 2.0
- **Deployment:** Google App Engine, Gunicorn

## Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/yourusername/ghostty-picker.git
cd ghostty-picker
```

### **2. Set Up the Environment**
Using **Poetry**:
```sh
poetry install
```

Or using **pip**:
```sh
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**
Create a `.env` file and add:
```
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GOOGLE_APPLICATION_CREDENTIALS=path/to/your-service-account.json
FLASK_SETTINGS_FILENAME=settings.py
```

### **4. Run the Application Locally**
```sh
flask run
```

By default, the application runs on `http://127.0.0.1:5000/`.

## Deployment
### **1. Enable Required Google Cloud Services**
```sh
gcloud services enable appengine.googleapis.com
gcloud services enable datastore.googleapis.com
gcloud services enable oauth2.googleapis.com
```

### **2. Deploy to Google App Engine**
```sh
gcloud app deploy --no-cache
```

### **3. Open the App in Browser**
```sh
gcloud app browse
```

## Usage
1. **Log in using Google**
2. **Select a ghost name**
3. **Modify the ghost name if needed**
4. **Confirm selection**
