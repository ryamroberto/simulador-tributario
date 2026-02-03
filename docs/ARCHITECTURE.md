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
*   **Responsabilidade:** Fornecer estruturas base para outros apps.
*   **Componentes:**
    *   `models.py`: Modelos abstratos (ex: `TimeStampedModel` com `created_at`, `updated_at`).
    *   `utils.py`: Funções utilitárias genéricas.

#### **`apps/companies`**
*   **Responsabilidade:** Gerenciar os dados cadastrais básicos da empresa.
*   **Componentes:**
    *   `models.py`:
        *   `Company`: Armazena faturamento, setor, UF, regime atual e número de funcionários.
    *   `serializers.py`: Validação e serialização dos dados da empresa.
    *   `views.py`: Endpoints para criação e recuperação de dados de empresa (se necessário persistência). *Nota: Para uma simulação puramente stateless, este app pode servir apenas para validação de entrada.*

#### **`apps/simulation`**
*   **Responsabilidade:** Executar a lógica de negócio principal (cálculos tributários).
*   **Componentes:**
    *   `services/`:
        *   `calculator.py`: Lógica pura de cálculo (Tax Calculator). Contém as regras "hardcoded" para "Cenário Atual" e "Cenário Pós-Reforma".
        *   `analyzer.py`: Lógica de comparação (Delta) e classificação (Positivo/Neutro/Negativo).
    *   `models.py`:
        *   `SimulationLog` (Opcional): Para registrar simulações realizadas (histórico simples).
    *   `serializers.py`: Define o contrato de entrada (JSON com dados financeiros) e saída (JSON com resultados).
    *   `views.py`: Endpoint `POST /api/v1/simulate/` que orquestra a chamada aos serviços e retorna o resultado.

## 4. Fluxo de Dados (Data Flow)

1.  **Request:** O cliente envia um `POST` para `/api/v1/simulate/` com um payload JSON contendo:
    *   Dados da Empresa (Faturamento, Regime, Setor, etc.)
    *   Dados Financeiros do Período (Faturamento mês, Custos, etc.)
2.  **Validação:** O `SimulationSerializer` valida os tipos de dados e campos obrigatórios.
3.  **Processamento (Service Layer):**
    *   O `CalculatorService` recebe os dados validados.
    *   Executa `calculate_current_tax(data)` -> Retorna carga atual.
    *   Executa `calculate_reform_tax(data)` -> Retorna carga pós-reforma.
    *   Executa `analyze_impact(current, reformed)` -> Calcula deltas e define a mensagem de sugestão.
4.  **Response:** A API retorna um JSON estruturado com:
    *   Resumo dos Inputs.
    *   Resultados Detalhados (Antes vs. Depois).
    *   Análise de Impacto (Texto + Classificação).

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

## 7. Segurança e Escalabilidade

*   **Segurança:** Uso padrão dos middlewares de segurança do Django. Validação estrita de inputs via Serializers.
*   **Escalabilidade:** Como a simulação é processamento de CPU e não depende de I/O pesado de banco de dados (stateless por natureza), a aplicação escala horizontalmente com facilidade atrás de um Load Balancer se necessário.

## 8. Considerações Finais

Esta arquitetura evita propositalmente a complexidade de microserviços ou estruturas assíncronas (Celery) neste momento, dado o requisito de "simplicidade e clareza". O foco é na robustez da lógica de cálculo (Domínio) e na clareza da API.
