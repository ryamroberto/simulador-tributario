# Instruções Docker - Simulador Tributário

Este projeto está configurado para rodar utilizando Docker e Docker Compose para garantir consistência entre ambientes de desenvolvimento.

## Pré-requisitos

*   Docker instalado
*   Docker Compose instalado

## Como Rodar

1.  **Configurar o ambiente:**
    Certifique-se de que o arquivo `.env` existe na raiz do projeto (foi criado automaticamente a partir do `.env.example`).

2.  **Subir os containers:**
    No terminal, execute:
    ```bash
    docker-compose up --build
    ```

3.  **Acessar a aplicação:**
    A API estará disponível em `http://localhost:8000`.
    A documentação Swagger em `http://localhost:8000/api/schema/swagger-ui/`.

## Comandos Úteis

*   **Rodar em background:** `docker-compose up -d`
*   **Parar containers:** `docker-compose down`
*   **Ver logs:** `docker-compose logs -f`
*   **Rodar migrações dentro do docker:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```
*   **Criar superusuário:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
*   **Rodar testes:**
    ```bash
    docker-compose exec web python manage.py test
    ```

## Notas sobre Persistência

O banco de dados SQLite (`db.sqlite3`) está mapeado via volume, garantindo que os dados não sejam perdidos ao reiniciar os containers.
