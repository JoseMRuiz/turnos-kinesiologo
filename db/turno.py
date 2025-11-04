from sqlalchemy import Column, Integer, String, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
import enum

class EstadoTurno(enum.Enum):
    pendiente = "pendiente"
    confirmado = "confirmado"
    cancelado = "cancelado"

class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(String(255), nullable=True)
    estado = Column(Enum(EstadoTurno), default=EstadoTurno.pendiente, nullable=False)

    # Relaciones
    paciente_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    kinesiologo_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    paciente = relationship("User", foreign_keys=[paciente_id], backref="turnos_paciente")
    kinesiologo = relationship("User", foreign_keys=[kinesiologo_id], backref="turnos_kinesiologo")
