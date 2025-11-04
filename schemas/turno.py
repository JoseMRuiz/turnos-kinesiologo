from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from enum import Enum

class EstadoTurno(str, Enum):
    pendiente = "pendiente"
    confirmado = "confirmado"
    cancelado = "cancelado"

class TurnoBase(BaseModel):
    fecha: date
    hora: time
    motivo: Optional[str] = None

class TurnoCreate(TurnoBase):
    paciente_id: Optional[int] = None  # si lo crea la recepcionista
    kinesiologo_id: int

class TurnoUpdateEstado(BaseModel):
    estado: EstadoTurno

class TurnoOut(TurnoBase):
    id: int
    estado: EstadoTurno
    paciente_id: int
    kinesiologo_id: int

    class Config:
        orm_mode = True
