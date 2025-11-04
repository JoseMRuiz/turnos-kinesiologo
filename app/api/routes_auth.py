from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.auth import UserCreate, UserLogin, Token
from services.auth import register_user, login_user
from core.security import get_password_hash
from db.user import User
from db.role import Role

router = APIRouter(prefix="/auth", tags=["Autenticación"])


# -------------------------------
# 🔹 Registro normal (rol paciente)
# -------------------------------
@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un usuario nuevo con rol 'paciente' por defecto.
    Devuelve un token de acceso automáticamente.
    """
    try:
        user = register_user(db, data.nombre, data.email, data.password)
        token = login_user(db, data.email, data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# 🔹 Login
# -------------------------------
@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión y devuelve el token JWT.
    """
    try:
        token = login_user(db, data.email, data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# -------------------------------
# 🔹 Crear el primer admin
# -------------------------------
@router.post("/init-admin")
def init_admin(data: UserCreate, db: Session = Depends(get_db)):
    """
    Crea el primer usuario admin si aún no existe.
    """
    # 1️⃣ Verificar si ya existe un admin
    existing_admin = db.query(User).join(Role).filter(Role.name == "admin").first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario administrador."
        )

    # 2️⃣ Crear roles base si no existen
    roles_base = [
        ("admin", "Administrador del sistema"),
        ("kinesiologo", "Profesional de kinesiología"),
        ("recepcionista", "Gestión de turnos"),
        ("paciente", "Usuario paciente"),
    ]
    for name, desc in roles_base:
        if not db.query(Role).filter(Role.name == name).first():
            db.add(Role(name=name, description=desc))
    db.commit()

    # 3️⃣ Obtener el rol admin
    admin_role = db.query(Role).filter(Role.name == "admin").first()

    # 4️⃣ Crear el usuario admin
    hashed_pw = get_password_hash(data.password)
    admin_user = User(
        nombre=data.nombre,
        email=data.email,
        password_hash=hashed_pw,
        role_id=admin_role.id
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return {
        "msg": "Administrador creado correctamente",
        "admin": {
            "id": admin_user.id,
            "email": admin_user.email,
            "nombre": admin_user.nombre,
            "role": "admin"
        }
    }
