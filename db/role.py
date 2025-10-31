from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150), nullable=True)
    users = relationship("User", back_populates="role")