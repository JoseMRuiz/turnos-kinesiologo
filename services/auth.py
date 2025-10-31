from datetime import timedelta
from sqlalchemy.orm import Session
from db.user import User
from db.role import Role
from core.security import verify_password, get_password_hash, create_access_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


def register_user(db: Session, nombre: str, email: str, password: str, role_name: str = "paciente"):
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("El email ya está registrado")

    
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"El rol '{role_name}' no existe")

   
    hashed_password = get_password_hash(password)

    new_user = User(
        nombre=nombre,
        email=email,
        password_hash=hashed_password,
        role_id=role.id,    
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

    
    token_data = {
        "sub": user.email,
        "role": user.role.name if user.role else None,
        "username": user.nombre
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    return access_token
