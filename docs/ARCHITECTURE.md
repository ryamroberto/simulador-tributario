# Arquitetura do Sistema - Simulador Tributário Simplificado

## 1. Visão Geral da Arquitetura

O sistema será construído como uma aplicação monolítica modular utilizando o framework **Django** e **Django Rest Framework (DRF)** para exposição de APIs. A arquitetura privilegia a simplicidade e a separação de responsabilidades, facilitando a manutenção e a evolução futura.

O foco é fornecer uma API RESTful (API-first) para simulação de impacto tributário, sem interface de usuário (frontend) neste escopo.

## 2. Tecnologias Principais

*   **Linguagem:** Python 3.x
*   **Framework Web:** Django 5+
*   **API Framework:** Django Rest Framework (DRF)
*   **Banco de Dados:** SQLite (padrão Django para desenvolvimento/simplicidade, facilmente substituível por PostgreSQL se necessário).
*   **Gerenciamento de Dependências:** `pip` / `venv`

## 3. Estrutura de Diretórios e Módulos (Apps)

A aplicação será organizada em "apps" Django isolados, seguindo o princípio de coesão e baixo acoplamento.

```
simulador-tributario/
├── config/                 # Configurações globais do projeto (settings, urls, wsgi)
├── docs/                   # Documentação (PRD, Arquitetura, etc.)
├── apps/                   # Diretório contendo os apps do projeto
│   ├── core/               # App base (utilitários, modelos abstratos, mixins globais)
│   ├── companies/          # Gestão de dados das empresas (cadastro simplificado)
│   └── simulation/         # Motor de cálculo e lógica de simulação tributária
├── manage.py               # Entry point do Django CLI
├── requirements.txt        # Dependências do projeto
└── .gitignore              # Arquivos ignorados pelo git
```

### 3.1. Detalhamento dos Apps

#### **`apps/core`**
*   **Responsabilidade:** Fornecer estruturas base e tratamento global de exceções.
*   **Componentes:**
    *   `exceptions.py`: Custom Exception Handler para tradução de erros de Throttling e outros.
    *   `validators.py`: Validações de CNPJ e regras de negócio comuns.

#### **`apps/companies`**
*   **Responsabilidade:** Gerenciar os dados cadastrais básicos da empresa.
*   **Componentes:**
    *   `models.py`:
        *   `Company`: Armazena faturamento, setor, UF, regime atual e número de funcionários.
    *   `serializers.py`: Validação e serialização dos dados da empresa.

#### **`apps/simulation`**
*   **Responsabilidade:** Executar a lógica de negócio principal, persistência de histórico e exportação.
*   **Componentes:**
    *   `services/`:
        *   `calculator.py`: Lógica pura de cálculo (Tax Calculator).
        *   `analyzer.py`: Impacto (Delta) e classificação. Consome `SuggestionMatrix` dinamicamente.
        *   `exporter.py`: Serviço `DataExporter` para geração de CSV (UTF-8 BOM) e Excel (.xlsx).
        *   `pdf_generator.py`: Geração de relatórios detalhados em PDF.
    *   `models.py`:
        *   `SimulationLog`: Persistência de cada simulação com isolamento por usuário.
        *   `TaxRule`: Regras tributárias persistidas para fácil ajuste administrativo.
        *   `SuggestionMatrix`: Sugestões dinâmicas baseadas em setor e impacto.
    *   `views.py`: Orquestração de endpoints, incluindo Throttling e exportações.

## 4. Fluxo de Dados (Data Flow)

1.  **Request:** O cliente envia requisições autenticadas via JWT para os endpoints do app `simulation`.
2.  **Segurança & Validação:** 
    *   `JWTAuthentication` valida a identidade do usuário.
    *   `Rate Limiting` (Throttling) protege os endpoints contra sobrecarga.
    *   `SimulationInputSerializer` valida a integridade dos dados financeiros.
3.  **Processamento (Service Layer):**
    *   `TaxCalculator` executa os cálculos baseados em regras (persistidas ou hardcoded).
    *   `ImpactAnalyzer` realiza a análise qualitativa consumindo a `SuggestionMatrix` (com cache).
4.  **Persistence & Response:**
    *   A simulação é registrada automaticamente no `SimulationLog` vinculada ao usuário logado.
    *   A API retorna o JSON estruturado ou o arquivo binário (PDF/Excel/CSV) solicitado.

## 5. Design da API (Contrato Simplificado)

**Endpoint:** `POST /api/v1/simulate/`

**Request Payload (Exemplo):**
```json
{
  "company": {
    "regime": "LUCRO_PRESUMIDO",
    "sector": "SERVICOS",
    "state": "SP",
    "employees_count": 10
  },
  "financials": {
    "revenue": 100000.00,
    "costs": 30000.00,
    "payroll": 40000.00
  }
}
```

**Response Payload (Exemplo):**
```json
{
  "input_summary": { ... },
  "results": {
    "current_tax_load": 16300.00,
    "reform_tax_load": 26500.00,
    "delta_value": 10200.00,
    "delta_percentage": 62.58
  },
  "analysis": {
    "impact_classification": "NEGATIVE",
    "message": "Sua carga tributária aumentará significativamente devido à nova alíquota única de IBS/CBS para serviços.",
    "suggestion": "Considere revisar seus créditos tributários e analisar o impacto na precificação."
  }
}
```

## 6. Estratégia de Testes

*   **Testes Unitários (`tests/unit`):** Foco total na lógica de cálculo (`services/calculator.py`). Garantir que para inputs conhecidos (A), a saída seja exatamente (B). Testar cenários de borda (faturamento zero, custos altos, etc.).
*   **Testes de Integração (`tests/integration`):** Validar se o endpoint `/simulate/` aceita o JSON correto e retorna o status 200 com a estrutura esperada.

## 7. Segurança e Resiliência

*   **Autenticação:** JWT (SimpleJWT) em todos os endpoints privados.
*   **Isolamento de Dados:** Filtros forçados por `request.user` garantem que um usuário nunca acesse dados de terceiros.
*   **Throttling:** 
    *   `UserRateThrottle`: 1000/dia.
    *   `ScopedRateThrottle` (scope: `export`): 10/minuto para endpoints pesados.
*   **Performance:** Uso de `LocMemCache` para persistência de regras e sugestões frequentes.

## 8. Considerações Finais

Esta arquitetura evita propositalmente a complexidade de microserviços ou estruturas assíncronas (Celery) neste momento, dado o requisito de "simplicidade e clareza". O foco é na robustez da lógica de cálculo (Domínio) e na clareza da API.
