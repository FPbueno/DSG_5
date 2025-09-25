from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..core.database import get_db
from ..core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..core.auth import get_current_user
from ..schemas.user import User, UserCreate, Token
from ..services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    try:
        return UserService.create_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Autentica usuário e retorna token"""
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário atual"""
    return current_user

@router.post("/encrypt")
async def encrypt_data_endpoint(
    data: str,
    current_user: User = Depends(get_current_user)
):
    """Criptografa dados do usuário"""
    encrypted_data = UserService.encrypt_user_data(data)
    return {"encrypted_data": encrypted_data}

@router.post("/decrypt")
async def decrypt_data_endpoint(
    encrypted_data: str,
    current_user: User = Depends(get_current_user)
):
    """Descriptografa dados do usuário"""
    try:
        decrypted_data = UserService.decrypt_user_data(encrypted_data)
        return {"decrypted_data": decrypted_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to decrypt data"
        )
