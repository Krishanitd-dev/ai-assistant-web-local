from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.ai_service import get_ai_response
from app.database import save_conversation, get_all_conversations, create_table

app = FastAPI()
create_table()

# CSS/ JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML
templates = Jinja2Templates(directory="./app/templates")




@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "answer": ""
        }
    )


@app.post("/ask", response_class=HTMLResponse)
async def ask_ai(request: Request, question: str = Form(...)):

    answer = get_ai_response(question)

    # save_conversation(question, answer)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "answer": answer,
            "question": question
        }
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    conversations = get_all_conversations()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "conversations": conversations
        }
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request
        }
    )