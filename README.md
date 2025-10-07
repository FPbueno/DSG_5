# WorcaFlow - Plataforma de Solicitação de Serviços

Sistema completo de marketplace de serviços residenciais conectando clientes a prestadores, com Machine Learning para previsão de preços e categorias. Desenvolvido com FastAPI (backend), MySQL (banco) e Flutter (frontend).

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐    SQL    ┌─────────────┐
│   Frontend      │◄──────────────►│   Backend       │◄─────────►│   MySQL     │
│   (Flutter)     │                 │   (FastAPI)     │            │             │
│                 │                 │                 │            │ • Usuários  │
│ • Mobile App    │                 │ • REST API      │            │ • Solicit.  │
│ • Web App       │                 │ • Auth/JWT      │            │ • Orçam.    │
│ • Desktop App   │                 │ • ML Models     │            │ • Aval.     │
└─────────────────┘                 └─────────────────┘            └─────────────┘
```

## 📁 Estrutura do Projeto

```
ABP/
├── backend/                    # API FastAPI + MySQL
│   ├── api/v1/                # Versão 1 da API
│   │   ├── core/              # Configurações (DB, Auth)
│   │   ├── models/            # Modelos ORM (SQLAlchemy)
│   │   ├── routes/            # Endpoints REST
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── services/          # Lógica de negócio + ML
│   ├── models/                # Modelos ML treinados (.pkl)
│   ├── main.py                # Servidor principal
│   ├── setup_db.py            # Inicialização do banco
│   └── requirements.txt       # Dependências Python
├── frontend/                  # App Flutter
│   ├── lib/                   # Código fonte Dart
│   │   ├── screens/           # Telas (Cliente/Prestador)
│   │   ├── models/            # Modelos de dados
│   │   ├── services/          # Serviços de API
│   │   ├── widgets/           # Componentes reutilizáveis
│   │   ├── constants/         # Constantes e temas
│   │   └── utils/             # Utilitários
│   ├── assets/                # Recursos (imagens, fontes)
│   └── pubspec.yaml           # Dependências Flutter
└── README.md                  # Este arquivo
```

## 🚀 Como Rodar o Projeto Completo

### 1. Backend (API FastAPI)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**URL**: `http://localhost:8000`
**Docs**: `http://localhost:8000/docs`

### 2. Frontend (App Flutter)

```bash
cd frontend
flutter pub get
flutter run -d chrome --web-port 8080
```

## 🔧 Como Funciona o Backend

### **Arquitetura FastAPI + MySQL**

O backend é uma API REST construída com FastAPI e MySQL:

- **📊 Banco MySQL**: Armazena usuários, solicitações, orçamentos e avaliações
- **🤖 ML Integrado**: Modelos para previsão de categoria e preço de serviços
- **🔒 Autenticação**: Sistema de login com bcrypt para senhas
- **📡 API REST**: Endpoints completos com validação Pydantic
- **⭐ Avaliações**: Sistema de rating para prestadores

### **Endpoints Principais**

```
# Usuários
POST   /api/v1/usuarios/registro       # Registrar usuário
POST   /api/v1/usuarios/login          # Login
GET    /api/v1/usuarios/{id}           # Buscar usuário

# Solicitações (Cliente)
POST   /api/v1/solicitacoes/           # Criar solicitação
GET    /api/v1/solicitacoes/minhas     # Minhas solicitações
GET    /api/v1/solicitacoes/disponiveis # Solicitações disponíveis

# Orçamentos (Prestador)
POST   /api/v1/orcamentos/             # Enviar orçamento
GET    /api/v1/orcamentos/solicitacao/{id} # Orçamentos de solicitação
PUT    /api/v1/orcamentos/{id}/aceitar # Aceitar orçamento
PUT    /api/v1/orcamentos/{id}/realizado # Marcar como realizado

# Avaliações
POST   /api/v1/avaliacoes/             # Avaliar serviço
GET    /api/v1/avaliacoes/prestador/{id} # Avaliações do prestador

# Machine Learning
POST   /api/v1/ml/predict-category     # Prever categoria
POST   /api/v1/ml/predict-price        # Prever preço
```

### **Fluxo de Dados**

1. **Recebe requisição** do frontend via HTTP/REST
2. **Valida dados** usando schemas Pydantic
3. **Processa** com lógica de negócio e ML
4. **Persiste no MySQL** via SQLAlchemy ORM
5. **Retorna resposta** JSON padronizada

## 📱 Como Funciona o Frontend

### **Arquitetura Flutter**

O frontend é um app multiplataforma construído com Flutter:

- **🎨 UI Dark Theme**: Interface moderna com tema escuro
- **📡 Comunicação HTTP**: Requisições REST para o backend
- **👥 Dois Perfis**: Cliente e Prestador com telas específicas
- **🔄 Navegação por Tabs**: Sistema de navegação intuitivo
- **📱 Modais Interativos**: Detalhes e ações em modais

### **Telas Cliente**

- **🏠 Home**: Lista de solicitações ativas + criar nova
- **📋 Orçamentos**: Visualizar e aceitar orçamentos recebidos (modal)
- **⭐ Avaliações**: Avaliar serviços realizados (modal)
- **📜 Histórico**: Ver histórico completo (somente leitura)
- **⚙️ Configurações**: Perfil e preferências

### **Telas Prestador**

- **🏠 Home**: Solicitações disponíveis + enviar orçamentos
- **💼 Meus Orçamentos**: Orçamentos enviados e status
- **📜 Histórico**: Serviços realizados
- **⚙️ Configurações**: Perfil e avaliações

### **Fluxo de Dados**

1. **Login/Registro** com autenticação
2. **Navegação por tipo** de usuário
3. **Requisições REST** para backend
4. **Atualização em tempo real** com pull-to-refresh

## ✨ Funcionalidades Principais

### Para Clientes

- 📝 **Criar Solicitações**: Descrever serviço necessário
- 💰 **Receber Orçamentos**: Múltiplos prestadores respondem
- ✅ **Aceitar Orçamentos**: Escolher melhor proposta
- ⭐ **Avaliar Serviços**: Dar feedback após conclusão
- 📜 **Histórico Completo**: Ver todas solicitações

### Para Prestadores

- 👀 **Ver Solicitações**: Buscar novos trabalhos
- 💼 **Enviar Orçamentos**: Propor valor e prazo
- 📊 **Acompanhar Status**: Ver orçamentos aceitos
- 🏆 **Receber Avaliações**: Construir reputação

### Tecnologia

- 🤖 **ML para Preços**: Sugestão inteligente de valores
- 🔒 **Autenticação Segura**: Login com bcrypt
- 📱 **Multiplataforma**: Android, iOS, Web, Desktop
- 💾 **MySQL**: Banco de dados robusto
- 🎨 **UI Dark**: Interface moderna e intuitiva

## 🛠️ Tecnologias

### Backend

- **FastAPI**: Framework web moderno e rápido
- **Python 3.8+**: Linguagem de programação
- **MySQL**: Banco de dados relacional
- **SQLAlchemy**: ORM para Python
- **Scikit-learn**: Machine Learning (Random Forest)
- **Pydantic**: Validação de dados e schemas
- **Bcrypt**: Criptografia de senhas
- **CORS**: Configuração de segurança

### Frontend

- **Flutter 3.0+**: Framework multiplataforma
- **Dart 3.0+**: Linguagem de programação
- **Material Design**: Design system moderno
- **HTTP**: Comunicação REST com API

## ⚙️ Configuração

### Backend

1. Configure MySQL com as credenciais em `backend/api/v1/core/config.py`
2. Execute `python setup_db.py` para criar as tabelas
3. Modelos ML já estão treinados em `backend/models/`

### Frontend

1. Configure a URL da API em `frontend/lib/constants/app_constants.dart`
2. Por padrão, conecta em `http://localhost:8000`

## 🔗 URLs de Desenvolvimento

- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Frontend Web**: `http://localhost:3000` (quando executado)
- **Frontend Mobile**: Dispositivo móvel conectado

## 📚 Documentação Adicional

Para informações detalhadas sobre cada módulo:

- [📖 Backend README](backend/README.md) - Documentação completa da API
- [📱 Frontend README](frontend/README.md) - Documentação completa do app
