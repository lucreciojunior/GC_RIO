"""Rotas de gerenciamento de usuários (restrito a admin)."""
from fastapi import APIRouter, HTTPException, status, Depends

from app.database import get_supabase
from app.security import hash_senha
from app.dependencies import requer_admin
from app.models import UsuarioCreate, UsuarioUpdate, UsuarioPublico

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


def _para_publico(user: dict) -> UsuarioPublico:
    return UsuarioPublico(
        id=user["id"],
        nome=user["nome"],
        usuario=user["usuario"],
        perfil=user["perfil"],
        igreja=user.get("igreja"),
    )


@router.get("", response_model=list[UsuarioPublico])
def listar_usuarios(_admin=Depends(requer_admin)):
    """Lista todos os usuários (sem as senhas)."""
    supabase = get_supabase()
    resultado = supabase.table("usuarios").select("*").order("id").execute()
    return [_para_publico(u) for u in resultado.data]


@router.post("", response_model=UsuarioPublico, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, _admin=Depends(requer_admin)):
    """Cadastra um novo usuário."""
    supabase = get_supabase()
    usuario = dados.usuario.strip().lower()

    # Checa duplicidade
    existente = supabase.table("usuarios").select("id").eq("usuario", usuario).execute()
    if existente.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esse nome de usuário já está em uso.",
        )

    novo = {
        "nome": dados.nome.strip(),
        "usuario": usuario,
        "senha_hash": hash_senha(dados.senha),
        "perfil": dados.perfil,
        "igreja": dados.igreja,
    }
    resultado = supabase.table("usuarios").insert(novo).execute()
    return _para_publico(resultado.data[0])


@router.put("/{usuario_id}", response_model=UsuarioPublico)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, _admin=Depends(requer_admin)):
    """Atualiza um usuário existente."""
    supabase = get_supabase()

    existente = supabase.table("usuarios").select("*").eq("id", usuario_id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    atualizacao: dict = {}
    if dados.nome is not None:
        atualizacao["nome"] = dados.nome.strip()
    if dados.usuario is not None:
        novo_usuario = dados.usuario.strip().lower()
        # Checa duplicidade com outro usuário
        dup = (
            supabase.table("usuarios")
            .select("id")
            .eq("usuario", novo_usuario)
            .neq("id", usuario_id)
            .execute()
        )
        if dup.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esse nome de usuário já está em uso por outra pessoa.",
            )
        atualizacao["usuario"] = novo_usuario
    if dados.senha is not None:
        atualizacao["senha_hash"] = hash_senha(dados.senha)
    if dados.perfil is not None:
        atualizacao["perfil"] = dados.perfil
    if dados.igreja is not None:
        atualizacao["igreja"] = dados.igreja

    if not atualizacao:
        return _para_publico(existente.data[0])

    resultado = (
        supabase.table("usuarios").update(atualizacao).eq("id", usuario_id).execute()
    )
    return _para_publico(resultado.data[0])


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_usuario(usuario_id: int, admin=Depends(requer_admin)):
    """Exclui um usuário. Impede o admin de excluir a si mesmo."""
    supabase = get_supabase()

    if usuario_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode excluir o próprio usuário logado.",
        )

    existente = supabase.table("usuarios").select("id").eq("id", usuario_id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    supabase.table("usuarios").delete().eq("id", usuario_id).execute()
    return None
