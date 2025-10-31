from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from db.user import User
from core.security import  verify_token
from core.dependencies import require_role

router = APIRouter()

# -------------------------
# 🔹 Solo el admin puede ver todos los usuarios
# -------------------------
@router.get("/", dependencies=[Depends(require_role("admin"))])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# -------------------------
# 🔹 Cada usuario puede ver su propio perfil
# -------------------------
@router.get("/me")
def get_my_profile(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# -------------------------
# 🔹 Solo admin puede eliminar usuarios
# -------------------------
@router.delete("/{user_id}", dependencies=[Depends(require_role("admin"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"msg": "Usuario eliminado correctamente"}
