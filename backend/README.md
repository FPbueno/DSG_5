# Backend - API de Orçamentos Residenciais

## Estrutura do Projeto

```
backend/
├── api/
│   └── v1/
│       ├── core/
│       │   └── config.py          # Configurações da aplicação
│       ├── models/
│       │   ├── client.py          # Modelos de dados - Clientes
│       │   ├── quote.py           # Modelos de dados - Orçamentos
│       │   └── service.py         # Modelos de dados - Serviços
│       ├── routes/
│       │   ├── ml.py              # Rotas de Machine Learning
│       │   ├── analytics.py       # Rotas de Analytics
│       │   ├── clients.py         # Rotas de Clientes
│       │   ├── quotes.py          # Rotas de Orçamentos
│       │   └── services.py        # Rotas de Serviços
│       └── services/
│           ├── ml_service.py      # Serviço de Machine Learning
│           └── excel_service.py   # Serviço de Excel
├── main.py                        # Arquivo principal
├── requirements.txt               # Dependências Python
├── quotes_data.xlsx              # Banco de dados Excel
└── .env                          # Variáveis de ambiente
```

## Como Rodar

### 1. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Executar o Servidor

```bash
python main.py
```

O servidor estará disponível em: `http://localhost:8000`

### 3. Documentação da API

Acesse: `http://localhost:8000/docs` para ver a documentação interativa da API.

## Funcionalidades

- **Clientes**: CRUD completo de clientes
- **Serviços**: CRUD completo de serviços
- **Orçamentos**: CRUD completo de orçamentos
- **Machine Learning**: Predição inteligente baseada em dados históricos
- **Analytics**: Relatórios e estatísticas
- **Excel**: Banco de dados em arquivo Excel

## Tecnologias

- FastAPI
- Python 3.8+
- Pandas + OpenPyXL
- Scikit-learn (Machine Learning)
- Pydantic
