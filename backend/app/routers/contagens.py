"""Rotas de contagens de culto: salvar e listar."""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_supabase
from app.dependencies import get_usuario_atual
from app.models import ContagemCreate, Contagem, UsuarioPublico

router = APIRouter(prefix="/contagens", tags=["Contagens"])


@router.post("", response_model=Contagem, status_code=status.HTTP_201_CREATED)
def salvar_contagem(
    dados: ContagemCreate,
    usuario: UsuarioPublico = Depends(get_usuario_atual),
):
    """Salva uma nova contagem de culto.

    Servo e líder só podem lançar para a própria igreja.
    Admin pode lançar para qualquer igreja.
    """
    supabase = get_supabase()

    igreja = dados.igreja
    if usuario.perfil != "admin":
        # Força a igreja do usuário, ignorando o que veio no payload
        if usuario.igreja:
            igreja = usuario.igreja
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seu usuário não está vinculado a uma igreja.",
            )

    registro = {
        "igreja": igreja,
        "data": dados.data.isoformat(),
        "horario": dados.horario,
        "responsavel": dados.responsavel,
        "total_visitantes": dados.total_visitantes,
        "total_criancas": dados.total_criancas,
        "total_nauta": dados.total_nauta,
        "total_servos": dados.total_servos,
        "total_templo": dados.total_templo,
        "total_geral": dados.total_geral,
        "dados": dados.dados,
        "usuario_id": usuario.id,
    }

    resultado = supabase.table("contagens").insert(registro).execute()
    return resultado.data[0]


@router.get("", response_model=list[Contagem])
def listar_contagens(
    igreja: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    usuario: UsuarioPublico = Depends(get_usuario_atual),
):
    """Lista contagens com filtros opcionais.

    Servo e líder só veem contagens da própria igreja.
    Admin vê de todas (ou filtra por igreja).
    """
    supabase = get_supabase()
    query = supabase.table("contagens").select("*")

    # Restrição por perfil
    if usuario.perfil != "admin":
        query = query.eq("igreja", usuario.igreja or "")
    elif igreja:
        query = query.eq("igreja", igreja)

    if data_inicio:
        query = query.gte("data", data_inicio.isoformat())
    if data_fim:
        query = query.lte("data", data_fim.isoformat())

    resultado = query.order("data", desc=True).execute()
    return resultado.data


@router.get("/{contagem_id}", response_model=Contagem)
def obter_contagem(
    contagem_id: int,
    usuario: UsuarioPublico = Depends(get_usuario_atual),
):
    """Retorna uma contagem específica, respeitando a restrição por igreja."""
    supabase = get_supabase()
    resultado = supabase.table("contagens").select("*").eq("id", contagem_id).execute()

    if not resultado.data:
        raise HTTPException(status_code=404, detail="Contagem não encontrada.")

    contagem = resultado.data[0]

    if usuario.perfil != "admin" and contagem["igreja"] != usuario.igreja:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem acesso a esta contagem.",
        )

    return contagem
