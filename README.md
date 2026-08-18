# Full-Stack AI Web Application
Frontend:
HTML
CSS
Jinja2 templates
JavaScript

Backend:
FastAPI (Python)
Uvicorn

AI:
Groq API 
Llama model

Database:
SQLite

Deployment
GitHub

## Features
User Authentication & Login
User Registration
Password Hashing & Secure Authentication
Session Management
Protected User Pages
User-Specific Conversation Data
AI-Powered Question Answering
copy and download pdf
Conversation Memory
Conversation History
Web-Based User Interface
AI Model Integration
Database Integration

### installation

python -m venv venv
.\venv\Scripts\activate
pip install "pwdlib[argon2]"


python -m pip install fastapi uvicorn jinja2 python-dotenv openai python-multipart reportlab


##### pdf
pip install reportlab


## Run 
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload


