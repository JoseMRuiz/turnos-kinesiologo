from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from app.turnos_enum import EstadoTurno  # 👈 import correcto

class UserShort(BaseModel):
    id: int
    nombre: str
    email: str
    class Config:
        from_attributes = True

class TurnoBase(BaseModel):
    fecha: date
    hora: time
    motivo: Optional[str] = None

class TurnoCreate(TurnoBase):
    paciente_id: Optional[int] = None
    kinesiologo_id: int

class TurnoUpdateEstado(BaseModel):
    estado: EstadoTurno

class TurnoOut(TurnoBase):
    id: int
    estado: EstadoTurno
    paciente: Optional[UserShort]
    kinesiologo: Optional[UserShort]
    class Config:
        from_attributes = True
