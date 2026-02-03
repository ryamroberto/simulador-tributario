# STORY-002: Implementação do Modelo de Empresa e Cadastro Base

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar o modelo de dados para a Empresa e os endpoints básicos de API para cadastro e consulta, conforme definido na arquitetura. Este modelo servirá de base para as simulações tributárias.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] O modelo `Company` deve ser criado no app `companies` com os campos: faturamento mensal, setor (Serviços, Comércio, Indústria), UF, regime tributário (Simples Nacional ou Lucro Presumido) e número de funcionários (opcional).
2. [x] Deve ser criado um `TimeStampedModel` no app `core` para ser usado como base.
3. [x] Serializers devem validar os campos obrigatórios e as opções de Enum.
4. [x] Endpoints de API para criar e listar empresas devem estar funcionais em `/api/v1/companies/`.
5. [x] Mensagens de erro e validação devem estar em Português (PT-BR).

## Lista de Arquivos
- `apps/core/models.py`
- `apps/companies/models.py`
- `apps/companies/serializers.py`
- `apps/companies/views.py`
- `apps/companies/urls.py`
- `config/urls.py`
- `config/settings.py`

## Tarefas
- [x] Criar o modelo abstrato `TimeStampedModel` em `apps/core/models.py`.
- [x] Definir o modelo `Company` em `apps/companies/models.py` com as escolhas (Choices) apropriadas.
- [x] Criar migrações e aplicar ao banco de dados.
- [x] Implementar `CompanySerializer` com as validações necessárias.
- [x] Implementar `CompanyViewSet` para operações CRUD básicas.
- [x] Configurar as rotas da API no app `companies` e no projeto global.
- [x] Escrever testes unitários básicos para o modelo e para o endpoint de criação.

## Qualidade (CodeRabbit)
- Foco em: Padrões de modelos Django, nomes de campos e mensagens de erro em PT-BR.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - Modelo `Company` implementado com todos os campos e enums (Setor, UF, Regime).
  - Herança de `TimeStampedModel` aplicada corretamente.
  - Serialização e validação funcionando como esperado.
  - Endpoints em `/api/v1/companies/` validados via testes.
  - **Conformidade de Idioma:** Verificado o uso de `verbose_name`, mensagens de validação e configuração global (`LANGUAGE_CODE`) em PT-BR.
- **Recommendations:** Nenhuma.

## Dev Agent Record
- **Status:** Completed
- **Changes:**
  - Criado `TimeStampedModel` em `apps/core/models.py`.
  - Criado modelo `Company` com enums para Setor, UF e Regime Tributário.
  - Implementado `CompanySerializer` com validação de faturamento e mensagens em PT-BR.
  - Implementado `CompanyViewSet` e roteamento em `/api/v1/companies/`.
  - Configurado `LANGUAGE_CODE = 'pt-br'` no `settings.py`.
- **Tests:** 3 testes unitários criados e passando (Model e API).

---
— River, removendo obstáculos 🌊
