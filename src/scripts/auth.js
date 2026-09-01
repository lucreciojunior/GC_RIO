/* ==========================================
   RIO - Autenticação (compatibilidade)
   Este arquivo agora depende de api.js.
   Inclua api.js ANTES de auth.js nas páginas.
   ========================================== */

// Verificar se está logado (redireciona ao login se não)
function verificarSessao() {
    const sessao = getSessao();
    if (!sessao || !sessao.token) {
        window.location.href = "login.html";
        return null;
    }
    return sessao;
}

// Verificar se tem um dos perfis permitidos
function verificarPerfil(perfisPermitidos) {
    const sessao = verificarSessao();
    if (!sessao) return null;

    if (!perfisPermitidos.includes(sessao.perfil)) {
        window.location.href = "home.html";
        return null;
    }
    return sessao;
}

// Logout
function logout() {
    API.logout();
}
