# STORY-013: API de Dashboard e Métricas Agregadas

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Criar um endpoint que forneça métricas consolidadas a partir do histórico de simulações (`SimulationLog`). Este dashboard servirá para análise macro dos impactos da reforma tributária entre os usuários do sistema.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Criar um endpoint `GET /api/simulation/dashboard/`.
2. [x] O endpoint deve retornar um JSON com as seguintes métricas:
    - `total_simulacoes`: Quantidade total de registros no log.
    - `faturamento_medio`: Média do faturamento mensal simulado.
    - `distribuicao_impacto`: Contagem de simulações por classificação (POSITIVO, NEUTRO, NEGATIVO).
    - `top_setores`: Lista dos 3 setores com maior volume de simulações.
    - `comparativo_carga_media`: Média da carga tributária atual vs. Média da carga pós-reforma.
3. [x] As métricas devem ser calculadas em tempo real via agregações do Django ORM (`Sum`, `Avg`, `Count`).
4. [x] O endpoint deve ser otimizado para evitar múltiplas queries ao banco (usar agregadores eficientes).
5. [x] Garantir que os nomes de campos na resposta sigam o padrão snake_case e as labels/mensagens sejam em PT-BR.
6. [x] Criar testes unitários validando a precisão dos cálculos agregados.

## Lista de Arquivos
- `apps/simulation/views.py`
- `apps/simulation/urls.py`
- `apps/simulation/tests.py`

## Tarefas
- [x] Implementar a lógica de agregação utilizando `django.db.models.Count`, `Avg`, etc.
- [x] Criar a `SimulationDashboardView`.
- [x] Configurar a rota em `apps/simulation/urls.py`.
- [x] Escrever testes garantindo que as médias e contagens refletem os dados do banco.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Implementação de queries de agregação (`Avg`, `Count`) no Django ORM.
- Criação de `SimulationDashboardView` retornando JSON estruturado.
- Verificação de 14 testes (incluindo regressão) com sucesso.
- Garantia de arredondamento de valores decimais para 2 casas decimais.

### Completion Notes
- O dashboard fornece uma visão macro em tempo real de todas as simulações.
- As métricas de "Top Setores" e "Distribuição de Impacto" permitem análises qualitativas rápidas.

### Change Log
- Adicionada `SimulationDashboardView`.
- Atualizado `urls.py` com a rota `/dashboard/`.
- Adicionado `SimulationDashboardAPITest` ao arquivo de testes.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Performance:** Agregações realizadas via ORM (`Avg`, `Count`), otimizadas para escala.
  - **Precisão:** Cálculos matemáticos validados via testes unitários com massa de dados variada.
  - **Resiliência:** Tratamento adequado para cenários sem dados (retorno zero em vez de erro).
  - **Internacionalização:** Resposta JSON 100% aderente às regras de PT-BR.
- **Recommendations:** Para visualizações de frontend, considerar a inclusão de filtros de data (mês/ano) no futuro para permitir análises temporais mais granulares.

## 🤖 CodeRabbit Integration
### Story Type Analysis
- **Primary Type:** API
- **Complexity:** Medium
- **Secondary Types:** Database (Aggregation)

### Specialized Agents
- **Primary Agent:** @dev
- **Secondary Agents:** @qa

### Quality Gates
- **Pre-Commit:** @dev (Linting, Unit Tests)
- **Pre-PR:** @github-devops

### Self-Healing Configuration
- **Mode:** light
- **Iterations:** 2
- **Max Time:** 15 min
- **Severity:** CRITICAL only

### Focus Areas
- Performance das agregações (evitar loops Python para cálculos).
- Precisão decimal nos valores médios.
- Coerência dos dados retornados em PT-BR.

---
— River, removendo obstáculos 🌊
