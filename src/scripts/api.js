/* ==========================================
   RIO - Camada de dados (Supabase direto)
   Requer: config.js e a lib supabase-js carregada antes deste arquivo.
   ========================================== */

// Cria o cliente Supabase (global window.supabase vem do CDN)
const _sb = window.supabase.createClient(
    SUPABASE_CONFIG.url,
    SUPABASE_CONFIG.anonKey
);

// Domínio interno para o "e-mail sintético".
// O usuário loga só com nome; por baixo usamos nome@rio.local no Auth.
const DOMINIO_INTERNO = "rio.local";

// Converte um nome de usuário em e-mail sintético
function usuarioParaEmail(usuario) {
    const limpo = String(usuario).trim().toLowerCase().replace(/\s+/g, "");
    // Se já for um e-mail, usa como está
    if (limpo.includes("@")) return limpo;
    return `${limpo}@${DOMINIO_INTERNO}`;
}

// ------------------------------------------------------------
// Sessão em cache (perfil do usuário logado)
// ------------------------------------------------------------
function getSessao() {
    const s = sessionStorage.getItem("rio_perfil");
    return s ? JSON.parse(s) : null;
}

function salvarPerfilLocal(perfil) {
    sessionStorage.setItem("rio_perfil", JSON.stringify(perfil));
}

function limparPerfilLocal() {
    sessionStorage.removeItem("rio_perfil");
}

// ------------------------------------------------------------
// Carrega o perfil do usuário logado (nome, perfil, igreja)
// ------------------------------------------------------------
async function carregarPerfil() {
    const { data: { user } } = await _sb.auth.getUser();
    if (!user) return null;

    const { data, error } = await _sb
        .from("perfis")
        .select("*")
        .eq("id", user.id)
        .single();

    if (error || !data) return null;

    const perfil = {
        id: user.id,
        email: user.email,
        nome: data.nome,
        perfil: data.perfil,
        igreja: data.igreja,
    };
    salvarPerfilLocal(perfil);
    return perfil;
}

// ------------------------------------------------------------
// API - operações
// ------------------------------------------------------------
const API = {
    // ---- Autenticação ----
    async login(usuario, senha) {
        const { error } = await _sb.auth.signInWithPassword({
            email: usuarioParaEmail(usuario),
            password: senha,
        });
        if (error) {
            throw new Error("Usuário ou senha incorretos.");
        }
        const perfil = await carregarPerfil();
        if (!perfil) {
            throw new Error("Usuário sem perfil configurado. Contate o administrador.");
        }
        return perfil;
    },

    async logout() {
        await _sb.auth.signOut();
        limparPerfilLocal();
        window.location.href = "login.html";
    },

    // ---- Usuários (perfis) ----
    async listarUsuarios() {
        const { data, error } = await _sb
            .from("perfis")
            .select("*")
            .order("nome");
        if (error) throw new Error(error.message);
        return data;
    },

    // Cria usuário no Auth + perfil (via metadados no cadastro).
    // O login é por nome de usuário; guardamos nome@rio.local no Auth.
    // Usa um client TEMPORÁRIO e isolado para o signUp não derrubar a
    // sessão do admin que está cadastrando (senão o Supabase loga no novo user).
    async criarUsuario({ usuario, senha, nome, perfil, igreja, data_nascimento }) {
        const login = String(usuario).trim().toLowerCase().replace(/\s+/g, "");

        const tempClient = window.supabase.createClient(
            SUPABASE_CONFIG.url,
            SUPABASE_CONFIG.anonKey,
            { auth: { persistSession: false, autoRefreshToken: false } }
        );

        const { data, error } = await tempClient.auth.signUp({
            email: usuarioParaEmail(login),
            password: senha,
            options: {
                data: { nome, usuario: login, perfil, igreja, data_nascimento: data_nascimento || "" },
            },
        });
        if (error) {
            if (String(error.message).toLowerCase().includes("already")) {
                throw new Error("Já existe um usuário com esse nome.");
            }
            throw new Error(error.message);
        }
        return data;
    },

    async atualizarUsuario(id, dados) {
        // Atualiza apenas o perfil (nome/perfil/igreja). Senha/email são geridos no Auth.
        const { data, error } = await _sb
            .from("perfis")
            .update(dados)
            .eq("id", id)
            .select()
            .single();
        if (error) throw new Error(error.message);
        return data;
    },

    async excluirUsuario(id) {
        // Remove o perfil. (A conta no Auth permanece; para remover 100%,
        // é necessário o painel do Supabase ou uma Edge Function.)
        const { error } = await _sb.from("perfis").delete().eq("id", id);
        if (error) throw new Error(error.message);
    },

    // ---- Igrejas ----
    async listarIgrejas() {
        const { data, error } = await _sb.from("igrejas").select("*").order("nome");
        if (error) throw new Error(error.message);
        return data;
    },

    async criarIgreja({ nome }) {
        const { data, error } = await _sb
            .from("igrejas")
            .insert({ nome })
            .select()
            .single();
        if (error) throw new Error(traduzErro(error));
        return data;
    },

    async atualizarIgreja(id, dados) {
        const { data, error } = await _sb
            .from("igrejas")
            .update(dados)
            .eq("id", id)
            .select()
            .single();
        if (error) throw new Error(traduzErro(error));
        return data;
    },

    async excluirIgreja(id) {
        const { error } = await _sb.from("igrejas").delete().eq("id", id);
        if (error) throw new Error(error.message);
    },

    // ---- Contagens ----
    async salvarContagem(contagem) {
        const { data: { user } } = await _sb.auth.getUser();
        const registro = { ...contagem, criado_por: user ? user.id : null };
        const { data, error } = await _sb
            .from("contagens")
            .insert(registro)
            .select()
            .single();
        if (error) throw new Error(error.message);
        return data;
    },

    async listarContagens(filtros = {}) {
        let q = _sb.from("contagens").select("*").order("data", { ascending: false });
        if (filtros.igreja) q = q.eq("igreja", filtros.igreja);
        if (filtros.data_inicio) q = q.gte("data", filtros.data_inicio);
        if (filtros.data_fim) q = q.lte("data", filtros.data_fim);
        const { data, error } = await q;
        if (error) throw new Error(error.message);
        return data;
    },

    // ---- Aniversariantes ----
    // Retorna os perfis com data de nascimento (RLS já filtra por igreja/perfil)
    async listarAniversariantes() {
        const { data, error } = await _sb
            .from("perfis")
            .select("id, nome, usuario, igreja, data_nascimento")
            .not("data_nascimento", "is", null)
            .order("nome");
        if (error) throw new Error(error.message);
        return data;
    },

    // ---- Check-in ----
    // Lista os servos visíveis (RLS filtra por igreja p/ líder, tudo p/ admin)
    async listarServos() {
        const { data, error } = await _sb
            .from("perfis")
            .select("id, nome, usuario, perfil, igreja")
            .order("nome");
        if (error) throw new Error(error.message);
        return data;
    },

    // Lista check-ins de uma data (padrão: hoje), com filtro opcional de igreja
    async listarCheckins(data = null, igreja = null) {
        const dia = data || new Date().toISOString().slice(0, 10);
        let q = _sb.from("checkins").select("*").eq("data", dia).order("horario");
        if (igreja) q = q.eq("igreja", igreja);
        const { data: rows, error } = await q;
        if (error) throw new Error(error.message);
        return rows;
    },

    // Histórico: agrupa check-ins por data (com filtros opcionais)
    async historicoCheckins({ igreja = null, data_inicio = null, data_fim = null } = {}) {
        let q = _sb.from("checkins").select("*").order("data", { ascending: false }).order("horario");
        if (igreja) q = q.eq("igreja", igreja);
        if (data_inicio) q = q.gte("data", data_inicio);
        if (data_fim) q = q.lte("data", data_fim);
        const { data, error } = await q;
        if (error) throw new Error(error.message);
        return data;
    },

    // Marca check-in (próprio ou de outro servo, conforme permissão do RLS)
    async marcarCheckin({ servo_id, servo_nome, igreja, data = null }) {
        const { data: { user } } = await _sb.auth.getUser();
        const registro = {
            servo_id,
            servo_nome,
            igreja,
            marcado_por: user ? user.id : null,
        };
        if (data) registro.data = data;
        const { data: row, error } = await _sb
            .from("checkins")
            .insert(registro)
            .select()
            .single();
        if (error) {
            if (error.code === "23505") throw new Error("Este servo já tem check-in hoje.");
            throw new Error(error.message);
        }
        return row;
    },

    // Desmarca (remove) um check-in
    async desmarcarCheckin(id) {
        const { error } = await _sb.from("checkins").delete().eq("id", id);
        if (error) throw new Error(error.message);
    },

    // ---- Pregações ----
    async listarPregacoes(igreja = null) {
        let q = _sb.from("pregacoes").select("*").order("data");
        if (igreja) q = q.eq("igreja", igreja);
        const { data, error } = await q;
        if (error) throw new Error(error.message);
        return data;
    },
    async criarPregacao(dados) {
        const { data, error } = await _sb.from("pregacoes").insert(dados).select().single();
        if (error) throw new Error(error.message);
        return data;
    },
    async atualizarPregacao(id, dados) {
        const { data, error } = await _sb.from("pregacoes").update(dados).eq("id", id).select().single();
        if (error) throw new Error(error.message);
        return data;
    },
    async excluirPregacao(id) {
        const { error } = await _sb.from("pregacoes").delete().eq("id", id);
        if (error) throw new Error(error.message);
    },

    // ---- Avisos ----
    async listarAvisos(igreja = null) {
        let q = _sb.from("avisos").select("*").order("data");
        if (igreja) q = q.eq("igreja", igreja);
        const { data, error } = await q;
        if (error) throw new Error(error.message);
        return data;
    },
    async criarAviso(dados) {
        const { data, error } = await _sb.from("avisos").insert(dados).select().single();
        if (error) throw new Error(error.message);
        return data;
    },
    async atualizarAviso(id, dados) {
        const { data, error } = await _sb.from("avisos").update(dados).eq("id", id).select().single();
        if (error) throw new Error(error.message);
        return data;
    },
    async excluirAviso(id) {
        const { error } = await _sb.from("avisos").delete().eq("id", id);
        if (error) throw new Error(error.message);
    },
};

// Traduz erros comuns do Postgres para mensagens amigáveis
function traduzErro(error) {
    if (error.code === "23505") return "Já existe um registro com esse nome.";
    return error.message || "Ocorreu um erro.";
}

// ------------------------------------------------------------
// Proteção de páginas
// ------------------------------------------------------------
async function protegerPagina(perfisPermitidos = null) {
    const { data: { session } } = await _sb.auth.getSession();
    if (!session) {
        window.location.href = "login.html";
        return null;
    }

    let perfil = getSessao();
    if (!perfil) {
        perfil = await carregarPerfil();
    }
    if (!perfil) {
        window.location.href = "login.html";
        return null;
    }

    if (perfisPermitidos && !perfisPermitidos.includes(perfil.perfil)) {
        window.location.href = "home.html";
        return null;
    }
    return perfil;
}
