from fastapi import Depends, HTTPException, status
from core.security import verify_token

def require_role(required_role: str):
    def role_checker(payload: dict = Depends(verify_token)):
        user_role = payload.get("role")
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Rol requerido: {required_role}"
            )
        return payload
    return role_checker
