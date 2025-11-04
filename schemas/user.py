from pydantic import BaseModel, EmailStr
from typing import Optional

# 🔸 Datos de entrada para registro o creación
class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    role_name: Optional[str] = "paciente"  # por defecto paciente


# 🔸 Datos de salida (para devolver info del usuario)
class UserOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    role_name: Optional[str] = None

    class Config:
        orm_mode = True
