# Flask Web Application

## 📌 Description
This is a web application built with Python’s **Flask** framework. It demonstrates the use of:

- **Jinja** templating  
- **WTForms** for form handling  
- Architectural design patterns and principles, including:  
  - Repository  
  - Dependency Inversion  
  - Single Responsibility  

The application also uses **Flask Blueprints** to maintain separation of concerns between application functions.  

**Testing** includes both unit and end-to-end tests using **pytest**.  

---

## ⚙️ Installation

```bash
# Navigate to where the app is stored
cd <project-directory>

# Create a virtual environment
py -3 -m venv venv

# Activate the virtual environment
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

```

## 🚀 Execution

From the project directory, with the virtual environment activated, run:
flask run
---

## 🔧 Configuration

The app uses the following configuration values:
```bashFLASK_APP``` → Entry point of the application (wsgi.py).
```bashFLASK_ENV``` → Environment mode (development or production).
```bashSECRET_KEY``` → Used to encrypt session data.
```bashTESTING``` → Set to False when running the application; automatically set to True during tests.
```bashWTF_CSRF_SECRET_KEY``` → Secret key for WTForms.

## Database Configuration
```bashSQLALCHEMY_DATABASE_URI``` → URI of the SQLite database (default: created in the project root).
```bashSQLALCHEMY_ECHO``` → If True, SQLAlchemy prints executed SQL statements.
```bashREPOSITORY``` → Switch between in-memory repository and SQLAlchemy database repository.
