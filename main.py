import os
from fastapi import FastAPI, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os
from models import User, Kilometraje
from database import engine, SessionLocal, Base
from schemas import UserCreate, KilometrajeBase
from auth import *
from crud import *

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/register")
def register_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(db=db, user=UserCreate(username=username, email=email, password=password))
    return RedirectResponse(url="/", status_code=303)

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return response

@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    registros = get_kilometraje_by_user(db, current_user.id)
    return templates.TemplateResponse("dashboard.html", {"request": request, "registros": registros, "user": current_user})

@app.post("/registro_km")
def registro_km(
    fecha: str = Form(...),
    patente: str = Form(...),
    km_inicio: float = Form(...),
    km_fin: float = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_km = km_fin - km_inicio
    km_data = KilometrajeBase(fecha=fecha, patente=patente, km_inicio=km_inicio, km_fin=km_fin, total_km=total_km)
    create_kilometraje(db, km_data, current_user.id)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/admin")
def admin_dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    usuarios = get_all_users(db)
    return templates.TemplateResponse("admin.html", {"request": request, "usuarios": usuarios})

 
@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
