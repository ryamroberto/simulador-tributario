# STORY-008: Validações de Negócio e Integridade de Dados

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Aprimorar a camada de validação do sistema para garantir a integridade dos dados cadastrais e financeiros. Isso inclui a implementação de um validador de CNPJ real, garantia de valores financeiros coerentes e tratamento de erros customizado.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Adicionar o campo `cnpj` ao modelo `Company` (app `companies`).
2. [x] Implementar um validador de CNPJ (algoritmo de dígitos verificadores) para garantir que apenas números válidos sejam salvos.
3. [x] Garantir que o campo `cnpj` seja único no banco de dados.
4. [x] Refinar os serializers de simulação para garantir que:
   - `monthly_revenue` (faturamento) seja sempre positivo.
   - `costs` (custos) não excedam o faturamento.
   - `costs` não sejam negativos.
5. [x] Centralizar as mensagens de erro de validação, garantindo tom profissional e 100% em PT-BR.
6. [x] Criar testes unitários específicos para o validador de CNPJ e para as novas regras de negócio financeiras.

## Lista de Arquivos
- `apps/companies/models.py`
- `apps/companies/serializers.py`
- `apps/simulation/serializers.py`
- `apps/core/validators.py`
- `apps/companies/tests.py`
- `apps/simulation/tests.py`
- `apps/companies/migrations/0002_company_cnpj.py`
- `apps/companies/migrations/0003_alter_company_cnpj.py`

## Tarefas
- [x] Criar `apps/core/validators.py` com a função `validate_cnpj`.
- [x] Adicionar campo `cnpj` no modelo `Company` e gerar migração.
- [x] Atualizar `CompanySerializer` para incluir e validar o CNPJ.
- [x] Adicionar validação cruzada no `SimulationInputSerializer` (costs <= monthly_revenue).
- [x] Implementar tratamento de erro amigável para campos financeiros.
- [x] Escrever bateria de testes para CNPJ (casos válidos e inválidos).
- [x] Escrever testes para as novas restrições financeiras da simulação.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Implementação do algoritmo de validação de CNPJ em `core/validators.py`.
- Adição do campo `cnpj` no modelo `Company` com migrations.
- Refatoração dos serializers para incluir validações de negócio financeiras (faturamento > 0, custos <= faturamento).
- Correção de erro em teste unitário onde o CNPJ fictício era matematicamente inválido.
- Execução de 13 testes com 100% de sucesso.

### Completion Notes
- O simulador agora impede a criação de empresas ou simulações com dados fiscais ou financeiros inconsistentes.
- Mensagens de erro foram refinadas para serem claras e informativas em PT-BR.

### Change Log
- Criado validador de CNPJ.
- Adicionado campo CNPJ único ao modelo de Empresa.
- Refinadas regras de validação nos serializers de Companies e Simulation.
- Atualizada suíte de testes unitários.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Integridade Cadastral:** Validador de CNPJ robusto e campo `unique` asseguram a qualidade dos dados da empresa.
  - **Lógica de Negócio:** Validações financeiras (revenue > 0 e costs <= revenue) implementadas e testadas.
  - **Internacionalização:** Mensagens de erro claras e profissionais em PT-BR.
  - **Rastreabilidade:** Requisitos do PRD mapeados para testes unitários automatizados.
- **Recommendations:** Nenhuma para esta fase. O sistema está pronto para evoluir para a dockerização ou cache.

## Qualidade (CodeRabbit)
- Foco em: Eficiência do algoritmo de validação de CNPJ e clareza das mensagens de erro para o usuário final.

---
— River, removendo obstáculos 🌊
