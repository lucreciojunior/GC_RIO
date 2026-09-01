"""Segurança: hash de senhas (bcrypt) e geração/validação de tokens JWT."""
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import jwt, JWTError

from app.config import settings


# ------------------------------------------------------------
# Senhas (bcrypt direto, sem passlib)
# ------------------------------------------------------------
def hash_senha(senha: str) -> str:
    """Gera o hash bcrypt de uma senha.

    bcrypt limita a senha a 72 bytes; truncamos por segurança.
    """
    senha_bytes = senha.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Confere se a senha bate com o hash salvo."""
    try:
        senha_bytes = senha.encode("utf-8")[:72]
        return bcrypt.checkpw(senha_bytes, senha_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ------------------------------------------------------------
# Tokens JWT
# ------------------------------------------------------------
def criar_token(dados: dict) -> str:
    """Cria um token JWT com expiração."""
    to_encode = dados.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decodificar_token(token: str) -> Optional[dict]:
    """Decodifica e valida um token JWT. Retorna None se inválido/expirado."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
