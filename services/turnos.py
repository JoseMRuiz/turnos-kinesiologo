from datetime import datetime
from sqlalchemy.orm import Session
from db.turno import Turno, EstadoTurno
from db.user import User

def crear_turno(db: Session, paciente_id: int, kinesiologo_id: int, fecha, hora, motivo: str | None = None):
    # Validar que el kinesiólogo no tenga un turno en la misma fecha/hora
    turno_existente = (
        db.query(Turno)
        .filter(Turno.kinesiologo_id == kinesiologo_id, Turno.fecha == fecha, Turno.hora == hora)
        .first()
    )
    if turno_existente:
        raise ValueError("El kinesiólogo ya tiene un turno en ese horario.")

    nuevo_turno = Turno(
        paciente_id=paciente_id,
        kinesiologo_id=kinesiologo_id,
        fecha=fecha,
        hora=hora,
        motivo=motivo,
        estado=EstadoTurno.pendiente
    )
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


def listar_turnos(db: Session, user: User):
    if user.role.name == "admin" or user.role.name == "recepcionista":
        return db.query(Turno).all()
    elif user.role.name == "kinesiologo":
        return db.query(Turno).filter(Turno.kinesiologo_id == user.id).all()
    else:  # paciente
        return db.query(Turno).filter(Turno.paciente_id == user.id).all()


def cambiar_estado(db: Session, turno_id: int, nuevo_estado: EstadoTurno):
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not turno:
        raise ValueError("Turno no encontrado.")
    turno.estado = nuevo_estado
    db.commit()
    db.refresh(turno)
    return turno
