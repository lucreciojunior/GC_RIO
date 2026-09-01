"""Dependências de autenticação e autorização para as rotas."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.security import decodificar_token
from app.models import UsuarioPublico

security_scheme = HTTPBearer()


def get_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> UsuarioPublico:
    """Extrai e valida o usuário do token JWT enviado no header Authorization."""
    token = credentials.credentials
    payload = decodificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UsuarioPublico(
        id=payload.get("id"),
        nome=payload.get("nome"),
        usuario=payload.get("sub"),
        perfil=payload.get("perfil"),
        igreja=payload.get("igreja"),
    )


def requer_admin(
    usuario: UsuarioPublico = Depends(get_usuario_atual),
) -> UsuarioPublico:
    """Só permite acesso a usuários com perfil admin."""
    if usuario.perfil != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )
    return usuario


def requer_perfis(*perfis_permitidos: str):
    """Fábrica de dependência que exige um dos perfis informados."""

    def verificador(
        usuario: UsuarioPublico = Depends(get_usuario_atual),
    ) -> UsuarioPublico:
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso.",
            )
        return usuario

    return verificador
