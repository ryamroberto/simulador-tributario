# Simulador Tributário Simplificado (MVP)

API-first focada na comparação de impacto da reforma tributária (Cenário Atual vs. Pós-Reforma).

## 🚀 Funcionalidades Principais
- **Simulação de Impacto:** Cálculo determinístico baseado em regimes tributários (Simples Nacional, Lucro Presumido).
- **Dashboard de Métricas:** Agregados de simulações por usuário.
- **Exportação Multiformato:** Download de resultados em PDF, CSV (UTF-8 BOM) e Excel (.xlsx).
- **Gestão Administrativa:** Endpoints exclusivos para administradores gerirem regras tributárias e matriz de sugestões.
- **Segurança & Resiliência:** 
  - Autenticação JWT.
  - Propriedade de dados (User Isolation).
  - Rate Limiting (Throttling) para proteção de endpoints sensíveis.

## 🛠️ Tecnologias
- Python 3.10+
- Django 5.x / Django Rest Framework
- OpenPyXL (Excel) / ReportLab (PDF)
- JWT (SimpleJWT)
- Docker & Docker Compose

## 📖 Documentação da API
Acesse a documentação interativa (Swagger) em:
`http://localhost:8000/api/docs/swagger/`

## 🔒 Segurança (Rate Limiting)
Para garantir a estabilidade, aplicamos os seguintes limites:
- **Geral (Usuário):** 1000 requisições/dia.
- **Exportação:** 10 requisições/minuto (Escopo: `export`).

## 🧪 Testes
Execute a suíte completa de testes:
```bash
python manage.py test
```

---
