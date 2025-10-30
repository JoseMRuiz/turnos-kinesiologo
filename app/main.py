from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.api import routes_auth, routes_roles
from db.session import get_db
from db.user import User
from db.turno import Turno

app = FastAPI(title="Sistema de Turnos")

app.include_router(routes_auth.router)
app.include_router(routes_roles.router)

from app.api.routes_auth import router as auth_router

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Backend de turnos funcionando correctamente"}

@app.get("/dbcheck")
def db_check(db: Session = Depends(get_db)):
    users = db.query(User).count()
    turnos = db.query(Turno).count()
    return {"ok": True, "users": users, "turnos": turnos}
