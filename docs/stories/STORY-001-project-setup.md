# STORY-001: Inicialização do Projeto e Estrutura de Apps

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Configurar a estrutura base do projeto Django seguindo a arquitetura definida em `docs/ARCHITECTURE.md`. Isso inclui a instalação do Django Rest Framework (DRF), a organização dos aplicativos dentro de um diretório `apps/` e a configuração inicial do `settings.py`.

## Critérios de Aceite
1. [x] O diretório `apps/` deve ser criado e conter os apps: `core`, `companies` e `simulation`.
2. [x] O `djangorestframework` deve estar listado no `requirements.txt` (ou instalado no venv) e adicionado ao `INSTALLED_APPS`.
3. [x] O `settings.py` deve estar configurado para reconhecer o caminho dos apps dentro de `apps/`.
4. [x] Os apps existentes (`empresas`, `regras_tributarias`, `simulaçoes`) devem ser migrados ou removidos em favor da nova estrutura.
5. [x] O comando `python manage.py check` deve rodar sem erros.

## Lista de Arquivos
- `requirements.txt`
- `config/settings.py`
- `apps/core/apps.py`
- `apps/companies/apps.py`
- `apps/simulation/apps.py`

## Tarefas
- [x] Criar o arquivo `requirements.txt` com as dependências básicas.
- [x] Criar o diretório `apps/` e inicializar os apps `core`, `companies` e `simulation`.
- [x] Mover/Refatorar lógica dos apps antigos para a nova estrutura.
- [x] Configurar `settings.py` (INSTALLED_APPS, DRF config).
- [x] Validar a instalação com um teste de fumaça (smoke test).

## Qualidade (CodeRabbit)
- Foco em: Organização de diretórios e padrões de nomenclatura Django.

## Dev Agent Record
- **Status:** Ready for Review
- **Changes:**
  - Criado `requirements.txt`.
  - Criada estrutura de pastas `apps/`.
  - Inicializados apps `core`, `companies` e `simulation`.
  - Removidos apps antigos (`empresas`, `regras_tributarias`, `simulaçoes`).
  - Configurado `sys.path` e `INSTALLED_APPS` no `settings.py`.
- **Tests:** `python manage.py check` executado com sucesso.

---
— River, removendo obstáculos 🌊
