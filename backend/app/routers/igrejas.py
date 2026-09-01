"""Rotas de gerenciamento de igrejas.

Listagem é liberada para qualquer usuário logado (para preencher selects).
Criar/editar/excluir é restrito a admin.
"""
from fastapi import APIRouter, HTTPException, status, Depends

from app.database import get_supabase
from app.dependencies import requer_admin, get_usuario_atual
from app.models import IgrejaCreate, IgrejaUpdate, Igreja

router = APIRouter(prefix="/igrejas", tags=["Igrejas"])


@router.get("", response_model=list[Igreja])
def listar_igrejas(_usuario=Depends(get_usuario_atual)):
    """Lista todas as igrejas (qualquer usuário logado)."""
    supabase = get_supabase()
    resultado = supabase.table("igrejas").select("*").order("nome").execute()
    return resultado.data


@router.post("", response_model=Igreja, status_code=status.HTTP_201_CREATED)
def criar_igreja(dados: IgrejaCreate, _admin=Depends(requer_admin)):
    """Cadastra uma nova igreja."""
    supabase = get_supabase()
    nome = dados.nome.strip().upper()

    existente = supabase.table("igrejas").select("id").eq("nome", nome).execute()
    if existente.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma igreja com esse nome.",
        )

    nova = {"nome": nome, "endereco": dados.endereco}
    resultado = supabase.table("igrejas").insert(nova).execute()
    return resultado.data[0]


@router.put("/{igreja_id}", response_model=Igreja)
def atualizar_igreja(igreja_id: int, dados: IgrejaUpdate, _admin=Depends(requer_admin)):
    """Atualiza uma igreja. Se o nome mudar, atualiza os usuários vinculados."""
    supabase = get_supabase()

    existente = supabase.table("igrejas").select("*").eq("id", igreja_id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Igreja não encontrada.")

    nome_antigo = existente.data[0]["nome"]
    atualizacao: dict = {}

    if dados.nome is not None:
        novo_nome = dados.nome.strip().upper()
        dup = (
            supabase.table("igrejas")
            .select("id")
            .eq("nome", novo_nome)
            .neq("id", igreja_id)
            .execute()
        )
        if dup.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outra igreja com esse nome.",
            )
        atualizacao["nome"] = novo_nome

    if dados.endereco is not None:
        atualizacao["endereco"] = dados.endereco

    if not atualizacao:
        return existente.data[0]

    resultado = supabase.table("igrejas").update(atualizacao).eq("id", igreja_id).execute()

    # Se o nome mudou, atualiza os usuários vinculados
    novo_nome = atualizacao.get("nome")
    if novo_nome and novo_nome != nome_antigo:
        supabase.table("usuarios").update({"igreja": novo_nome}).eq(
            "igreja", nome_antigo
        ).execute()

    return resultado.data[0]


@router.delete("/{igreja_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_igreja(igreja_id: int, _admin=Depends(requer_admin)):
    """Exclui uma igreja."""
    supabase = get_supabase()

    existente = supabase.table("igrejas").select("id").eq("id", igreja_id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Igreja não encontrada.")

    supabase.table("igrejas").delete().eq("id", igreja_id).execute()
    return None
