from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base  

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(190), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
        # 🔹 Eliminamos el campo 'rol' de texto y agregamos la ForeignKey
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)

    # 🔹 Relación con el modelo Role
    role = relationship("Role", back_populates="users")

    # 🔹 Relación con Turno (ya la tenías)
    turnos = relationship("Turno", back_populates="user")

    turnos = relationship("Turno", back_populates="user")
