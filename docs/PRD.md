# Documento de Requisitos (PRD) - Simulador Tributário Simplificado

## 1. Visão Geral do Produto
Desenvolvimento de um simulador tributário "API-first" simplificado, focado exclusivamente na comparação de impacto da reforma tributária. O sistema visa oferecer clareza e confiabilidade através de regras fixas e transparentes, sem complexidade excessiva de planejamento fiscal.

## 2. Escopo

### 2.1 Dentro do Escopo
- **Backend:** Django com Django Rest Framework (DRF).
- **Regimes Suportados:** Simples Nacional ou Lucro Presumido (um por vez).
- **Período:** Simulação de período único (ex: mês de referência).
- **Cálculos:** Regras "hardcoded" para cenário Antes vs. Depois da reforma.
- **Saída:** Comparativo financeiro (Absoluto/%) e qualitativo (Positivo/Neutro/Negativo).
- **Sugestões:** Textos estáticos baseados na faixa de impacto.

### 2.2 Fora do Escopo
- Frontend (Interface de Usuário).
- Múltiplos regimes simultâneos ou histórico acumulado.
- Integrações com sistemas governamentais (Receita, Sintegra, etc.).
- Relatórios oficiais contábeis.
- Inteligência Artificial ou personalização avançada.
- Gráficos complexos.

## 3. Funcionalidades Principais

### 3.1 Cadastro de Empresa (Simplificado)
- **Campos Obrigatórios:**
  - Faturamento Mensal.
  - Setor de Atuação.
  - UF (Estado).
  - Regime Tributário Atual (Enum: Simples Nacional, Lucro Presumido).
- **Campos Opcionais:**
  - Número de Funcionários.

### 3.2 Motor de Simulação
- **Entradas (Inputs):**
  - Dados financeiros do período (Faturamento, Custos, Folha de Pagamento opcional).
- **Processamento:**
  - Cálculo da Carga Atual (Regras vigentes fixas).
  - Cálculo da Carga Pós-Reforma (Regras propostas fixas).
  - Cálculo do Delta (Diferença R$ e %).

### 3.3 Apresentação de Resultados
- **Classificação:** Impacto Positivo, Neutro ou Negativo.
- **Feedback:** Explicação textual simples e direta sobre o resultado.
- **Recomendação:** Sugestão genérica estática baseada no resultado (ex: "Considere revisar seus créditos tributários" se impacto negativo).

## 4. Requisitos Técnicos
- **Linguagem/Framework:** Python 3.x, Django 5+, DRF.
- **Estrutura:** Separação clara de responsabilidades (Apps: `core`, `companies`, `simulation`).
- **Testes:** 
  - Testes unitários cobrindo a lógica de cálculo (regras tributárias).
  - Testes de integração simples para os endpoints da API.
- **Documentação:** Código limpo e regras de negócio comentadas/documentadas no próprio código.

## 5. Critérios de Sucesso
- A API deve receber um JSON com dados da empresa e retornar um JSON com a simulação completa.
- O cálculo deve ser determinístico e verificável via testes.
- O código deve estar pronto para evolução futura (extensibilidade básica).
