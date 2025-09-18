# Frontend - App Flutter WorcaFlow

## Estrutura do Projeto

```
frontend/
├── lib/
│   ├── constants/
│   │   ├── app_constants.dart     # Constantes da aplicação
│   │   └── app_theme.dart         # Tema e cores
│   ├── models/
│   │   ├── client.dart            # Modelo de Cliente
│   │   ├── quote.dart             # Modelo de Orçamento
│   │   ├── service.dart           # Modelo de Serviço
│   │   └── simple_quote.dart      # Modelo de Orçamento Simples
│   ├── screens/
│   │   ├── analytics_screen.dart  # Tela de Analytics
│   │   ├── history_screen.dart    # Tela de Histórico
│   │   ├── home_screen.dart       # Tela Principal
│   │   ├── simple_home_screen.dart # Tela Principal Simples
│   │   └── ml_settings_screen.dart # Tela de Configurações ML
│   ├── services/
│   │   └── api_service.dart       # Serviço de API
│   ├── utils/
│   │   └── format_utils.dart      # Utilitários de formatação
│   ├── widgets/
│   │   ├── footer_menu.dart       # Menu inferior
│   │   └── logo_widget.dart       # Widget do logo
│   └── main.dart                  # Arquivo principal
├── assets/
│   ├── fonts/                     # Fontes personalizadas
│   ├── icons/                     # Ícones
│   └── images/                    # Imagens
├── pubspec.yaml                   # Dependências Flutter
└── README.md
```

## Como Rodar

### 1. Instalar Flutter

Certifique-se de ter o Flutter instalado: [flutter.dev](https://flutter.dev)

### 2. Instalar Dependências

```bash
cd frontend
flutter pub get
```

### 3. Executar o App

```bash
# Para debug
flutter run

# Para release
flutter run --release
```

### 4. Plataformas Suportadas

- **Android**: `flutter run -d android`
- **iOS**: `flutter run -d ios`
- **Web**: `flutter run -d web`
- **Windows**: `flutter run -d windows`
- **macOS**: `flutter run -d macos`
- **Linux**: `flutter run -d linux`

## Funcionalidades

- **Home**: Criação de orçamentos com Machine Learning
- **Histórico**: Visualização de orçamentos criados
- **Analytics**: Relatórios e estatísticas
- **ML**: Predições inteligentes de serviços
- **Configurações ML**: Gerenciamento de modelos
- **Responsivo**: Interface adaptável

## Tecnologias

- Flutter 3.0+
- Dart 3.0+
- HTTP (requisições API)
- Material Design

## Configuração

O app se conecta automaticamente com o backend em `http://localhost:8000`.

Para alterar a URL da API, edite `lib/services/api_service.dart`:

```dart
static const String baseUrl = 'http://localhost:8000/api/v1';
```
