import json
import os

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contagem RIO - Dashboard Gerencial</title>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-green: #2e7d32;
            --primary-light: #4caf50;
            --primary-dark: #1b5e20;
            --accent-green: #81c784;
            --bg-color: #f4f7f6;
            --card-bg: #ffffff;
            --text-color: #333333;
            --text-muted: #666666;
            --border-color: #e0e0e0;
            --shadow: 0 4px 12px rgba(0,0,0,0.05);
            --radius: 12px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Header Styling */
        header {
            background: linear-gradient(135deg, var(--primary-dark), var(--primary-green));
            color: white;
            padding: 30px;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .header-title h1 {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-title h1 span {
            color: var(--accent-green);
        }

        .header-title p {
            font-size: 1rem;
            opacity: 0.9;
            margin-top: 5px;
            font-weight: 300;
        }

        .header-badge {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(5px);
            padding: 10px 20px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Filter Section */
        .filter-section {
            background: var(--card-bg);
            padding: 20px 25px;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 25px;
        }

        .filter-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .filters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .filter-group label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
        }

        .filter-group select, .filter-group input {
            padding: 10px 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
            background-color: #fafafa;
        }

        .filter-group select:focus, .filter-group input:focus {
            border-color: var(--primary-light);
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
            background-color: #fff;
        }

        .search-global {
            position: relative;
            grid-column: 1 / -1;
        }

        .search-global input {
            width: 100%;
            padding-left: 38px;
            background-color: #f0f4f1;
            border: 1px solid #c8e6c9;
        }

        .search-global i {
            position: absolute;
            left: 12px;
            top: 68%;
            transform: translateY(-50%);
            color: var(--primary-green);
        }

        .filter-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 10px;
        }

        .btn-reset {
            background-color: #f5f5f5;
            color: var(--text-color);
            border: 1px solid var(--border-color);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }

        .btn-reset:hover {
            background-color: #e0e0e0;
        }

        /* KPI Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .kpi-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            border-left: 5px solid var(--primary-green);
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: transform 0.2s;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
        }

        .kpi-info h3 {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .kpi-info .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary-dark);
            margin-top: 5px;
        }

        .kpi-icon {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: #e8f5e9;
            color: var(--primary-green);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
        }

        /* Navigation Tabs */
        .tab-nav {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 2px;
        }

        .tab-btn {
            padding: 12px 24px;
            background: none;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            position: relative;
            transition: color 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn:hover {
            color: var(--primary-green);
        }

        .tab-btn.active {
            color: var(--primary-green);
        }

        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 100%;
            height: 4px;
            background-color: var(--primary-green);
            border-radius: 2px 2px 0 0;
        }

        /* Tab Content */
        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Dashboard Charts Layout */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
        }

        .chart-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
        }

        .chart-card.full-width {
            grid-column: 1 / -1;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .chart-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chart-container {
            position: relative;
            min-height: 280px;
            width: 100%;
        }

        /* Table View */
        .table-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 25px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background-color: #f8f9fa;
            color: var(--primary-dark);
            padding: 12px 15px;
            font-weight: 600;
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }

        tbody tr:hover {
            background-color: #f1f8e9;
        }

        .badge-servos {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 20px;
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- Header -->
        <header>
            <div class="header-title">
                <h1><i class="fa-solid fa-church"></i> RIO - <span>Relevante, Integral e Orgânico</span></h1>
                <p>Relatório de Culto & Gestão de Indicadores</p>
            </div>
            <div class="header-badge">
                <i class="fa-solid fa-location-dot"></i> Igreja RIO: ALDEIA
            </div>
        </header>

        <!-- Dynamic Filter Form -->
        <section class="filter-section">
            <div class="filter-title">
                <i class="fa-solid fa-filter"></i> Filtros Avançados e Pesquisa
            </div>
            <div class="filters-grid">
                <div class="filter-group">
                    <label for="filter-igreja">Igreja RIO</label>
                    <select id="filter-igreja">
                        <option value="TODOS">Todas</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label for="filter-data">Data</label>
                    <select id="filter-data">
                        <option value="TODOS">Todas as Datas</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label for="filter-horario">Horário</label>
                    <select id="filter-horario">
                        <option value="TODOS">Todos</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label for="filter-responsavel">Responsável</label>
                    <select id="filter-responsavel">
                        <option value="TODOS">Todos</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label for="filter-ministerio">Ministério</label>
                    <select id="filter-ministerio">
                        <option value="TODOS">Todos</option>
                    </select>
                </div>
                <div class="filter-group search-global">
                    <label for="search-input">Pesquisa Global Dinâmica</label>
                    <i class="fa-solid fa-magnifying-glass"></i>
                    <input type="text" id="search-input" placeholder="Buscar por qualquer palavra-chave...">
                </div>
            </div>
            <div class="filter-actions">
                <button class="btn-reset" onclick="resetFilters()"><i class="fa-solid fa-rotate-left"></i> Limpar Filtros</button>
            </div>
        </section>

        <!-- KPI Metrics -->
        <section class="kpi-grid">
            <div class="kpi-card" style="border-left-color: #2e7d32;">
                <div class="kpi-info">
                    <h3>Total Geral Consolidado</h3>
                    <div class="kpi-value" id="kpi-total-geral">0</div>
                </div>
                <div class="kpi-icon"><i class="fa-solid fa-users"></i></div>
            </div>
            <div class="kpi-card" style="border-left-color: #1565c0;">
                <div class="kpi-info">
                    <h3>Público no Templo</h3>
                    <div class="kpi-value" id="kpi-templo">0</div>
                </div>
                <div class="kpi-icon" style="background-color: #e3f2fd; color: #1565c0;"><i class="fa-solid fa-place-of-worship"></i></div>
            </div>
            <div class="kpi-card" style="border-left-color: #f57c00;">
                <div class="kpi-info">
                    <h3>Equipe de Servos</h3>
                    <div class="kpi-value" id="kpi-servos">0</div>
                </div>
                <div class="kpi-icon" style="background-color: #fff3e0; color: #f57c00;"><i class="fa-solid fa-hands-holding-child"></i></div>
            </div>
            <div class="kpi-card" style="border-left-color: #e91e63;">
                <div class="kpi-info">
                    <h3>Total Crianças & Bebês</h3>
                    <div class="kpi-value" id="kpi-criancas">0</div>
                </div>
                <div class="kpi-icon" style="background-color: #fce4ec; color: #e91e63;"><i class="fa-solid fa-child"></i></div>
            </div>
            <div class="kpi-card" style="border-left-color: #8e24aa;">
                <div class="kpi-info">
                    <h3>Visitantes Integrados</h3>
                    <div class="kpi-value" id="kpi-visitantes">0</div>
                </div>
                <div class="kpi-icon" style="background-color: #f3e5f5; color: #8e24aa;"><i class="fa-solid fa-user-plus"></i></div>
            </div>
            <div class="kpi-card" style="border-left-color: #00838f;">
                <div class="kpi-info">
                    <h3>Total de Veículos</h3>
                    <div class="kpi-value" id="kpi-veiculos">0</div>
                </div>
                <div class="kpi-icon" style="background-color: #e0f7fa; color: #00838f;"><i class="fa-solid fa-car"></i></div>
            </div>
        </section>

        <!-- Navigation Tabs -->
        <div class="tab-nav">
            <button class="tab-btn active" onclick="switchTab('tab-visao-geral')"><i class="fa-solid fa-chart-line"></i> Visão Geral & Evolução</button>
            <button class="tab-btn" onclick="switchTab('tab-ministerios')"><i class="fa-solid fa-chart-pie"></i> Análise por Ministérios</button>
            <button class="tab-btn" onclick="switchTab('tab-estatisticas')"><i class="fa-solid fa-chart-column"></i> Demografia & Operacional</button>
            <button class="tab-btn" onclick="switchTab('tab-dados')"><i class="fa-solid fa-table"></i> Tabela Detalhada</button>
        </div>

        <!-- TAB 1: Visão Geral & Evolução -->
        <div id="tab-visao-geral" class="tab-content active">
            <div class="charts-grid">
                <div class="chart-card full-width">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-chart-line" style="color:var(--primary-green);"></i> Evolução Histórica do Público por Data</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartEvolucao"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-pie-chart" style="color:#1565c0;"></i> Distribuição de Público por Categoria</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartDistribuicaoGeral"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-user-tie" style="color:#f57c00;"></i> Comparativo por Responsáveis de Culto</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartResponsaveis"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: Análise por Ministérios -->
        <div id="tab-ministerios" class="tab-content">
            <div class="charts-grid">
                <div class="chart-card full-width">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-users-gear" style="color:var(--primary-green);"></i> Voluntários / Servos por Ministério</div>
                    </div>
                    <div class="chart-container" style="min-height: 380px;">
                        <canvas id="chartMinisteriosBar"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-baby-carriage" style="color:#e91e63;"></i> Atendimento Infantil & Mídia</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartInfantilMidia"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-handshake" style="color:#8e24aa;"></i> Integração & Atendimento</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartIntegracao"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: Demografia & Operacional -->
        <div id="tab-estatisticas" class="tab-content">
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-square-parking" style="color:#00838f;"></i> RIO Parking (Carros vs Motos)</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartParking"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fa-solid fa-children" style="color:#4caf50;"></i> Distribuição do Público Infantil</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="chartInfantilDetalhe"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: Tabela Detalhada -->
        <div id="tab-dados" class="tab-content">
            <div class="table-card">
                <table id="data-table">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Igreja RIO</th>
                            <th>Responsável</th>
                            <th>Ministério</th>
                            <th>Contagem</th>
                        </tr>
                    </thead>
                    <tbody id="table-body">
                        <!-- Dynamic content -->
                    </tbody>
                </table>
            </div>
        </div>

        <footer>
            <p>&copy; 2026 RIO - Relevante, Integral e Orgânico | Sistema Integrado de Gestão de Cultos</p>
        </footer>
    </div>

    <script>
        // Raw dataset built directly from provided graphics
        const rawData = [
            // Date: 02/08/2026
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "INTEGRAÇÃO SERVOS", contagem: 6, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "INTEGRAÇÃO VISITANTES", contagem: 4, cat: "visitantes" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "INTERCESSÃO", contagem: 4, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "GESTÃO DE CULTO", contagem: 2, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "COMUNICAÇÃO", contagem: 1, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "MIDIA SERVOS", contagem: 4, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "MIDIA ONLINE", contagem: 0, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "RIO BAND", contagem: 9, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "CAFÉ RIO", contagem: 4, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "RIO STORE", contagem: 1, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "GERAÇÃO RIO SERVOS", contagem: 5, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "GERAÇÃO RIO CRIANÇAS", contagem: 28, cat: "criancas" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "NAUTA SERVOS", contagem: 2, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "NAUTA CRIANÇAS", contagem: 16, cat: "nauta" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "BERÇARIO ADULTO", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "BERÇARIO CRIANÇAS", contagem: 4, cat: "criancas" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "RIO PARKING SERVOS", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "RIO PARKING CARROS", contagem: 109, cat: "carros" },
            { igreja: "ALDEIA", data: "02/08/2026", horario: "18:00", responsavel: "Arthur e Victor", ministerio: "RIO PARKING MOTOS", contagem: 17, cat: "motos" },

            // Date: 09/08/2026
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "INTEGRAÇÃO SERVOS", contagem: 5, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "INTEGRAÇÃO VISITANTES", contagem: 3, cat: "visitantes" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "INTERCESSÃO", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "GESTÃO DE CULTO", contagem: 2, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "COMUNICAÇÃO", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "MIDIA SERVOS", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "MIDIA ONLINE", contagem: 12, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "RIO BAND", contagem: 7, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "CAFÉ RIO", contagem: 5, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "RIO STORE", contagem: 1, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "GERAÇÃO RIO SERVOS", contagem: 9, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "GERAÇÃO RIO CRIANÇAS", contagem: 30, cat: "criancas" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "NAUTA SERVOS", contagem: 2, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "NAUTA CRIANÇAS", contagem: 17, cat: "nauta" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "BERÇARIO ADULTO", contagem: 1, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "BERÇARIO CRIANÇAS", contagem: 1, cat: "criancas" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "RIO PARKING SERVOS", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "RIO PARKING CARROS", contagem: 75, cat: "carros" },
            { igreja: "ALDEIA", data: "09/08/2026", horario: "18:00", responsavel: "Ewerton/Valderes", ministerio: "RIO PARKING MOTOS", contagem: 6, cat: "motos" },

            // Date: 16/08/2026
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "INTEGRAÇÃO SERVOS", contagem: 7, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "INTEGRAÇÃO VISITANTES", contagem: 6, cat: "visitantes" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "INTERCESSÃO", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "GESTÃO DE CULTO", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "COMUNICAÇÃO", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "MIDIA SERVOS", contagem: 4, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "MIDIA ONLINE", contagem: 0, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "RIO BAND", contagem: 9, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "CAFÉ RIO", contagem: 4, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "RIO STORE", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "GERAÇÃO RIO SERVOS", contagem: 10, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "GERAÇÃO RIO CRIANÇAS", contagem: 33, cat: "criancas" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "NAUTA SERVOS", contagem: 4, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "NAUTA CRIANÇAS", contagem: 11, cat: "nauta" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "BERÇARIO ADULTO", contagem: 0, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "BERÇARIO CRIANÇAS", contagem: 0, cat: "criancas" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "RIO PARKING SERVOS", contagem: 3, cat: "servos" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "RIO PARKING CARROS", contagem: 98, cat: "carros" },
            { igreja: "ALDEIA", data: "16/08/2026", horario: "18:00", responsavel: "Ewerton/Victor", ministerio: "RIO PARKING MOTOS", contagem: 7, cat: "motos" }
        ];

        // Summary Aggregates by Date from Image Totals
        const totalsByDate = {
            "02/08/2026": { visitantes: 4, criancas: 32, nauta: 16, servos: 41, templo: 258, geral: 351 },
            "09/08/2026": { visitantes: 3, criancas: 31, nauta: 17, servos: 43, templo: 169, geral: 263 },
            "16/08/2026": { visitantes: 6, criancas: 33, nauta: 11, servos: 53, templo: 206, geral: 309 }
        };

        // Chart instances holder
        let charts = {};

        // Populate Select Filters
        function initFilters() {
            const igrejas = [...new Set(rawData.map(d => d.igreja))];
            const datas = [...new Set(rawData.map(d => d.data))];
            const horarios = [...new Set(rawData.map(d => d.horario))];
            const responsaveis = [...new Set(rawData.map(d => d.responsavel))];
            const ministerios = [...new Set(rawData.map(d => d.ministerio))];

            populateSelect("filter-igreja", igrejas);
            populateSelect("filter-data", datas);
            populateSelect("filter-horario", horarios);
            populateSelect("filter-responsavel", responsaveis);
            populateSelect("filter-ministerio", ministerios);

            // Add Event Listeners
            document.querySelectorAll(".filter-section select, #search-input").forEach(el => {
                el.addEventListener("input", updateDashboard);
            });
        }

        function populateSelect(id, values) {
            const select = document.getElementById(id);
            values.forEach(v => {
                const opt = document.createElement("option");
                opt.value = v;
                opt.textContent = v;
                select.appendChild(opt);
            });
        }

        function resetFilters() {
            document.getElementById("filter-igreja").value = "TODOS";
            document.getElementById("filter-data").value = "TODOS";
            document.getElementById("filter-horario").value = "TODOS";
            document.getElementById("filter-responsavel").value = "TODOS";
            document.getElementById("filter-ministerio").value = "TODOS";
            document.getElementById("search-input").value = "";
            updateDashboard();
        }

        // Filter Data Logic
        function getFilteredData() {
            const fIgreja = document.getElementById("filter-igreja").value;
            const fData = document.getElementById("filter-data").value;
            const fHorario = document.getElementById("filter-horario").value;
            const fResponsavel = document.getElementById("filter-responsavel").value;
            const fMinisterio = document.getElementById("filter-ministerio").value;
            const fSearch = document.getElementById("search-input").value.toLowerCase().trim();

            return rawData.filter(item => {
                if (fIgreja !== "TODOS" && item.igreja !== fIgreja) return false;
                if (fData !== "TODOS" && item.data !== fData) return false;
                if (fHorario !== "TODOS" && item.horario !== fHorario) return false;
                if (fResponsavel !== "TODOS" && item.responsavel !== fResponsavel) return false;
                if (fMinisterio !== "TODOS" && item.ministerio !== fMinisterio) return false;
                if (fSearch !== "") {
                    const lineStr = `${item.igreja} ${item.data} ${item.horario} ${item.responsavel} ${item.ministerio} ${item.contagem}`.toLowerCase();
                    if (!lineStr.includes(fSearch)) return false;
                }
                return true;
            });
        }

        // Update Dashboard Elements
        function updateDashboard() {
            const filtered = getFilteredData();
            updateKPIs(filtered);
            updateTable(filtered);
            updateCharts(filtered);
        }

        function updateKPIs(filtered) {
            const activeDates = [...new Set(filtered.map(d => d.data))];
            
            let totalGeral = 0, totalTemplo = 0, totalServos = 0, totalCriancas = 0, totalVisitantes = 0, totalVeiculos = 0;

            // If date is specific or all
            activeDates.forEach(date => {
                if (totalsByDate[date]) {
                    // Adjust proportion if filter filters ministerios specifically
                    const isMinisterioFiltered = document.getElementById("filter-ministerio").value !== "TODOS" || document.getElementById("search-input").value !== "";
                    if (!isMinisterioFiltered) {
                        totalGeral += totalsByDate[date].geral;
                        totalTemplo += totalsByDate[date].templo;
                        totalServos += totalsByDate[date].servos;
                        totalCriancas += totalsByDate[date].criancas + totalsByDate[date].nauta;
                        totalVisitantes += totalsByDate[date].visitantes;
                    }
                }
            });

            // If specific ministry filter is active, compute direct sums from filtered
            if (document.getElementById("filter-ministerio").value !== "TODOS" || document.getElementById("search-input").value !== "" || activeDates.length === 0) {
                totalServos = filtered.filter(f => f.cat === 'servos').reduce((a,b) => a + b.contagem, 0);
                totalCriancas = filtered.filter(f => f.cat === 'criancas' || f.cat === 'nauta').reduce((a,b) => a + b.contagem, 0);
                totalVisitantes = filtered.filter(f => f.cat === 'visitantes').reduce((a,b) => a + b.contagem, 0);
                
                // Recalculate estimated templo and geral based on filtered items
                totalVeiculos = filtered.filter(f => f.cat === 'carros' || f.cat === 'motos').reduce((a,b) => a + b.contagem, 0);
                totalTemplo = totalServos + totalCriancas + totalVisitantes; // base estimation for filtered view
                totalGeral = totalTemplo;
            } else {
                totalVeiculos = filtered.filter(f => f.cat === 'carros' || f.cat === 'motos').reduce((a,b) => a + b.contagem, 0);
            }

            document.getElementById("kpi-total-geral").textContent = totalGeral.toLocaleString();
            document.getElementById("kpi-templo").textContent = totalTemplo.toLocaleString();
            document.getElementById("kpi-servos").textContent = totalServos.toLocaleString();
            document.getElementById("kpi-criancas").textContent = totalCriancas.toLocaleString();
            document.getElementById("kpi-visitantes").textContent = totalVisitantes.toLocaleString();
            document.getElementById("kpi-veiculos").textContent = totalVeiculos.toLocaleString();
        }

        function updateTable(filtered) {
            const tbody = document.getElementById("table-body");
            tbody.innerHTML = "";

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 20px; color: var(--text-muted);">Nenhum registro encontrado para os filtros selecionados.</td></tr>`;
                return;
            }

            filtered.forEach(item => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${item.data}</td>
                    <td>${item.horario}</td>
                    <td><strong>${item.igreja}</strong></td>
                    <td>${item.responsavel}</td>
                    <td>${item.ministerio}</td>
                    <td><span class="badge-servos">${item.contagem}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Initialize & Render Charts
        function updateCharts(filtered) {
            const dates = ["02/08/2026", "09/08/2026", "16/08/2026"];
            const activeDates = dates.filter(d => filtered.some(f => f.data === d));

            // Chart 1: Evolução Histórica
            const evolucaoDataGeral = activeDates.map(d => totalsByDate[d] ? totalsByDate[d].geral : 0);
            const evolucaoDataTemplo = activeDates.map(d => totalsByDate[d] ? totalsByDate[d].templo : 0);
            const evolucaoDataServos = activeDates.map(d => totalsByDate[d] ? totalsByDate[d].servos : 0);

            renderChart("chartEvolucao", "line", {
                labels: activeDates,
                datasets: [
                    { label: "Total Geral", data: evolucaoDataGeral, borderColor: "#2e7d32", backgroundColor: "rgba(46, 125, 50, 0.1)", fill: true, tension: 0.3 },
                    { label: "Público Templo", data: evolucaoDataTemplo, borderColor: "#1565c0", backgroundColor: "transparent", borderDash: [5, 5], tension: 0.3 },
                    { label: "Equipe de Servos", data: evolucaoDataServos, borderColor: "#f57c00", backgroundColor: "transparent", tension: 0.3 }
                ]
            });

            // Chart 2: Distribuição Geral (Pie/Doughnut)
            const sumServos = activeDates.reduce((acc, d) => acc + (totalsByDate[d]?.servos || 0), 0);
            const sumCriancas = activeDates.reduce((acc, d) => acc + (totalsByDate[d]?.criancas || 0), 0);
            const sumNauta = activeDates.reduce((acc, d) => acc + (totalsByDate[d]?.nauta || 0), 0);
            const sumVisitantes = activeDates.reduce((acc, d) => acc + (totalsByDate[d]?.visitantes || 0), 0);

            renderChart("chartDistribuicaoGeral", "doughnut", {
                labels: ["Servos", "Crianças (Geração)", "Nauta", "Visitantes"],
                datasets: [{
                    data: [sumServos, sumCriancas, sumNauta, sumVisitantes],
                    backgroundColor: ["#f57c00", "#e91e63", "#00bcd4", "#8e24aa"]
                }]
            });

            // Chart 3: Comparativo por Responsáveis
            const respMap = {};
            filtered.forEach(f => {
                if (!respMap[f.responsavel]) respMap[f.responsavel] = 0;
                respMap[f.responsavel] += f.contagem;
            });

            renderChart("chartResponsaveis", "bar", {
                labels: Object.keys(respMap),
                datasets: [{
                    label: "Total de Registros/Contagens",
                    data: Object.values(respMap),
                    backgroundColor: ["#2e7d32", "#1565c0", "#8e24aa"]
                }]
            });

            // Chart 4: Voluntários por Ministério
            const minMap = {};
            filtered.filter(f => f.cat === "servos").forEach(f => {
                if (!minMap[f.ministerio]) minMap[f.ministerio] = 0;
                minMap[f.ministerio] += f.contagem;
            });

            renderChart("chartMinisteriosBar", "bar", {
                labels: Object.keys(minMap),
                datasets: [{
                    label: "Quantidade de Servos",
                    data: Object.values(minMap),
                    backgroundColor: "#4caf50",
                    borderRadius: 6
                }]
            }, { indexAxis: 'y' });

            // Chart 5: Infantil & Mídia
            const geracaoCount = filtered.filter(f => f.ministerio.includes("GERAÇÃO")).reduce((a,b) => a + b.contagem, 0);
            const nautaCount = filtered.filter(f => f.ministerio.includes("NAUTA")).reduce((a,b) => a + b.contagem, 0);
            const bercarioCount = filtered.filter(f => f.ministerio.includes("BERÇARIO")).reduce((a,b) => a + b.contagem, 0);
            const midiaCount = filtered.filter(f => f.ministerio.includes("MIDIA")).reduce((a,b) => a + b.contagem, 0);

            renderChart("chartInfantilMidia", "polarArea", {
                labels: ["Geração RIO", "Nauta", "Berçário", "Mídia RIO"],
                datasets: [{
                    data: [geracaoCount, nautaCount, bercarioCount, midiaCount],
                    backgroundColor: ["#e91e63", "#00bcd4", "#ffb74d", "#9c27b0"]
                }]
            });

            // Chart 6: Integração
            const integServos = filtered.filter(f => f.ministerio === "INTEGRAÇÃO SERVOS").reduce((a,b) => a + b.contagem, 0);
            const integVisitantes = filtered.filter(f => f.ministerio === "INTEGRAÇÃO VISITANTES").reduce((a,b) => a + b.contagem, 0);

            renderChart("chartIntegracao", "bar", {
                labels: ["Integração Servos", "Integração Visitantes"],
                datasets: [{
                    label: "Atendimentos",
                    data: [integServos, integVisitantes],
                    backgroundColor: ["#2e7d32", "#8e24aa"]
                }]
            });

            // Chart 7: Parking
            const carros = filtered.filter(f => f.ministerio === "RIO PARKING CARROS").reduce((a,b) => a + b.contagem, 0);
            const motos = filtered.filter(f => f.ministerio === "RIO PARKING MOTOS").reduce((a,b) => a + b.contagem, 0);
            const parkingServos = filtered.filter(f => f.ministerio === "RIO PARKING SERVOS").reduce((a,b) => a + b.contagem, 0);

            renderChart("chartParking", "doughnut", {
                labels: ["Carros", "Motos", "Servos Parking"],
                datasets: [{
                    data: [carros, motos, parkingServos],
                    backgroundColor: ["#00838f", "#ff9800", "#4caf50"]
                }]
            });

            // Chart 8: Infantil Detalhe
            const criancasGeral = activeDates.map(d => totalsByDate[d] ? totalsByDate[d].criancas : 0);
            const nautaGeral = activeDates.map(d => totalsByDate[d] ? totalsByDate[d].nauta : 0);

            renderChart("chartInfantilDetalhe", "bar", {
                labels: activeDates,
                datasets: [
                    { label: "Crianças (Geração/Berçário)", data: criancasGeral, backgroundColor: "#e91e63" },
                    { label: "Nauta", data: nautaGeral, backgroundColor: "#00bcd4" }
                ]
            });
        }

        function renderChart(canvasId, type, data, options = {}) {
            if (charts[canvasId]) {
                charts[canvasId].destroy();
            }

            const ctx = document.getElementById(canvasId).getContext("2d");
            charts[canvasId] = new Chart(ctx, {
                type: type,
                data: data,
                options: Object.assign({
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { font: { family: 'Inter', size: 12 } }
                        }
                    }
                }, options)
            });
        }

        // Tab Switcher
        function switchTab(tabId) {
            document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(content => content.classList.remove("active"));

            event.currentTarget.classList.add("active");
            document.getElementById(tabId).classList.add("active");
        }

        // Run on load
        window.onload = function() {
            initFilters();
            updateDashboard();
        };
    </script>
</body>
</html>
"""

# Gera o HTML na pasta de pages
output_dir = os.path.join(os.path.dirname(__file__), "..", "pages")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "Contagem_RIO.html")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✓ Dashboard gerado com sucesso em: {output_path}")