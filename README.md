# WorcaFlow - Sistema de Orçamentos Residenciais

Sistema completo para gerenciamento de orçamentos residenciais com Machine Learning, desenvolvido com FastAPI (backend) e Flutter (frontend).

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Frontend      │◄──────────────►│   Backend       │
│   (Flutter)     │                 │   (FastAPI)     │
│                 │                 │                 │
│ • Mobile App    │                 │ • REST API      │
│ • Web App       │                 │ • ML Local      │
│ • Desktop App   │                 │ • Excel DB      │
└─────────────────┘                 └─────────────────┘
```

## 📁 Estrutura do Projeto

```
ABP/
├── backend/                    # API FastAPI
│   ├── api/v1/                # Versão 1 da API
│   │   ├── core/              # Configurações
│   │   ├── models/            # Modelos de dados
│   │   ├── routes/            # Endpoints da API
│   │   └── services/          # Lógica de negócio
│   ├── main.py                # Servidor principal
│   ├── requirements.txt       # Dependências Python
│   └── README.md              # Documentação do Backend
├── frontend/                  # App Flutter
│   ├── lib/                   # Código fonte Dart
│   │   ├── screens/           # Telas da aplicação
│   │   ├── services/          # Serviços de API
│   │   ├── models/            # Modelos de dados
│   │   └── widgets/           # Componentes reutilizáveis
│   ├── assets/                # Recursos (imagens, fontes)
│   ├── pubspec.yaml           # Dependências Flutter
│   └── README.md              # Documentação do Frontend
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

### **Arquitetura FastAPI**

O backend é uma API REST construída com FastAPI que funciona como servidor de dados:

- **📊 Banco de Dados**: Usa Excel como banco de dados (arquivo `quotes_data.xlsx`)
- **🤖 ML Integrado**: Machine Learning local para gerar serviços inteligentes
- **📡 API REST**: Endpoints para CRUD de clientes, serviços e orçamentos
- **📈 Analytics**: Gera relatórios e estatísticas dos dados

### **Endpoints Principais**

```
GET    /api/v1/clients          # Listar clientes
POST   /api/v1/clients          # Criar cliente
GET    /api/v1/services         # Listar serviços
POST   /api/v1/services         # Criar serviço
GET    /api/v1/quotes           # Listar orçamentos
POST   /api/v1/quotes           # Criar orçamento
PUT    /api/v1/quotes/{id}      # Atualizar orçamento
DELETE /api/v1/quotes/{id}      # Excluir orçamento
POST   /api/v1/ml/smart-create  # Criar serviço com ML
GET    /api/v1/analytics/*      # Relatórios e estatísticas
```

### **Fluxo de Dados**

1. **Recebe requisição** do frontend via HTTP
2. **Processa dados** usando serviços Python
3. **Salva no Excel** usando Pandas + OpenPyXL
4. **Retorna resposta** em formato JSON

## 📱 Como Funciona o Frontend

### **Arquitetura Flutter**

O frontend é um app multiplataforma construído com Flutter:

- **🎨 UI Responsiva**: Interface adaptável para mobile, web e desktop
- **📡 Comunicação**: Faz requisições HTTP para o backend
- **💾 Estado Local**: Gerencia estado da aplicação
- **🔄 Navegação**: Sistema de navegação entre telas

### **Telas Principais**

- **🏠 Home**: Criação de orçamentos com IA
- **📋 Histórico**: Lista e edição de orçamentos
- **📊 Analytics**: Relatórios e estatísticas

### **Fluxo de Dados**

1. **Usuário interage** com a interface
2. **App faz requisição** para o backend
3. **Recebe dados** em formato JSON
4. **Atualiza interface** com os dados recebidos

## ✨ Funcionalidades Principais

- 🤖 **Machine Learning**: Predições inteligentes baseadas em dados históricos
- 📊 **Analytics**: Relatórios e estatísticas em tempo real
- 📱 **Multiplataforma**: Android, iOS, Web, Desktop
- 💾 **Excel como DB**: Banco de dados em planilha
- 🎨 **UI Moderna**: Interface responsiva e intuitiva
- ✏️ **CRUD Completo**: Criar, ler, atualizar e excluir dados
- 🔄 **Tempo Real**: Atualizações automáticas

## 🛠️ Tecnologias

### Backend

- **FastAPI**: Framework web moderno e rápido
- **Python 3.8+**: Linguagem de programação
- **Scikit-learn**: Machine Learning
- **Pandas + OpenPyXL**: Manipulação de Excel
- **Pydantic**: Validação de dados

### Frontend

- **Flutter 3.0+**: Framework multiplataforma
- **Dart 3.0+**: Linguagem de programação
- **Material Design**: Design system do Google
- **HTTP**: Comunicação com API

## ⚙️ Configuração

1. **Backend**: Não requer configuração adicional
2. **Frontend**: Conecta automaticamente com o backend local

## 🔗 URLs de Desenvolvimento

- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Frontend Web**: `http://localhost:3000` (quando executado)
- **Frontend Mobile**: Dispositivo móvel conectado

## 📚 Documentação Adicional

Para informações detalhadas sobre cada módulo:

- [📖 Backend README](backend/README.md) - Documentação completa da API
- [📱 Frontend README](frontend/README.md) - Documentação completa do app
