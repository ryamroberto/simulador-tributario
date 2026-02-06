# STORY-017: Propriedade de Dados e Filtros de Usuário (Ownership)

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar o vínculo de propriedade entre usuários, empresas e logs de simulação. Agora que o sistema possui autenticação JWT, cada registro deve pertencer a um usuário, e as APIs de listagem devem filtrar automaticamente os dados para exibir apenas o que pertence ao usuário autenticado.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Adicionar um campo `user` (ForeignKey para `User`) nos modelos `Company` e `SimulationLog`.
2. [x] No endpoint de cadastro de empresa (`POST /api/v1/companies/`), o usuário autenticado deve ser setado automaticamente como dono.
3. [x] No endpoint de execução de simulação (`POST /api/simulation/simulate/`), o log gerado deve ser vinculado ao usuário autenticado.
4. [x] Refatorar os endpoints de listagem (`GET /api/v1/companies/`, `GET /api/simulation/history/`, `GET /api/simulation/dashboard/`) para retornar apenas os registros onde `user == request.user`.
5. [x] Garantir que ao tentar acessar um detalhe (`retrieve`), editar ou excluir um registro que não pertence ao usuário, o sistema retorne `404 Not Found`.
6. [x] Criar testes unitários validando o isolamento de dados entre dois usuários diferentes.

## Lista de Arquivos
- `apps/companies/models.py`
- `apps/simulation/models.py`
- `apps/companies/views.py`
- `apps/simulation/views.py`
- `apps/simulation/tests.py`

## Tarefas
- [x] Adicionar campo `user` ao modelo `Company` com migração.
- [x] Adicionar campo `user` ao modelo `SimulationLog` com migração.
- [x] Sobrescrever `perform_create` no `CompanyViewSet` para associar o usuário.
- [x] Atualizar `SimulationView` para salvar o usuário no log.
- [x] Sobrescrever `get_queryset` em todas as views de listagem para aplicar o filtro de ownership.
- [x] Escrever testes de "Cross-User Access" (Usuário A tentando ver dados do Usuário B).

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Criação de ForeignKey para `User` com `null=True` para registros legados.
- Uso de `get_queryset` para garantir que o isolamento ocorra no nível do banco de dados (QuerySet level filtering).
- Implementação de `perform_create` em ViewSets e criação direta no log associando `request.user`.
- Validação de isolamento via testes: Usuário B recebe lista vazia ao tentar ver histórico do Usuário A.
- Verificação de que `get_object_or_404` em endpoints de detalhe respeita o filtro de usuário.

### Completion Notes
- Privacidade de dados garantida. Cada usuário agora possui seu ambiente isolado de simulações e empresas.
- O dashboard agrega apenas os dados pertinentes ao usuário logado.

### Change Log
- Atualizados modelos `Company` e `SimulationLog`.
- Geradas migrações de esquema.
- Refatoradas views de Companies e Simulation para suporte a ownership.
- Adicionados testes de isolamento de dados.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Isolamento de Dados:** Implementado com sucesso através da filtragem de QuerySets (`get_queryset`) e atribuição automática de propriedade em `perform_create` e no endpoint de simulação.
  - **Integridade:** Migrações de banco de dados geradas e aplicadas para os modelos `Company` e `SimulationLog`.
  - **Segurança:** Validado que usuários não conseguem acessar, listar ou exportar dados pertencentes a outros usuários (retornando 404 conforme esperado).
  - **Privacidade:** O Dashboard agora reflete métricas agregadas baseadas exclusivamente no histórico do usuário logado.
  - **Testabilidade:** Suite de testes `OwnershipAPITest` cobre cenários críticos de acesso cruzado e privacidade de métricas.
- **Recommendations:** Nenhuma. A arquitetura de autorização segue as melhores práticas do Django Rest Framework.

## 🤖 CodeRabbit Integration
### Story Type Analysis
- **Primary Type:** Security (Authorization)
- **Complexity:** Medium
- **Secondary Types:** Database (Schema change)

### Specialized Agents
- **Primary Agent:** @dev
- **Secondary Agents:** @architect

### Quality Gates
- **Pre-Commit:** @dev (Linting, Unit Tests)
- **Pre-PR:** @github-devops

### Self-Healing Configuration
- **Mode:** light
- **Iterations:** 2
- **Max Time:** 15 min
- **Severity:** CRITICAL only

### Focus Areas
- Integridade das migrações (lidar com registros existentes sem dono).
- Correção dos filtros de QuerySet para evitar vazamento de dados.
- Mensagens de erro em PT-BR.

---
— River, removendo obstáculos 🌊
