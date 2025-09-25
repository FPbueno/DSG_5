from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password, encrypt_data, decrypt_data

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Cria um novo usuário"""
        # Verifica se o usuário já existe
        if db.query(User).filter(User.username == user.username).first():
            raise ValueError("Username already registered")
        
        if db.query(User).filter(User.email == user.email).first():
            raise ValueError("Email already registered")
        
        # Cria o usuário
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Obtém usuário por username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Obtém usuário por email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Union[User, None]:
        """Autentica usuário"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """Atualiza dados do usuário"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if user_update.username:
            # Verifica se o novo username já existe
            existing_user = db.query(User).filter(
                User.username == user_update.username,
                User.id != user_id
            ).first()
            if existing_user:
                raise ValueError("Username already taken")
            user.username = user_update.username
        
        if user_update.email:
            # Verifica se o novo email já existe
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != user_id
            ).first()
            if existing_user:
                raise ValueError("Email already taken")
            user.email = user_update.email
        
        if user_update.password:
            user.hashed_password = get_password_hash(user_update.password)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def encrypt_user_data(data: str) -> str:
        """Criptografa dados do usuário"""
        return encrypt_data(data)
    
    @staticmethod
    def decrypt_user_data(encrypted_data: str) -> str:
        """Descriptografa dados do usuário"""
        return decrypt_data(encrypted_data)
