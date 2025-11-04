from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    APP_NAME: str = "Sistema de Turnos"
    ENV: str = "dev"

    # 🔹 Base de datos
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "turnos"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"

    # 🔹 JWT
    SECRET_KEY: str = "jose123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🔹 Admin inicial (para autogenerar al arrancar)
    ADMIN_EMAIL: str = "admin@kine.local"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_NOMBRE: str = "Administrador"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()

# Alias para compatibilidad
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
