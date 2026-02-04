# Integração Contínua (CI) - Simulador Tributário

Este projeto utiliza o **GitHub Actions** para garantir a qualidade do código e evitar regressões.

## Como funciona

Sempre que um novo código é enviado (**push**) ou um **Pull Request** é aberto para a branch `master` ou `main`, o pipeline de CI é acionado automaticamente.

O pipeline executa as seguintes etapas:

1.  **Configuração do Ambiente:** Prepara um ambiente Linux com Python 3.12.
2.  **Instalação de Dependências:** Instala todas as bibliotecas listadas no `requirements.txt`.
3.  **Linting (Ruff):** Verifica se o código segue os padrões de estilo e se não há erros óbvios (como variáveis não utilizadas ou imports inválidos).
4.  **Testes Automatizados:** Executa todos os testes unitários e de integração do projeto utilizando o comando `python manage.py test`.

## Visualizando Resultados

Você pode visualizar o status de execução do pipeline na aba **Actions** do seu repositório no GitHub.

*   ✅ **Verde:** O código passou em todos os testes e no linting.
*   ❌ **Vermelho:** Houve alguma falha. Clique no workflow para ver os logs e identificar o erro.

## Configuração Local

Para rodar as mesmas verificações localmente antes de enviar o código:

1.  **Instalar ferramentas:**
    ```bash
    pip install ruff
    ```

2.  **Rodar o Linter:**
    ```bash
    ruff check .
    ```

3.  **Rodar os Testes:**
    ```bash
    python manage.py test companies simulation
    ```
