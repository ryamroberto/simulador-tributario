# STORY-004: Inteligência de Feedback e Refinamento de Sugestões

## Status
- [x] Tasks defined
- [x] Implementation in progress
- [x] Testing
- [x] Completed

## Descrição
Melhorar a camada de resposta da API para fornecer feedbacks qualitativos e sugestões baseadas no perfil da empresa (Setor, Regime e UF). O objetivo é transformar o resultado numérico em insights acionáveis para o usuário.

**REGRA OBRIGATORIO: qualquer texto exibido ao usuario deve estar em portugues (pt-br) se houver ingles, considere um erro.**

## Critérios de Aceite
1. Expandir o `ImpactAnalyzer` para selecionar sugestões de uma matriz de conhecimento (Hardcoded no serviço por enquanto).
2. As sugestões devem variar conforme o **Setor** (ex: Serviços vs. Indústria) e o **Impacto** (Positivo/Negativo).
3. Integrar o campo **UF** na lógica (verificar se há alíquotas de ISS/ICMS específicas que podem ser mencionadas no feedback, mesmo que o cálculo use médias).
4. O campo `mensagem` na resposta da API deve ser mais detalhado (ex: "Seu setor de Serviços pode ser impactado pela nova alíquota de IBS, revise seus contratos de longo prazo.").
5. Garantir que 100% dos textos de feedback estejam em Português (PT-BR).
6. Testes unitários para validar se a sugestão correta é retornada para diferentes combinações de Setor + Impacto.

## Lista de Arquivos
- `apps/simulation/services/analyzer.py` (atualização)
- `apps/simulation/tests.py` (novos testes)
- `apps/simulation/serializers.py` (atualização)
- `apps/simulation/views.py` (atualização)

## Tarefas
- [x] Mapear uma matriz de sugestões mínimas (3 por setor: Serviços, Comércio, Indústria).
- [x] Refatorar o `ImpactAnalyzer.analyze` para aceitar `sector` e `uf` como parâmetros.
- [x] Implementar a lógica de seleção de sugestões dinâmicas.
- [x] Adicionar um campo `detalhes_setoriais` na resposta da API (opcional, para maior clareza).
- [x] Atualizar testes existentes e adicionar novos casos de borda para sugestões.
- [x] Revisão final de termos técnicos para garantir clareza em PT-BR.

## Dev Agent Record
### Agent Model Used
- Gemini 2.0 Flash

### Debug Log
- Refatoração do `ImpactAnalyzer` para incluir matriz de sugestões.
- Correção de erro de indentação no `analyzer.py` que causava `AttributeError`.
- Atualização do `SimulationInputSerializer` para incluir o campo `state` (UF).
- Atualização da `SimulationView` para integrar os novos campos na resposta da API.
- Execução de 8 testes (4 novos) com 100% de sucesso.

### Completion Notes
- As sugestões agora são específicas para os setores de Serviços, Comércio e Indústria.
- O campo `detalhes_setoriais` fornece contexto adicional baseado na UF informada.
- Todos os textos de feedback seguem rigorosamente a regra de idioma PT-BR.

### Change Log
- Criada matriz de sugestões no `ImpactAnalyzer`.
- Adicionado campo `state` ao endpoint de simulação.
- Refinados testes unitários e de integração.
- Status da story atualizado para "Completed".

---
— Dex, sempre construindo 🔨

## QA Results
### Status: PASS ✅

### Auditoria Técnica
- **Cobertura de Requisitos:** Todos os critérios de aceite foram validados. A matriz de sugestões é abrangente e a lógica de seleção por setor/impacto funciona conforme o esperado.
- **Internacionalização:** Rigorosamente seguido. Todas as strings de feedback e labels da API estão em Português (PT-BR).
- **Testes Automatizados:** 8 testes executados com sucesso (`python manage.py test simulation`). Cobertura de cenários positivos, negativos e neutros para todos os setores principais.
- **Qualidade do Código:** Separação clara entre serviços de cálculo e serviços de análise. O uso de `Decimal` garante a precisão necessária para simulações financeiras.

### Recomendações (Advisory)
- **Escalabilidade:** Futuramente, considere mover a matriz de sugestões para o banco de dados caso a equipe de conteúdo precise editá-las sem tocar no código.
- **UF:** O mapeamento manual de UF no serviço atende ao MVP, mas pode ser centralizado no app `core` ou `companies` em próximas iterações.

— Quinn, guardião da qualidade 🛡️

## Qualidade (CodeRabbit)
- Foco em: Redação dos feedbacks (tom profissional e útil) e corretude da lógica de seleção.

---
— River, removendo obstáculos 🌊
