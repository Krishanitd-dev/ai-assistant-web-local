from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.pdf_service import create_pdf
from app.ai_service import get_ai_response
from app.database import save_conversation, get_all_conversations, create_table, delete_conversation, create_user, get_user
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from app.auth import secure_hash, verify_password
from pydantic import EmailStr

app = FastAPI()
create_table()

app.add_middleware(
    SessionMiddleware,
    secret_key="secret-key-will-move-to-env"
)

# CSS/ JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML
templates = Jinja2Templates(directory="./app/templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):

    logout_message = None

    if request.query_params.get("logout") == "success":
        logout_message = "You have been logged out successfully."

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "logout_message": logout_message
        }
    )
@app.post("/login")
async def login(request:Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = get_user(email)

    if not user:
      return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": "Invalid email or password."}
    )

    password_hash = user[2]
    if not verify_password(password, password_hash):
        return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": "Invalid email or password."}
        )

    # create login session here 
    request.session["user_id"] = user[0]
    request.session["email"] = user[1]
   
    return RedirectResponse(
        url="/ask",
        status_code=303
    )

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

@app.post("/register")
async def register(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)):

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Passwords do not match."}
        )

    existing_user = get_user(email)

    if (len(password) < 8 
    or not any(char.isdigit() for char in password) 
    or not any(char.isupper() for char in password)
    or not any(char.islower() for char in password)):
        return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "error": "Password must be at least 8 characters and contain an uppercase letter, lowercase letter, and number."
        })

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Email already registered."})
    
    password_hash = secure_hash(password)
    created_at = datetime.now().isoformat()

    create_user(email, password_hash,created_at)
    return RedirectResponse(
        url="/",
        status_code=303)

@app.get("/ask", response_class=HTMLResponse)
async def ask_page(request: Request):
    
    if "user_id" not in request.session:
        print("NO LOGIN SESSION - REDIRECTING")
        return RedirectResponse(
            url="/",
            status_code=303
        )
    email = request.session.get("email")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "email": email
        }
    )
   

@app.post("/ask", response_class=HTMLResponse)
async def ask_ai(request: Request, question: str = Form(...)):

    if "user_id" not in request.session:
        return RedirectResponse( url="/", status_code=303)
    email = request.session.get("email")

    answer = get_ai_response(question)

    save_conversation(email, question, answer)

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
    if "user_id" not in request.session:
        return RedirectResponse( url="/", status_code=303)
    email = request.session.get("email")

    
    conversations = get_all_conversations(email)

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

    if "user_id" not in request.session:
        return RedirectResponse( url="/", status_code=303)
    email = request.session.get("email")

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request
        }
    )

@app.post("/delete/{id}")
async def delete_history(
    request: Request,
    id: int
):

    if "user_id" not in request.session:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    email = request.session.get("email")

    delete_conversation(id, email)

    return RedirectResponse(
        url="/history",
        status_code=303
    )

@app.post("/download-pdf")
async def download_pdf(
    request: Request,
    question: str =Form(...),
    answer: str = Form(...)
):

    if "user_id" not in request.session:
        return RedirectResponse(
            url="/",
            status_code=303
        )
    filename = create_pdf(
        question, answer
    )
    return FileResponse(
        filename,
        media_type="application/pdf",
        filename="AI_Response.pdf"
    )

@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/?logout=success",
        status_code=303
    )

@app.middleware("http")
async def no_cache(request: Request, call_next):

    response = await call_next(request)

    if request.url.path in ["/ask", "/history", "/about"]:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response