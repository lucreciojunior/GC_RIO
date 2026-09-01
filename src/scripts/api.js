/* ==========================================
   RIO - Camada de API
   Comunicação com o backend FastAPI
   ========================================== */

// URL base do backend - detecta automaticamente o ambiente.
// - Local (localhost/127.0.0.1): usa o backend local na porta 8000
// - Produção: usa a URL do backend publicado na Vercel
//
// IMPORTANTE: depois de publicar o backend, troque a URL de produção abaixo
// pela URL real do seu backend na Vercel (ex: https://contagem-rio-api.vercel.app)
const API_BASE_URL = (function () {
    const host = window.location.hostname;
    const ehLocal = host === "localhost" || host === "127.0.0.1" || host === "";
    if (ehLocal) {
        return "http://localhost:8000";
    }
    // >>> TROQUE pela URL do seu backend publicado na Vercel <<<
    return "https://contagem-rio-api.vercel.app";
})();

// ------------------------------------------------------------
// Sessão / Token
// ------------------------------------------------------------
function getToken() {
    const sessao = sessionStorage.getItem("rio_sessao");
    if (!sessao) return null;
    try {
        return JSON.parse(sessao).token || null;
    } catch {
        return null;
    }
}

function getSessao() {
    const sessao = sessionStorage.getItem("rio_sessao");
    return sessao ? JSON.parse(sessao) : null;
}

function salvarSessao(dados) {
    sessionStorage.setItem("rio_sessao", JSON.stringify(dados));
}

function limparSessao() {
    sessionStorage.removeItem("rio_sessao");
}

// ------------------------------------------------------------
// Helper genérico de requisição
// ------------------------------------------------------------
async function apiRequest(caminho, opcoes = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(opcoes.headers || {}),
    };

    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    let resposta;
    try {
        resposta = await fetch(`${API_BASE_URL}${caminho}`, {
            ...opcoes,
            headers,
        });
    } catch (erro) {
        throw new Error(
            "Não foi possível conectar ao servidor. Verifique se o backend está rodando."
        );
    }

    // 401 = token inválido/expirado -> volta pro login
    if (resposta.status === 401) {
        limparSessao();
        if (!window.location.pathname.endsWith("login.html")) {
            window.location.href = "login.html";
        }
        throw new Error("Sessão expirada. Faça login novamente.");
    }

    // 204 = sem conteúdo (delete)
    if (resposta.status === 204) {
        return null;
    }

    const dados = await resposta.json().catch(() => ({}));

    if (!resposta.ok) {
        const msg = dados.detail || "Ocorreu um erro na requisição.";
        throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
    }

    return dados;
}

// ------------------------------------------------------------
// API - endpoints organizados
// ------------------------------------------------------------
const API = {
    // Autenticação
    async login(usuario, senha) {
        const dados = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({ usuario, senha }),
        });
        // Salva sessão com token + dados do usuário
        salvarSessao({
            token: dados.access_token,
            ...dados.usuario,
        });
        return dados;
    },

    logout() {
        limparSessao();
        window.location.href = "login.html";
    },

    // Usuários
    listarUsuarios() {
        return apiRequest("/usuarios");
    },
    criarUsuario(usuario) {
        return apiRequest("/usuarios", {
            method: "POST",
            body: JSON.stringify(usuario),
        });
    },
    atualizarUsuario(id, dados) {
        return apiRequest(`/usuarios/${id}`, {
            method: "PUT",
            body: JSON.stringify(dados),
        });
    },
    excluirUsuario(id) {
        return apiRequest(`/usuarios/${id}`, { method: "DELETE" });
    },

    // Igrejas
    listarIgrejas() {
        return apiRequest("/igrejas");
    },
    criarIgreja(igreja) {
        return apiRequest("/igrejas", {
            method: "POST",
            body: JSON.stringify(igreja),
        });
    },
    atualizarIgreja(id, dados) {
        return apiRequest(`/igrejas/${id}`, {
            method: "PUT",
            body: JSON.stringify(dados),
        });
    },
    excluirIgreja(id) {
        return apiRequest(`/igrejas/${id}`, { method: "DELETE" });
    },

    // Contagens
    salvarContagem(contagem) {
        return apiRequest("/contagens", {
            method: "POST",
            body: JSON.stringify(contagem),
        });
    },
    listarContagens(filtros = {}) {
        const params = new URLSearchParams();
        if (filtros.igreja) params.set("igreja", filtros.igreja);
        if (filtros.data_inicio) params.set("data_inicio", filtros.data_inicio);
        if (filtros.data_fim) params.set("data_fim", filtros.data_fim);
        const qs = params.toString();
        return apiRequest(`/contagens${qs ? "?" + qs : ""}`);
    },
};

// ------------------------------------------------------------
// Proteção de páginas
// ------------------------------------------------------------
function protegerPagina(perfisPermitidos = null) {
    const sessao = getSessao();
    if (!sessao || !sessao.token) {
        window.location.href = "login.html";
        return null;
    }
    if (perfisPermitidos && !perfisPermitidos.includes(sessao.perfil)) {
        window.location.href = "home.html";
        return null;
    }
    return sessao;
}
