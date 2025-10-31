from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Routers
from app.api import routes_auth, routes_roles, routes_users, routes_turnos

# DB
from db.session import get_db
from db.user import User
from db.turno import Turno

app = FastAPI(title="Sistema de Turnos")

# --- Middleware CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rutas base ---
@app.get("/")
def root():
    return {"message": "Backend de turnos funcionando correctamente"}

@app.get("/dbcheck")
def db_check(db: Session = Depends(get_db)):
    users = db.query(User).count()
    turnos = db.query(Turno).count()
    return {"ok": True, "users": users, "turnos": turnos}

# Incluimos los routers SIN prefix duplicado
app.include_router(routes_auth.router, tags=["Autenticación"])
app.include_router(routes_roles.router, tags=["Roles"])
app.include_router(routes_users.router, tags=["Usuarios"])
app.include_router(routes_turnos.router, tags=["Turnos"])
