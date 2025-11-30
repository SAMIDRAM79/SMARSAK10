from fastapi import HTTPException, status, Header
from typing import Optional

# Email autorisé pour l'accès à l'application
AUTHORIZED_EMAIL = "konatdra@gmail.com"

async def verify_email(x_user_email: Optional[str] = Header(None)):
    """Vérifie que l'email de l'utilisateur est autorisé"""
    if not x_user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email non fourni. Accès refusé."
        )
    
    if x_user_email.lower() != AUTHORIZED_EMAIL.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé. Seul l'administrateur peut accéder à cette application."
        )
    
    return x_user_email
