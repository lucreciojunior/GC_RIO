"""Cliente Supabase compartilhado por toda a aplicação."""
from supabase import create_client, Client

from app.config import settings

_client: Client | None = None


def get_supabase() -> Client:
    """Retorna o cliente Supabase (singleton).

    Levanta erro claro se as credenciais não estiverem configuradas.
    """
    global _client

    if _client is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL e SUPABASE_KEY não configurados. "
                "Copie backend/.env.example para backend/.env e preencha os valores."
            )
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    return _client
