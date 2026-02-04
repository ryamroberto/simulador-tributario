# STORY-011: Histórico de Simulações e Logs de Auditoria

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar a persistência das simulações realizadas através de um modelo de log. Isso permitirá que o sistema mantenha um histórico de consultas para fins de auditoria, análise de dados agregados e futura exibição para os usuários.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Criar o modelo `SimulationLog` no app `simulation`.
2. [x] O modelo deve armazenar todos os inputs da simulação.
3. [x] O modelo deve armazenar os resultados gerados.
4. [x] O campo `company` deve ser uma chave estrangeira opcional.
5. [x] A gravação do log deve ocorrer automaticamente após uma simulação bem-sucedida.
6. [x] Registrar o modelo no Django Admin.
7. [x] Criar testes unitários e de integração validando a criação do log.

## Lista de Arquivos
- `apps/simulation/models.py`
- `apps/simulation/admin.py`
- `apps/simulation/views.py`
- `apps/simulation/tests.py`
- `apps/simulation/migrations/0003_simulationlog.py`

## Tarefas
- [x] Definir o modelo `SimulationLog` utilizando o `TimeStampedModel` como base.
- [x] Gerar e aplicar a migração de banco de dados.
- [x] Refatorar a `SimulationView` para salvar o log após o processamento bem-sucedido.
- [x] Configurar o `admin.py` para exibir os logs com filtros por regime, setor e classificação de impacto.
- [x] Escrever testes garantindo que, a cada simulação, um novo registro de log é criado no banco.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Criação do modelo `SimulationLog` com campos Decimal para precisão financeira.
- Implementação de `SimulationLog.objects.create` dentro do método `post` da `SimulationView`.
- Configuração de `SimulationLogAdmin` com filtros por data e classificação.
- Correção de `NameError` no `admin.py` devido a import esquecido.
- Verificação de 13 testes com sucesso.

### Completion Notes
- O sistema agora mantém um histórico completo de todas as simulações executadas via API.
- O campo `company_id` é capturado se fornecido no input da simulação.

### Change Log
- Adicionado modelo `SimulationLog`.
- Atualizada View de Simulação para persistência de dados.
- Registrado novo modelo no Admin.
- Adicionado teste de integridade de log.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Auditabilidade:** Implementado modelo `SimulationLog` que captura o contexto completo das simulações (input + output).
  - **Precisão:** Uso de `DecimalField` em todos os campos monetários assegura a integridade financeira dos logs.
  - **Resiliência:** Relacionamento opcional com `Company` evita perda de dados históricos em caso de deleção cadastral.
  - **Internacionalização:** 100% em PT-BR (verbose_names e admin).
  - **Testes:** Validada a criação automática de logs via teste de integração na `SimulationView`.
- **Recommendations:** Para escala massiva (milhares de logs por segundo), considerar a escrita assíncrona dos logs (ex: via Celery ou Background Tasks) para não impactar o tempo de resposta da API principal.

## Qualidade (CodeRabbit)
- Foco em: Performance da escrita de log (non-blocking se possível) e integridade dos dados financeiros persistidos (uso de Decimal).

---
— River, removendo obstáculos 🌊
