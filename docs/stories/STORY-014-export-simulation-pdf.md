# STORY-014: Exportação de Simulação para PDF

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Implementar a funcionalidade de exportação dos resultados de uma simulação específica para o formato PDF. Isso permitirá que o usuário faça o download de um relatório formatado contendo o comparativo entre a carga tributária atual e a pós-reforma.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. [x] Criar um endpoint `GET /api/simulation/{id}/export/`.
2. [x] O endpoint deve gerar um arquivo PDF em tempo real baseado no ID do `SimulationLog`.
3. [x] O PDF deve conter:
    - Cabeçalho com o nome "Relatório de Impacto Tributário".
    - Resumo dos dados de entrada (Faturamento, Setor, Regime).
    - Tabela comparativa clara: Carga Atual vs. Carga Reforma.
    - O Delta (Diferença em R$ e %).
    - A classificação do impacto e as sugestões geradas.
4. [x] O layout deve ser limpo e profissional (usar `reportlab` ou biblioteca similar).
5. [x] Garantir que todos os textos e rótulos no PDF estejam em PT-BR.
6. [x] O endpoint deve retornar o PDF com o cabeçalho `Content-Disposition: attachment; filename=simulacao_{id}.pdf`.
7. [x] Criar testes unitários validando a geração do arquivo (status 200 e tipo de conteúdo PDF).

## Lista de Arquivos
- `apps/simulation/services/pdf_generator.py`
- `apps/simulation/views.py`
- `apps/simulation/urls.py`
- `apps/simulation/tests.py`
- `requirements.txt`

## Tarefas
- [x] Adicionar `reportlab` ao `requirements.txt`.
- [x] Criar o serviço `PDFGenerator` para montar o layout do documento com `reportlab.platypus`.
- [x] Implementar a `SimulationExportPDFView` utilizando `FileResponse`.
- [x] Registrar a rota em `apps/simulation/urls.py`.
- [x] Escrever testes garantindo o download do arquivo e o `Content-Type` correto.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Integração da biblioteca `reportlab` para construção de tabelas e parágrafos.
- Implementação de lógica de cores dinâmica no PDF (Vermelho para impacto negativo, Verde para positivo).
- Formatação manual de valores monetários no padrão brasileiro (R$ 0.000,00) via strings de formatação.
- Ajuste nos testes para consumir `streaming_content` em respostas do tipo `FileResponse`.
- Verificação de 15 testes com sucesso.

### Completion Notes
- O relatório gerado é visualmente limpo e contém todas as informações críticas da simulação.
- O uso de `BytesIO` garante que nenhum arquivo temporário seja deixado no servidor.

### Change Log
- Criado `PDFGenerator` em `services/`.
- Adicionada `SimulationExportPDFView`.
- Atualizado `urls.py` e `tests.py`.
- Adicionado `reportlab` às dependências.

## QA Results
- **Gate Decision:** PASS ✅
- **Review Summary:**
  - **Eficiência:** Geração de PDF via stream (`BytesIO`) otimizada para baixo consumo de memória.
  - **Conformidade:** Relatório gerado contém todos os dados de entrada, comparativo financeiro e sugestões solicitados.
  - **Localização:** Formatação numérica e monetária rigorosamente dentro dos padrões brasileiros (PT-BR).
  - **Robustez:** Tratamento de erros via `get_object_or_404` e validação de download via testes de integração.
- **Recommendations:** Para escala futura, se o layout do PDF se tornar muito complexo, considerar a migração para templates HTML renderizados (ex: `django-weasyprint`).

## 🤖 CodeRabbit Integration
### Story Type Analysis
- **Primary Type:** API
- **Complexity:** Medium
- **Secondary Types:** Integration (PDF Library)

### Specialized Agents
- **Primary Agent:** @dev
- **Secondary Agents:** @qa

### Quality Gates
- **Pre-Commit:** @dev (Linting, Unit Tests)
- **Pre-PR:** @github-devops

### Self-Healing Configuration
- **Mode:** light
- **Iterations:** 2
- **Max Time:** 15 min
- **Severity:** CRITICAL only

### Focus Areas
- Manuseio correto de streams de arquivos (evitar vazamento de memória).
- Precisão na formatação de valores monetários no PDF.
- Codificação de caracteres (UTF-8) para garantir acentuação correta em PT-BR.

---
— River, removendo obstáculos 🌊
