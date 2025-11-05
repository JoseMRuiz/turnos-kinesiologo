from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from db.turno import Turno
from db.user import User
from app.turnos_enum import EstadoTurno

def crear_turno(db: Session, paciente_id: int, kinesiologo_id: int, fecha, hora, motivo: str | None = None):
    # Evitar duplicados: un kinesiólogo no puede tener dos turnos al mismo horario
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
        estado=EstadoTurno.pendiente,
    )
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


def listar_turnos(db: Session, user: User):
    q = db.query(Turno).options(joinedload(Turno.paciente), joinedload(Turno.kinesiologo))

    if user.role.name in ["admin", "recepcionista"]:
        return q.all()
    elif user.role.name == "kinesiologo":
        return q.filter(Turno.kinesiologo_id == user.id).all()
    elif user.role.name == "paciente":
        return q.filter(Turno.paciente_id == user.id).all()
    else:
        return []


def cambiar_estado(db: Session, turno_id: int, nuevo_estado: EstadoTurno):
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not turno:
        raise ValueError("Turno no encontrado.")
    turno.estado = nuevo_estado
    db.commit()
    db.refresh(turno)
    return turno
