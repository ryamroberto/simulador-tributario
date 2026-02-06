# STORY-018: API de Gestão de Regras e Sugestões (Admin)

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Expor as regras tributárias (`TaxRule`) e a matriz de sugestões (`SuggestionMatrix`) via API para permitir a gestão remota e programática desses dados. O acesso a estes endpoints deve ser restrito exclusivamente a usuários administradores (`is_staff`).

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Criar ViewSets para CRUD completo de `TaxRule`.
2. [x] Criar ViewSets para CRUD completo de `SuggestionMatrix`.
3. [x] Proteger os endpoints com a permissão `IsAdminUser` do DRF.
4. [x] Registrar os endpoints sob o prefixo `/api/management/`.
5. [x] Garantir que as alterações via API invalidem o cache (conectar com os Signals já existentes).
6. [x] Documentar os endpoints no Swagger sob a tag `Gestão`.
7. [x] Criar testes unitários validando que usuários comuns recebem `403 Forbidden` e administradores conseguem realizar o CRUD.

## Lista de Arquivos
- `apps/simulation/serializers.py`
- `apps/simulation/views.py`
- `apps/simulation/urls.py`
- `apps/simulation/tests.py`

## Tarefas
- [x] Implementar `TaxRuleSerializer` e `SuggestionMatrixSerializer`.
- [x] Implementar `TaxRuleViewSet` e `SuggestionMatrixViewSet` com `permission_classes = [IsAdminUser]`.
- [x] Configurar as rotas no `urls.py`.
- [x] Validar se o salvamento via API dispara o `post_save` signal para limpar o cache.
- [x] Escrever testes de segurança (permissão de administrador) e CRUD.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Criação de serializers para os modelos de domínio fiscais.
- Implementação de ViewSets baseados em `ModelViewSet` para permitir o CRUD completo via API.
- Configuração de roteamento amigável sob `/management/`.
- Verificação de que o Django Signals (`post_save`) limpa corretamente o cache quando uma alíquota é alterada via endpoint administrativo.
- Resolução de conflito nos testes causado por dados pré-populados, ajustando as verificações para serem resilientes à massa de dados inicial.

### Completion Notes
- O sistema de simulação agora pode ter suas regras fiscais alteradas em tempo real via API por um admin.
- O cache é invalidado instantaneamente, garantindo que a próxima simulação use as regras novas.

### Change Log
- Adicionados serializers de gestão.
- Adicionadas views administrativas com permissão `IsAdminUser`.
- Integrado roteador DRF em `urls.py`.
- Adicionada suíte de testes de gestão.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Controle de Acesso:** Implementada restrição via `IsAdminUser`, protegendo as regras de negócio de acessos não autorizados.
  - **Sincronização de Cache:** Validado que atualizações via API disparam a limpeza do cache, garantindo integridade dos cálculos.
  - **Interface Administrativa:** Endpoints CRUD funcionais e devidamente documentados no Swagger sob a tag 'Gestão'.
  - **Internacionalização:** Labels, resumos e descrições em total conformidade com a regra de PT-BR.
- **Recommendations:** Para escala futura, considerar o registro de logs de auditoria (`SimulationLog`) também para alterações de regras, permitindo rastrear quem alterou uma alíquota e quando.

## 🤖 CodeRabbit Integration
### Story Type Analysis
- **Primary Type:** API
- **Complexity:** Low
- **Secondary Types:** Security (Authorization)

### Specialized Agents
- **Primary Agent:** @dev
- **Secondary Agents:** @qa

### Quality Gates
- **Pre-Commit:** @dev (Unit Tests)
- **Pre-PR:** @github-devops

### Self-Healing Configuration
- **Mode:** light
- **Iterations:** 2
- **Max Time:** 15 min
- **Severity:** CRITICAL only

### Focus Areas
- Rigor na validação de permissões (impedir acesso de usuários comuns).
- Consistência dos dados decimais ao editar alíquotas.
- Mensagens de erro em PT-BR para violação de permissão.

---
— River, removendo obstáculos 🌊
