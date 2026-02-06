# STORY-012: API de Listagem do Histórico de Simulações

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Criar um endpoint para que os usuários (ou sistemas externos) possam consultar o histórico de simulações realizadas. Atualmente, o histórico é salvo no banco de dados (`SimulationLog`), mas só é acessível via Django Admin. Esta story visa expor esses dados de forma estruturada via API.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Criar um endpoint `GET /api/simulation/history/`.
2. [x] O endpoint deve retornar uma lista paginada de simulações.
3. [x] Deve ser possível filtrar o histórico por `company_id` via query parameter (ex: `?company=1`).
4. [x] Os resultados devem ser ordenados do mais recente para o mais antigo (`created_at` descendente).
5. [x] Incluir campos essenciais na resposta: data da simulação, faturamento, regime, setor, carga atual, carga reforma e a classificação do impacto.
6. [x] Garantir que os campos monetários sejam formatados com 2 casas decimais.
7. [x] Criar testes unitários para o endpoint, validando filtros e paginação.

## Lista de Arquivos
- `apps/simulation/serializers.py`
- `apps/simulation/views.py`
- `apps/simulation/urls.py`
- `apps/simulation/tests.py`

## Tarefas
- [x] Criar `SimulationLogSerializer` focado em leitura com descrições em PT-BR.
- [x] Implementar `SimulationHistoryView` utilizando as facilidades de listagem do DRF e `PageNumberPagination`.
- [x] Adicionar `django-filter` para filtragem por `company`.
- [x] Registrar a rota em `apps/simulation/urls.py`.
- [x] Validar a saída JSON em relação à regra de PT-BR.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Implementação do `SimulationLogListSerializer` com campos de descrição (`get_FIELD_display`).
- Configuração de `StandardResultsSetPagination` para cumprir requisito de paginação.
- Resolução de conflito de importação Django (`RuntimeError`) padronizando imports para remover o prefixo `apps.`.
- Correção de `IntegrityError` nos testes ao adicionar campos obrigatórios de `Company`.
- Ajuste nos testes para lidar com a estrutura de resposta paginada (`results`).

### Completion Notes
- O endpoint `/api/simulation/history/` está totalmente funcional com paginação e filtros.
- A saída está 100% em conformidade com as regras de internacionalização (PT-BR).

### Change Log
- Adicionado `SimulationLogListSerializer`.
- Adicionada `SimulationHistoryView` com paginação e filtros.
- Atualizado `urls.py`.
- Adicionados testes de integração para o histórico.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Funcionalidade:** Endpoint `/api/simulation/history/` implementado com sucesso, incluindo paginação e filtros por empresa.
  - **Internacionalização:** 100% em conformidade com as regras de PT-BR (uso de descrições amigáveis no serializer).
  - **Testabilidade:** Testes de integração robustos cobrindo filtros e estrutura de resposta.
  - **Performance:** Uso de paginação garante a escalabilidade do endpoint.
- **Recommendations:** Em uma fase futura com autenticação, garantir que a listagem seja restrita aos registros pertencentes ao usuário autenticado.

## 🤖 CodeRabbit Integration
### Story Type Analysis
- **Primary Type:** API
- **Complexity:** Low
- **Secondary Types:** Database (Query)

### Specialized Agents
- **Primary Agent:** @dev
- **Secondary Agents:** @qa (para validar paginação e filtros)

### Quality Gates
- **Pre-Commit:** @dev (Linting, Unit Tests)
- **Pre-PR:** @github-devops (Verify integration tests)

### Self-Healing Configuration
- **Mode:** light
- **Iterations:** 2
- **Max Time:** 15 min
- **Severity:** CRITICAL only

### Focus Areas
- Performance da query (evitar N+1 se houver relacionamentos).
- Precisão na serialização de campos Decimal.
- Adesão estrita ao PT-BR nas mensagens e documentação da API.

---
— River, removendo obstáculos 🌊
