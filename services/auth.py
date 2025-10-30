# services/auth.py
from datetime import timedelta
from sqlalchemy.orm import Session
from db.user import User
from core.security import verify_password, get_password_hash, create_access_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


from db.user import User
from core.security import get_password_hash
from sqlalchemy.orm import Session

def register_user(db: Session, nombre: str, email: str, password: str):
    # Verificar si ya existe el usuario
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("El email ya está registrado")

    hashed_password = get_password_hash(password)

    # Crear nuevo usuario
    new_user = User(
        nombre=nombre,
        email=email,
        password_hash=hashed_password,  # 👈 campo correcto
        rol="paciente"                  # 👈 valor por defecto (paciente)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash): 
        raise ValueError("Credenciales inválidas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # 👇 Incluir el rol en el token
    token_data = {
        "sub": user.email,
        "role": user.rol,
        "username": user.nombre
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    return access_token