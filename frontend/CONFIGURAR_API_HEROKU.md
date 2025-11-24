# Configurar API do Heroku no APK

Antes de gerar o APK para distribuir no Google Drive, você precisa alterar as URLs da API de `localhost` para a URL do seu backend no Heroku.

## URL do Heroku

Após fazer o deploy no Heroku, você terá uma URL como:

```
https://nome-da-sua-app.herokuapp.com
```

A URL completa da API será:

```
https://nome-da-sua-app.herokuapp.com/api/v1
```

## Arquivos que Precisam ser Alterados

Você precisa alterar a URL da API nos seguintes arquivos:

### 1. `frontend/lib/constants/app_constants.dart`

**Linha 27** - Altere de:

```dart
static const String apiBaseUrl = 'http://localhost:8000/api/v1';
```

Para:

```dart
static const String apiBaseUrl = 'https://nome-da-sua-app.herokuapp.com/api/v1';
```

### 2. `frontend/lib/services/api_service.dart`

**Linha 8** - Altere de:

```dart
static const String baseUrl = 'http://localhost:8000/api/v1';
```

Para:

```dart
static const String baseUrl = 'https://nome-da-sua-app.herokuapp.com/api/v1';
```

### 3. `frontend/lib/services/auth_service.dart`

**Linha 8** - Altere de:

```dart
static const String baseUrl = 'http://localhost:8000/api/v1';
```

Para:

```dart
static const String baseUrl = 'https://nome-da-sua-app.herokuapp.com/api/v1';
```

## Passo a Passo

1. **Fazer deploy do backend no Heroku** (siga o guia em `DEPLOY_HEROKU.md`)

2. **Anotar a URL do Heroku** (ex: `https://sua-app.herokuapp.com`)

3. **Editar os 3 arquivos acima** e substituir `http://localhost:8000/api/v1` pela URL do Heroku

4. **Gerar o APK:**

   ```bash
   cd frontend
   flutter build apk --release
   ```

5. **O APK estará em:**

   ```
   frontend/build/app/outputs/flutter-apk/app-release.apk
   ```

6. **Fazer upload do APK no Google Drive** e compartilhar o link de download

## Importante ⚠️

- **HTTPS**: O Heroku fornece HTTPS automaticamente. Certifique-se de usar `https://` e não `http://`
- **CORS**: O backend já está configurado para aceitar requisições de qualquer origem (`CORS_ORIGINS = ["*"]`)
- **Teste**: Antes de gerar o APK final, teste a conexão com a API do Heroku usando um emulador ou dispositivo físico

## Exemplo de URL Completa

Se sua app no Heroku for `orcamentos-api-2025`, a URL será:

```
https://orcamentos-api-2025.herokuapp.com/api/v1
```

## Dica 💡

Se quiser facilitar futuras alterações, considere criar um arquivo de configuração único que seja usado por todos os serviços. Mas para uma solução rápida, alterar os 3 arquivos acima é suficiente.
