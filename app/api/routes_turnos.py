from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import verify_token
from db.session import get_db
from db.user import User
from schemas.turno import TurnoCreate, TurnoOut, TurnoUpdateEstado, EstadoTurno
from services.turnos import crear_turno, listar_turnos, cambiar_estado

router = APIRouter(prefix="/turnos", tags=["Turnos"])


# -------------------------------
# 🔹 Helper: obtener usuario actual
# -------------------------------
def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o token inválido.")
    return user


# -------------------------------
# 🔹 Crear turno
# -------------------------------
@router.post("/", response_model=TurnoOut)
def crear_turno_route(
    data: TurnoCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Crear turno:
    - Paciente crea el suyo
    - Recepcionista o admin puede crear para cualquier paciente
    """
    try:
        # Si lo crea un paciente, forzamos su propio ID
        if user.role.name == "paciente":
            paciente_id = user.id
        elif user.role.name in ["recepcionista", "admin"]:
            # Recepcionista o admin pueden elegir paciente
            if not data.paciente_id:
                raise HTTPException(status_code=400, detail="Debe indicar el paciente_id.")
            paciente_id = data.paciente_id
        else:
            raise HTTPException(status_code=403, detail="No tienes permisos para crear turnos.")

        turno = crear_turno(
            db,
            paciente_id=paciente_id,
            kinesiologo_id=data.kinesiologo_id,
            fecha=data.fecha,
            hora=data.hora,
            motivo=data.motivo,
        )
        return turno

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



# -------------------------------
# 🔹 Listar turnos según el rol
# -------------------------------
@router.get("/", response_model=list[TurnoOut])
def listar_turnos_route(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Lista los turnos según el rol del usuario.
    """
    return listar_turnos(db, user)


# -------------------------------
# 🔹 Cambiar estado de turno
# -------------------------------
@router.put("/{turno_id}/estado", response_model=TurnoOut)
def cambiar_estado_route(
    turno_id: int,
    data: TurnoUpdateEstado,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Cambia el estado de un turno (solo recepcionista, admin o kinesiólogo).
    """
    if user.role.name not in ["admin", "recepcionista", "kinesiologo"]:
        raise HTTPException(status_code=403, detail="No autorizado para cambiar estados.")

    try:
        turno = cambiar_estado(db, turno_id, data.estado)
        return turno
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
