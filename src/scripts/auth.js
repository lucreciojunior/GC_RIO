/* ==========================================
   RIO - Autenticação (compatibilidade)
   Depende de config.js e api.js (Supabase).
   Carregue nesta ordem: supabase-js, config.js, api.js, auth.js
   ========================================== */

// Protege a página: exige login (async). Retorna o perfil ou redireciona.
async function verificarSessao() {
    return await protegerPagina();
}

// Protege exigindo um dos perfis permitidos (async).
async function verificarPerfil(perfisPermitidos) {
    return await protegerPagina(perfisPermitidos);
}

// Logout
function logout() {
    API.logout();
}
