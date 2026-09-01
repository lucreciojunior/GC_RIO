"""Rotas de autenticação: login."""
from fastapi import APIRouter, HTTPException, status

from app.database import get_supabase
from app.security import verificar_senha, criar_token
from app.models import LoginRequest, TokenResponse, UsuarioPublico

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest):
    """Autentica o usuário e retorna um token JWT."""
    supabase = get_supabase()

    resultado = (
        supabase.table("usuarios")
        .select("*")
        .eq("usuario", dados.usuario.strip().lower())
        .execute()
    )

    if not resultado.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
        )

    user = resultado.data[0]

    if not verificar_senha(dados.senha, user["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
        )

    usuario_publico = UsuarioPublico(
        id=user["id"],
        nome=user["nome"],
        usuario=user["usuario"],
        perfil=user["perfil"],
        igreja=user.get("igreja"),
    )

    # Payload do token
    token = criar_token({
        "sub": user["usuario"],
        "id": user["id"],
        "nome": user["nome"],
        "perfil": user["perfil"],
        "igreja": user.get("igreja"),
    })

    return TokenResponse(access_token=token, usuario=usuario_publico)
