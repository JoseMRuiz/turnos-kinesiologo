from sqlalchemy.orm import Session
from db.role import Role
from schemas.role import RoleCreate

def get_roles(db: Session):
    return db.query(Role).all()

def create_role(db: Session, role: RoleCreate):
    db_role = Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
