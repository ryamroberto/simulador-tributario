# STORY-015: Autenticação e Gestão de Usuários (JWT)

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar um sistema de autenticação robusto utilizando JSON Web Tokens (JWT). Isso permitirá que o sistema identifique os usuários, gerencie sessões seguras e prepare o terreno para que cada usuário acesse apenas suas próprias empresas e simulações.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Instalar e configurar `djangorestframework-simplejwt`.
2. [x] Criar endpoints de autenticação:
    - `POST /api/token/` (Login - gera par de tokens).
    - `POST /api/token/refresh/` (Renovação de token).
3. [x] Criar um endpoint de registro de usuário: `POST /api/users/register/`.
4. [x] Proteger os endpoints existentes (`simulate`, `history`, `dashboard`, `export`) exigindo autenticação.
5. [x] Garantir que mensagens de erro de login/token expirado estejam em PT-BR.
6. [x] Adicionar suporte a `Bearer Token` na documentação do Swagger (Spectacular).
7. [x] Criar testes unitários para o fluxo de registro, login e acesso protegido.

## Lista de Arquivos
- `requirements.txt`
- `config/settings.py`
- `apps/core/serializers.py`
- `apps/core/views.py`
- `apps/simulation/views.py`
- `config/urls.py`
- `apps/simulation/tests.py`

## Tarefas
- [x] Adicionar `djangorestframework-simplejwt` ao `requirements.txt`.
- [x] Configurar `REST_FRAMEWORK` em `settings.py` para usar `JWTAuthentication`.
- [x] Implementar Serializer e View para criação de novos usuários (User Model do Django).
- [x] Atualizar as Views de Simulação com `permission_classes = [IsAuthenticated]`.
- [x] Configurar o `drf-spectacular` para exibir o botão "Authorize" na UI.
- [x] Escrever testes de segurança e atualizar testes de integração existentes.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Configuração do `SIMPLE_JWT` em `settings.py` com tempo de vida de 60 minutos para o access token.
- Implementação da `UserRegistrationView` no app `core` para centralizar gestão de usuários.
- Ajuste global nos testes de integração para usar `force_authenticate`, evitando falhas de 401 Unauthorized após proteção dos endpoints.
- Verificação de 8 testes focados em segurança e integração com sucesso.

### Completion Notes
- A API agora está blindada. O botão "Authorize" no Swagger permite testar os endpoints enviando o token JWT.
- O registro de usuário exige confirmação de senha e valida e-mail único.

### Change Log
- Adicionado fluxo JWT completo.
- Protegidos endpoints de `/simulation/`.
- Adicionado endpoint de registro de usuário.
- Atualizada configuração do Swagger para segurança.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Autenticação:** Implementação bem-sucedida de JWT via `simplejwt`, com tokens de acesso e refresh funcionais.
  - **Segurança:** Blindagem de endpoints críticos (`simulate`, `history`, `dashboard`, `export`) validada via testes.
  - **Cadastro:** Fluxo de registro de usuário com validações de segurança (senha e e-mail único).
  - **Documentação:** Suporte a Bearer Auth integrado ao Swagger UI, facilitando testes manuais.
- **Recommendations:** Para uma próxima fase, considerar a implementação de bloqueio de conta após múltiplas tentativas de login falhas (Brute-force protection).

## 🤖 CodeRabbit Integration
### Story Type Analysis
- **Primary Type:** Security
- **Complexity:** Medium
- **Secondary Types:** API, Architecture

### Specialized Agents
- **Primary Agent:** @dev
- **Secondary Agents:** @architect (para validar o flow de segurança)

### Quality Gates
- **Pre-Commit:** @dev (Linting, Security Tests)
- **Pre-PR:** @github-devops

### Self-Healing Configuration
- **Mode:** light
- **Iterations:** 2
- **Max Time:** 15 min
- **Severity:** CRITICAL only

### Focus Areas
- Armazenamento seguro de senhas (padrão Django).
- Configuração correta do tempo de expiração do Token.
- Respostas de erro claras em PT-BR para o usuário final.

---
— River, removendo obstáculos 🌊
