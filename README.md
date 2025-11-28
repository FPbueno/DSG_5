# WorcaFlow - Plataforma de Solicitação de Serviços

[![CI - Backend Tests](https://github.com/USER/REPO/workflows/CI%20-%20Backend%20Tests/badge.svg)](https://github.com/USER/REPO/actions)
[![Coverage](https://codecov.io/gh/USER/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USER/REPO)

Sistema completo de marketplace de serviços residenciais conectando clientes a prestadores, com Machine Learning para previsão de preços e categorias. Desenvolvido com FastAPI (backend), Supabase/PostgreSQL (banco) e Flutter (frontend).

## 🏆 Funcionalidades Implementadas

- 🔐 **Autenticação JWT** com bcrypt para senhas
- 🗄️ **Banco Supabase/PostgreSQL** para dados de usuários
- 🛡️ **Criptografia de dados** sensíveis
- 📱 **App Flutter** multiplataforma (Android, iOS, Web)
- 🤖 **Modelos ML** treinados para previsão de preços
- 🌐 **API REST** completa com FastAPI
- ⭐ **Sistema de avaliações** para prestadores

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐    SQL    ┌─────────────┐
│   Frontend      │◄──────────────►│   Backend       │◄─────────►│ Supabase    │
│   (Flutter)     │                 │   (FastAPI)     │            │ PostgreSQL  │
│                 │                 │                 │            │             │
│ • Mobile App    │                 │ • REST API      │            │ • Usuários  │
│ • Web App       │                 │ • Auth/JWT      │            │ • Solicit.  │
│ • Desktop App   │                 │ • ML Models     │            │ • Orçam.    │
│ • Dark Theme    │                 │ • Supabase      │            │ • Aval.     │
└─────────────────┘                 └─────────────────┘            └─────────────┘
```

## 📁 Estrutura do Projeto

```
ABP/
├── backend/                    # API FastAPI + Supabase
│   ├── api/v1/                # Versão 1 da API
│   │   ├── core/              # Configurações (DB, Auth, Security)
│   │   ├── models/            # Modelos ORM (SQLAlchemy)
│   │   ├── routes/            # Endpoints REST (11 rotas)
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── services/          # Lógica de negócio + ML + Supabase
│   ├── models/                # Modelos ML treinados (.pkl)
│   ├── main.py                # Servidor principal
│   ├── setup_db.py            # Inicialização do banco
│   └── requirements.txt       # Dependências Python
├── frontend/                  # App Flutter Multiplataforma
│   ├── lib/                   # Código fonte Dart
│   │   ├── screens/           # Telas (Cliente/Prestador/Shared)
│   │   │   ├── cliente/       # 7 telas para clientes
│   │   │   ├── prestador/     # 7 telas para prestadores
│   │   │   └── shared/        # Telas compartilhadas
│   │   ├── models/            # Modelos de dados
│   │   ├── services/          # Serviços de API
│   │   ├── widgets/           # Componentes reutilizáveis
│   │   ├── constants/         # Constantes e temas
│   │   └── utils/             # Utilitários
│   ├── assets/                # Recursos (imagens, fontes)
│   └── pubspec.yaml           # Dependências Flutter
├── Trello_Cards_ABP.md        # Backlog completo do projeto
├── create_github_issues.py    # Automação de issues GitHub
└── README.md                  # Este arquivo
```

## 🚀 Como Rodar o Projeto Completo

### 1. Backend (API FastAPI + Supabase)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**URL**: `http://localhost:8000`
**Docs**: `http://localhost:8000/docs`
**Banco**: Supabase PostgreSQL (configurado)

### 2. Frontend (App Flutter)

```bash
cd frontend
flutter pub get
flutter run -d chrome --web-port 8080
```

**Mobile**: `flutter run` (Android/iOS)
**Web**: `flutter run -d chrome`

## 🔧 Como Funciona o Backend

### **Arquitetura FastAPI + Supabase**

O backend é uma API REST construída com FastAPI e Supabase:

- **📊 Banco Supabase/PostgreSQL**: Armazena usuários, solicitações, orçamentos e avaliações
- **🤖 ML Integrado**: Modelos treinados para previsão de categoria e preço de serviços
- **🔒 Autenticação JWT**: Sistema de login com bcrypt para senhas
- **📡 API REST**: 11 endpoints completos com validação Pydantic
- **⭐ Avaliações**: Sistema de rating para prestadores
- **☁️ Supabase**: Integração completa com serviços em nuvem

### **Fluxo de Dados**

1. **Recebe requisição** do frontend via HTTP/REST
2. **Valida dados** usando schemas Pydantic
3. **Processa** com lógica de negócio e ML
4. **Persiste no Supabase** via SQLAlchemy ORM
5. **Retorna resposta** JSON padronizada

## 📱 Como Funciona o Frontend

### **Arquitetura Flutter**

O frontend é um app multiplataforma construído com Flutter:

- **🎨 UI Dark Theme**: Interface moderna com tema escuro
- **📡 Comunicação HTTP**: Requisições REST para o backend
- **👥 Dois Perfis**: Cliente e Prestador com telas específicas (7 telas cada)
- **🔄 Navegação por Tabs**: Sistema de navegação intuitivo
- **📱 Modais Interativos**: Detalhes e ações em modais
- **📱 Multiplataforma**: Android, iOS, Web, Desktop
- **🎯 Provider State Management**: Gerenciamento de estado

### **Telas Cliente (7 telas)**

- **🏠 Home Cliente**: Lista de solicitações ativas + criar nova
- **📋 Detalhes Orçamento**: Visualizar e aceitar orçamentos recebidos
- **📝 Detalhes Solicitação**: Ver detalhes da solicitação
- **📜 Histórico Cliente**: Ver histórico completo
- **⚙️ Configurações Cliente**: Perfil e preferências
- **🔐 Login/Registro**: Autenticação de usuários
- **👤 Tipo Usuário**: Seleção de perfil (Cliente/Prestador)

### **Telas Prestador (7 telas)**

- **🏠 Home Prestador**: Solicitações disponíveis + enviar orçamentos
- **💼 Detalhes Solicitação Prestador**: Ver detalhes para orçar
- **📝 Criar Solicitação**: Criar nova solicitação
- **📜 Histórico Prestador**: Serviços realizados
- **⚙️ Configurações Prestador**: Perfil e avaliações
- **🔐 Login/Registro**: Autenticação de usuários
- **👤 Tipo Usuário**: Seleção de perfil (Cliente/Prestador)

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
- **Supabase/PostgreSQL**: Banco de dados em nuvem
- **SQLAlchemy**: ORM para Python
- **Scikit-learn**: Machine Learning (Random Forest)
- **Pydantic**: Validação de dados e schemas
- **Bcrypt**: Criptografia de senhas
- **JWT**: Autenticação com tokens
- **CORS**: Configuração de segurança

### Frontend

- **Flutter 3.9+**: Framework multiplataforma
- **Dart 3.9+**: Linguagem de programação
- **Material Design**: Design system moderno
- **HTTP**: Comunicação REST com API
- **Provider**: Gerenciamento de estado
- **Go Router**: Navegação avançada
- **Shared Preferences**: Armazenamento local

## ⚙️ Configuração

### Backend

1. Configure Supabase com as credenciais em `backend/api/v1/core/config.py`
2. Execute `python setup_db.py` para criar as tabelas
3. Modelos ML já estão treinados em `backend/models/`
4. Configure variáveis de ambiente para Supabase

### Frontend

1. Configure a URL da API em `frontend/lib/constants/app_constants.dart`
2. Por padrão, conecta em `http://localhost:8000`
3. Configure assets (imagens, fontes) em `pubspec.yaml`

## 🔗 URLs de Desenvolvimento

- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Frontend Web**: `http://localhost:3000` (quando executado)
- **Frontend Mobile**: Dispositivo móvel conectado

## 🧪 Testes e CI/CD

O projeto segue práticas de **TDD (Test-Driven Development)** e **CI/CD (Continuous Integration/Continuous Deployment)**:

- ✅ **Testes Automatizados**: pytest com cobertura de código
- ✅ **CI/CD**: GitHub Actions executando testes automaticamente
- ✅ **Estrutura Organizada**: Testes unitários, integração e E2E
- ✅ **Documentação**: Guia completo de testes em [`backend/TESTING.md`](backend/TESTING.md)

### CI/CD

Os testes são executados automaticamente via GitHub Actions em:

- Push para branches principais
- Pull Requests

Veja [`.github/workflows/ci.yml`](.github/workflows/ci.yml) para detalhes.

**Plano de Implementação**:

- [`PLANO_TDD_CI_CD.md`](PLANO_TDD_CI_CD.md) - Roteiro detalhado completo
- [`PROGRESSO_TDD_CI_CD.md`](PROGRESSO_TDD_CI_CD.md) - Progresso atual dos 7 dias

## 📚 Documentação Adicional

Para informações detalhadas sobre cada módulo:

- [📖 Backend README](backend/README.md) - Documentação completa da API
- [📱 Frontend README](frontend/README.md) - Documentação completa do app
- [🧪 Guia de Testes](backend/TESTING.md) - Convenções e práticas de teste
- [🚀 Plano TDD/CI/CD](PLANO_TDD_CI_CD.md) - Roteiro de implementação

## 🎥 Vídeos do Projeto

- [📹 Sprint 1 - Apresentação](https://www.youtube.com/watch?v=uDxAFuqi48g) - Vídeo da Sprint 1
- [📹 Sprint 2 - Apresentação](https://www.youtube.com/watch?v=EiAMgibpMMM) - Vídeo da Sprint 2
- [📹 Sprint 3 - Apresentação](https://www.youtube.com/shorts/IQw_s5aWHUE) - Vídeo da Sprint 3
