from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base  

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(190), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("roles.id"), nullable=True)

    # Relación con Role
    role = relationship("Role", back_populates="users")

    # 👇 Relaciones separadas para evitar ambigüedad
    turnos_como_paciente = relationship(
        "Turno",
        back_populates="paciente",
        foreign_keys="Turno.paciente_id",
        cascade="all, delete-orphan"
    )

    turnos_como_kinesiologo = relationship(
        "Turno",
        back_populates="kinesiologo",
        foreign_keys="Turno.kinesiologo_id",
        cascade="all, delete-orphan"
    )
