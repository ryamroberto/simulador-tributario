# STORY-020: Implementação de Rate Limiting e Proteção de Endpoints

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Para garantir a estabilidade do sistema e prevenir abusos, especialmente nos novos endpoints de exportação de dados (CSV/Excel), deve ser implementada uma camada de Rate Limiting (Throttling). Isso evitará ataques de negação de serviço (DoS) e garantirá que os recursos do servidor sejam distribuídos de forma justa entre os usuários.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Configurar o Django Rest Framework para suportar Throttling global.
2. [x] Definir um limite padrão para usuários autenticados (ex: 1000 requisições por dia).
3. [x] Definir um limite restrito para os endpoints de exportação:
    - `/api/simulation/export-all-history/`
    - `/api/simulation/export-all-history/excel/`
    - `/api/simulation/export-pdf/`
    - Limite sugerido: 10 requisições por minuto por usuário.
4. [x] Personalizar a resposta de erro para Throttling garantindo que a mensagem esteja em PT-BR (ex: "Limite de requisições excedido. Tente novamente em X segundos.").
5. [x] Adicionar testes automatizados que validem o bloqueio após exceder o limite.

## Lista de Arquivos
- `config/settings.py`
- `apps/simulation/views.py`
- `apps/core/exceptions.py`
- `apps/simulation/tests_throttling.py`

## Tarefas
- [x] Configurar `DEFAULT_THROTTLE_CLASSES` e `DEFAULT_THROTTLE_RATES` no `settings.py`.
- [x] Criar classes de Throttle customizadas se necessário (ex: `ExportRateThrottle`).
- [x] Aplicar as classes de Throttle nas Views específicas de exportação.
- [x] Implementar um custom exception handler para traduzir a mensagem de "Request was throttled".
- [x] Validar o comportamento com testes de carga simulados.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Throttling configurado globalmente em `settings.py`.
- Limite de exportação definido via `ScopedRateThrottle` com escopo `export` (10/min).
- `custom_exception_handler` criado em `apps/core/exceptions.py` para traduzir mensagens de erro para PT-BR.
- Testes automatizados em `apps/simulation/tests_throttling.py` validando o bloqueio e a mensagem.

### Completion Notes
- MVP blindado contra abusos em endpoints pesados de exportação.

### Change Log
- Adicionadas configurações de Throttling em `settings.py`.
- Criado `apps/core/exceptions.py`.
- Atualizado `apps/simulation/views.py` com `ScopedRateThrottle`.
- Criado `apps/simulation/tests_throttling.py`.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Segurança:** Camada de Throttling implementada globalmente para proteção contra abusos de API.
  - **Resiliência:** Limite específico de 10 requisições/minuto para exportações garante que processos pesados não degradem o servidor.
  - **UX/Internacionalização:** Mensagem de erro traduzida com sucesso no `custom_exception_handler`.
  - **Testabilidade:** Cobertura de testes automatizados validada com 100% de sucesso.
- **Recommendations:** Nenhuma ação adicional requerida. MVP protegido.

## 🤖 CodeRabbit Integration
- [ ] Habilitar revisão para esta story.
