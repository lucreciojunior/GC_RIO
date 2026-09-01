"""Cria (ou atualiza) o usuário admin padrão no Supabase com a senha correta.

Uso:
    cd backend
    python seed_admin.py

Requer o arquivo .env configurado com SUPABASE_URL e SUPABASE_KEY.
"""
from app.database import get_supabase
from app.security import hash_senha


def seed():
    supabase = get_supabase()

    usuario = "admin"
    senha = "admin"
    nome = "Administrador"
    perfil = "admin"
    igreja = "PRADO"

    senha_hash = hash_senha(senha)

    # Verifica se já existe
    existente = supabase.table("usuarios").select("id").eq("usuario", usuario).execute()

    if existente.data:
        supabase.table("usuarios").update({
            "senha_hash": senha_hash,
            "nome": nome,
            "perfil": perfil,
            "igreja": igreja,
        }).eq("usuario", usuario).execute()
        print(f"Admin atualizado. Login: {usuario} / Senha: {senha}")
    else:
        supabase.table("usuarios").insert({
            "nome": nome,
            "usuario": usuario,
            "senha_hash": senha_hash,
            "perfil": perfil,
            "igreja": igreja,
        }).execute()
        print(f"Admin criado. Login: {usuario} / Senha: {senha}")

    print("Lembre-se de trocar a senha após o primeiro login.")


if __name__ == "__main__":
    seed()
