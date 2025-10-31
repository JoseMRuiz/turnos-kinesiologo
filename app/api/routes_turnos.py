from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import  verify_token
from db.session import get_db
from db.turno import Turno
from core.dependencies import require_role

router = APIRouter()

# --------------------------
# 🔹 KINESIÓLOGO: Ver sus turnos
# --------------------------
@router.get("/mis-turnos", dependencies=[Depends(require_role("kinesiologo"))])
def get_turnos_kinesiologo(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    kinesiologo_id = payload.get("sub")
    return db.query(Turno).filter(Turno.kinesiologo_id == kinesiologo_id).all()

# --------------------------
# 🔹 KINESIÓLOGO: Editar sus turnos
# --------------------------
@router.put("/editar/{turno_id}", dependencies=[Depends(require_role("kinesiologo"))])
def editar_turno(turno_id: int, nuevo_horario: str, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    kinesiologo_id = payload.get("sub")
    turno = db.query(Turno).filter(Turno.id == turno_id, Turno.kinesiologo_id == kinesiologo_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado o no autorizado")
    turno.horario = nuevo_horario
    db.commit()
    return {"msg": "Turno actualizado correctamente"}

# --------------------------
# 🔹 RECEPCIONISTA: Asignar pacientes
# --------------------------
@router.post("/asignar", dependencies=[Depends(require_role("recepcionista"))])
def asignar_paciente(turno_id: int, paciente_id: int, db: Session = Depends(get_db)):
    turno = db.query(Turno).get(turno_id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    turno.paciente_id = paciente_id
    db.commit()
    return {"msg": "Paciente asignado correctamente"}

# --------------------------
# 🔹 PACIENTE: Ver sus turnos
# --------------------------
@router.get("/paciente/mis-turnos", dependencies=[Depends(require_role("paciente"))])
def get_turnos_paciente(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    paciente_id = payload.get("sub")
    return db.query(Turno).filter(Turno.paciente_id == paciente_id).all()
