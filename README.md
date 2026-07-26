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

## Features
1. AI-Powered Question Answering
2. Conversation Memory
3.  Conversation History
4.  Web-Based User Interface
5. AI Model Integration
6.  Database Integration

### installation

python -m venv venv
.\venv\Scripts\activate


python -m pip install fastapi uvicorn jinja2 python-dotenv openai python-multipart

##### pdf
pip install reportlab

pip freeze > requirements.txt
pip install -r requirements.txt


## Run 
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload