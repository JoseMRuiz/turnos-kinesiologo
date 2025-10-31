from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.role import RoleOut, RoleCreate
from services.roles import get_roles, create_role
from core.dependencies import require_role

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=list[RoleOut], dependencies=[Depends(require_role("admin"))])
def get_roles_route(db: Session = Depends(get_db)):
    return get_roles(db)

@router.post("/", response_model=RoleOut, dependencies=[Depends(require_role("admin"))])
def create_role_route(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)
