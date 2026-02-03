# STORY-003: Motor de Simulação Tributária (Core)

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar o motor de cálculo central do simulador. Esta story foca na lógica de comparação entre a carga tributária atual (Simples Nacional ou Lucro Presumido) e a nova carga proposta pela reforma (IBS/CBS), além de expor o endpoint principal de simulação.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. Implementar a camada de serviço `TaxCalculator` em `apps/simulation/services/calculator.py`.
2. O motor deve calcular a carga tributária atual com base no regime (regras fixas simplificadas):
   - **Simples Nacional:** Alíquota média fixa baseada no faturamento.
   - **Lucro Presumido:** PIS/COFINS/ISS/IRPJ/CSLL (alíquotas fixas padrão por setor).
3. O motor deve calcular a carga pós-reforma:
   - Alíquota única estimada de IBS/CBS (ex: 26.5%) aplicada sobre o valor adicionado (faturamento - custos permitidos).
4. Endpoint `POST /api/v1/simulate/` deve aceitar dados financeiros e retornar o comparativo.
5. Todas as mensagens de resposta, nomes de campos no JSON de saída (labels) e validações devem estar em Português (PT-BR).
6. Testes unitários devem cobrir pelo menos 3 cenários de cálculo (1 para Simples, 1 para Lucro Presumido, 1 para Reforma).

## Lista de Arquivos
- `apps/simulation/services/calculator.py`
- `apps/simulation/services/analyzer.py`
- `apps/simulation/serializers.py`
- `apps/simulation/views.py`
- `apps/simulation/urls.py`
- `config/urls.py` (atualização)

## Tarefas
- [x] Criar `apps/simulation/services/calculator.py` com as fórmulas de cálculo hardcoded.
- [x] Criar `apps/simulation/services/analyzer.py` para calcular o delta (R$ e %) e classificação inicial.
- [x] Implementar `SimulationSerializer` para validar o input financeiro (faturamento, custos, folha).
- [x] Criar a view `SimulationView` (APIView ou ViewSet) para processar a requisição.
- [x] Configurar roteamento em `apps/simulation/urls.py` e incluí-lo no `config/urls.py`.
- [x] Escrever testes unitários para a lógica do `TaxCalculator`.
- [x] Validar se todos os outputs da API estão em PT-BR.

## Dev Agent Record
### Agent Model Used
- Model: Gemini 2.0 Flash

### Debug Log
- Verificação de arquivos existentes: `calculator.py`, `analyzer.py`, `views.py`, `serializers.py`, `urls.py`.
- Execução de testes: `python manage.py test simulation` -> 4 testes passaram.
- Validação de idioma: Labels e mensagens confirmadas em PT-BR.

### Completion Notes
- A lógica de cálculo utiliza alíquotas fixas conforme solicitado.
- O endpoint `POST /api/v1/simulate/` está funcional e integrado ao roteamento global.
- Testes cobrem cenários de Simples Nacional, Lucro Presumido e Reforma.

### Change Log
- Atualização do status da story para "Completed".
- Marcação de todas as tarefas como concluídas.
- Adição deste registro de desenvolvimento.

---
— Dex, sempre construindo 🔨

## Qualidade (CodeRabbit)
- Foco em: Precisão dos cálculos matemáticos e clareza das mensagens de feedback em PT-BR.

---
— River, removendo obstáculos 🌊
