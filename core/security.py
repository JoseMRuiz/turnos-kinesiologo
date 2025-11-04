from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import get_db
from db.user import User

# ==============================
# 🔐 CONFIGURACIÓN DE SEGURIDAD
# ==============================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()


# ==============================
# 🔹 HASH DE CONTRASEÑA
# ==============================
def get_password_hash(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="La contraseña no puede tener más de 72 caracteres."
        )
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ==============================
# 🔹 CREACIÓN DEL TOKEN JWT
# ==============================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Genera un JWT de acceso a partir de un diccionario de datos.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ==============================
# 🔹 VERIFICACIÓN DEL TOKEN
# ==============================
def verify_token(credentials=Depends(oauth2_scheme)):
    token = credentials.credentials
    print("🪪 TOKEN RECIBIDO:", token[:50], "...")  # ✅ Debug: ver parte del token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ PAYLOAD DECODIFICADO:", payload)
        return payload
    except JWTError as e:
        print("❌ ERROR JWT:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )



# ==============================
# 🔹 USUARIO ACTUAL
# ==============================
def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Retorna el usuario autenticado a partir del token.
    """
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido: falta sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o token inválido.")
    return user
