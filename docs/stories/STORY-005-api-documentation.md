# STORY-005: Documentação da API (Swagger/OpenAPI)

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar a documentação automatizada da API utilizando o padrão OpenAPI 3.0. Isso permitirá que desenvolvedores e parceiros visualizem, testem e integrem o simulador tributário de forma profissional e independente.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. Instalar e configurar a biblioteca `drf-spectacular` (padrão atual para OpenAPI 3 no DRF).
2. A documentação deve estar acessível via `/api/schema/swagger-ui/`.
3. Todos os endpoints das apps `companies` e `simulation` devem estar listados.
4. Os schemas de entrada (Input) e saída (Output) devem detalhar os tipos de dados e campos obrigatórios.
5. Todas as descrições de endpoints, parâmetros e mensagens de erro na interface do Swagger devem estar em Português (PT-BR).
6. O esquema da API deve estar disponível para download em formato YAML/JSON em `/api/schema/`.

## Lista de Arquivos
- `requirements.txt` (atualização)
- `config/settings.py` (configuração do spectacular)
- `config/urls.py` (novas rotas de documentação)
- `apps/simulation/views.py` (ajustes de decorators se necessário)
- `apps/companies/views.py` (ajustes de decorators se necessário)
- `apps/simulation/serializers.py` (ajustes de label e help_text)

## Tarefas
- [x] Adicionar `drf-spectacular` ao `requirements.txt`.
- [x] Configurar `REST_FRAMEWORK` no `settings.py` para usar `drf-spectacular` como schema class.
- [x] Adicionar metadados da API (Título: "API Simulador Tributário", Versão: "1.0.0", Descrição em PT-BR).
- [x] Configurar rotas para `SpectacularAPIView`, `SpectacularSwaggerView` e `SpectacularRedocView`.
- [x] Revisar Serializers para garantir que `help_text` e `label` estão presentes e em PT-BR.
- [x] Validar a visualização dos endpoints de Simulação e Cadastro no Swagger UI.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Instalação do `drf-spectacular`.
- Configuração do `DEFAULT_SCHEMA_CLASS` e `SPECTACULAR_SETTINGS`.
- Criação das rotas de schema e UI (Swagger/Redoc).
- Refatoração da `SimulationView` para incluir `serializer_class` e resolver avisos de geração de schema.
- Adição de `label` e `help_text` em PT-BR no `SimulationInputSerializer`.
- Geração de schema via CLI (`python manage.py spectacular`) validada sem erros.
- Execução de testes em todos os apps afetados com 100% de sucesso.

### Completion Notes
- A documentação está disponível em `/api/schema/swagger-ui/`.
- O padrão OpenAPI 3.0 é seguido rigorosamente.
- Todas as interfaces visuais e metadados estão em Português.

### Change Log
- Adicionada dependência `drf-spectacular`.
- Configurado metadados da API no `settings.py`.
- Integradas rotas de documentação no `urls.py`.
- Adicionados decorators `@extend_schema` nas views para enriquecer a documentação técnica.

---
— Dex, sempre construindo 🔨

## QA Results
### Status: PASS ✅

### Auditoria Técnica
- **Infraestrutura:** Biblioteca `drf-spectacular` corretamente instalada e integrada ao ecossistema do Django Rest Framework.
- **OpenAPI 3.0:** Schema gerado com sucesso via CLI, validando a integridade estrutural da definição da API.
- **Idioma (Regra Crítica):** 100% de conformidade. Títulos, descrições de campos, metadados de enums e mensagens de ajuda estão todos em Português (PT-BR).
- **Testes de Regressão:** 11 testes executados e aprovados (Apps `simulation` e `companies`). A inclusão da documentação não alterou o comportamento funcional dos endpoints.

### Observações
- A interface do Swagger UI em `/api/schema/swagger-ui/` está profissional e pronta para uso por desenvolvedores frontend.
- Os schemas de entrada e saída estão detalhados, o que reduz drasticamente a necessidade de suporte manual para integração.

— Quinn, guardião da qualidade 🛡️

## Qualidade (CodeRabbit)
- Foco em: Completude da documentação e clareza das descrições em Português.

---
— River, removendo obstáculos 🌊
