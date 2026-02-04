# STORY-006: Persistência de Regras Tributárias e Matriz de Sugestões

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Refatorar o motor de simulação para que as alíquotas (Simples Nacional, Lucro Presumido, Reforma) e a matriz de sugestões (por setor e impacto) sejam lidas do banco de dados em vez de estarem fixas no código. Isso permitirá que o sistema seja atualizado via Admin do Django sem novos deploys de código.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Criar modelos `TaxRule` e `SuggestionMatrix` no app `simulation`.
2. [x] O modelo `TaxRule` deve armazenar: tipo de regime (Enum), setor (Enum), UF (opcional) e a alíquota (Decimal).
3. [x] O modelo `SuggestionMatrix` deve armazenar: setor (Enum), classificação de impacto (Positivo/Neutro/Negativo) e o texto da sugestão.
4. [x] Refatorar `TaxCalculator` e `ImpactAnalyzer` para buscar os dados nesses novos modelos.
5. [x] Garantir que o sistema tenha um mecanismo de *fallback* ou erro amigável caso as regras não estejam cadastradas.
6. [x] Registrar os novos modelos no `admin.py` para permitir edição via interface administrativa.
7. [x] Criar uma migração de dados (data migration) ou fixture para popular o banco com as regras atuais já implementadas.

## Lista de Arquivos
- `apps/simulation/models.py`
- `apps/simulation/admin.py`
- `apps/simulation/services/calculator.py`
- `apps/simulation/services/analyzer.py`
- `apps/simulation/migrations/0001_initial.py`
- `apps/simulation/migrations/0002_populate_initial_data.py`

## Tarefas
- [x] Criar o modelo `TaxRule` em `apps/simulation/models.py`.
- [x] Criar o modelo `SuggestionMatrix` em `apps/simulation/models.py`.
- [x] Executar `makemigrations` e `migrate`.
- [x] Registrar os modelos em `apps/simulation/admin.py`.
- [x] Criar fixture `initial_rules.json` com os dados atuais (substituído por Data Migration).
- [x] Refatorar `TaxCalculator.calculate_current_tax` e `calculate_reform_tax` para consultar o banco.
- [x] Refatorar `ImpactAnalyzer.analyze` para buscar sugestões no banco.
- [x] Atualizar testes unitários para garantir que o motor funciona com os dados do banco.

## Dev Agent Record
- **Status:** Completed
- **Changes:**
  - Implementados modelos `TaxRule` e `SuggestionMatrix`.
  - Criada migração de dados para popular alíquotas e sugestões iniciais.
  - Refatorados serviços de cálculo e análise para busca dinâmica no banco de dados.
  - Corrigidos problemas de importação relativa e conflitos de `app_label` no Django.
- **Tests:** `python manage.py test simulation` executado com 8 testes passando.
- **Notes:** O uso de `app_label` explícito nos modelos e imports absolutos resolveu os problemas de conflito detectados nos testes.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Modelagem:** Modelos `TaxRule` e `SuggestionMatrix` implementados corretamente com campos Decimal e Enums.
  - **Migração de Dados:** Dados iniciais populados via `0002_populate_initial_data.py`, garantindo paridade com o MVP.
  - **Resiliência:** Implementado mecanismo de *fallback* no `TaxCalculator` para evitar falhas críticas em caso de banco vazio.
  - **Internacionalização:** 100% em PT-BR (verbose_names, enums e mensagens).
  - **Testes:** 8/8 testes passando. Refatoração validada com sucesso.
- **Recommendations:** Futuramente, considerar o uso de `django-cache` para armazenar as alíquotas em memória e reduzir o I/O de banco por simulação.

## Qualidade (CodeRabbit)
- Foco em: Integridade referencial, performance de consultas ao banco e clareza das mensagens de erro em PT-BR.

---
— River, removendo obstáculos 🌊
