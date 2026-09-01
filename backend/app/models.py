"""Models Pydantic para validação de entrada e saída da API."""
from datetime import date
from typing import Optional, Any, Literal

from pydantic import BaseModel, Field


# ============================================================
# Autenticação
# ============================================================
class LoginRequest(BaseModel):
    usuario: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioPublico"


# ============================================================
# Usuários
# ============================================================
Perfil = Literal["admin", "lider", "servo"]


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=2)
    usuario: str = Field(..., min_length=3)
    perfil: Perfil = "servo"
    igreja: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=3)


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2)
    usuario: Optional[str] = Field(None, min_length=3)
    senha: Optional[str] = Field(None, min_length=3)
    perfil: Optional[Perfil] = None
    igreja: Optional[str] = None


class UsuarioPublico(BaseModel):
    """Dados do usuário retornados pela API (sem a senha)."""
    id: int
    nome: str
    usuario: str
    perfil: Perfil
    igreja: Optional[str] = None


# ============================================================
# Igrejas
# ============================================================
class IgrejaBase(BaseModel):
    nome: str = Field(..., min_length=2)
    endereco: Optional[str] = None


class IgrejaCreate(IgrejaBase):
    pass


class IgrejaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2)
    endereco: Optional[str] = None


class Igreja(IgrejaBase):
    id: int


# ============================================================
# Contagens
# ============================================================
class ContagemCreate(BaseModel):
    igreja: str
    data: date
    horario: Optional[str] = None
    responsavel: Optional[str] = None
    total_visitantes: int = 0
    total_criancas: int = 0
    total_nauta: int = 0
    total_servos: int = 0
    total_templo: int = 0
    total_geral: int = 0
    # dados = objeto livre com todos os campos por ministério
    dados: Optional[dict[str, Any]] = None


class Contagem(ContagemCreate):
    id: int
    usuario_id: Optional[int] = None


# Resolve a referência adiantada em TokenResponse
TokenResponse.model_rebuild()
