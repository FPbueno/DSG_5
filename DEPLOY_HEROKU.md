# Deploy no Heroku - Guia Rápido

Este projeto está configurado para fazer deploy do backend no Heroku.

## Pré-requisitos

1. Conta no Heroku (https://heroku.com)
2. Heroku CLI instalado (https://devcenter.heroku.com/articles/heroku-cli)
3. Git configurado

## Passos para Deploy

### 1. Login no Heroku

```bash
heroku login
```

### 2. Criar uma nova aplicação no Heroku

```bash
heroku create nome-da-sua-app
```

Ou se já tiver uma app criada:

```bash
heroku git:remote -a nome-da-sua-app
```

### 3. Configurar variáveis de ambiente

Configure as variáveis de ambiente necessárias no Heroku:

```bash
heroku config:set DATABASE_URL="sua-url-do-banco"
heroku config:set SUPABASE_URL="sua-url-do-supabase"
heroku config:set SUPABASE_ANON_KEY="sua-chave-anon"
heroku config:set SUPABASE_SERVICE_ROLE_KEY="sua-chave-service-role"
```

**Variáveis importantes:**

- `DATABASE_URL`: URL de conexão do banco de dados (PostgreSQL no Heroku)
- `SUPABASE_URL`: URL do seu projeto Supabase
- `SUPABASE_ANON_KEY`: Chave pública do Supabase
- `SUPABASE_SERVICE_ROLE_KEY`: Chave de serviço do Supabase

### 4. Fazer deploy

```bash
git add .
git commit -m "Preparar para deploy no Heroku"
git push heroku main
```

Ou se sua branch principal for `master`:

```bash
git push heroku master
```

### 5. Verificar logs

```bash
heroku logs --tail
```

### 6. Abrir a aplicação

```bash
heroku open
```

## Estrutura de Arquivos para Heroku

- `Procfile`: Define como iniciar a aplicação
- `runtime.txt`: Especifica a versão do Python (3.11.9)
- `requirements.txt`: Dependências Python (localizado em `backend/requirements.txt`)
- `.slugignore`: Arquivos ignorados no deploy (reduz tamanho)
- `app.json`: Configurações opcionais do Heroku

## Notas Importantes

1. **Banco de Dados**: O Heroku oferece add-ons de PostgreSQL. Você pode adicionar um com:

   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

   Isso automaticamente configura a variável `DATABASE_URL`.

2. **Porta**: O Heroku define automaticamente a variável `PORT`. A aplicação já está configurada para usá-la.

3. **Variáveis de Ambiente**: Não commite o arquivo `.env` com informações sensíveis. Use `heroku config:set` para definir variáveis.

4. **Logs**: Use `heroku logs --tail` para acompanhar o que está acontecendo.

5. **Dynos**: O Heroku oferece um dyno gratuito. Certifique-se de que está ativo:
   ```bash
   heroku ps:scale web=1
   ```

## Troubleshooting

### Erro ao iniciar

- Verifique os logs: `heroku logs --tail`
- Certifique-se de que todas as variáveis de ambiente estão configuradas
- Verifique se o `Procfile` está correto

### Erro de módulos não encontrados

- Verifique se o `requirements.txt` está completo
- Certifique-se de que o PYTHONPATH está configurado corretamente no `Procfile`

### Erro de conexão com banco

- Verifique a `DATABASE_URL`
- Certifique-se de que o banco está acessível
- Para PostgreSQL no Heroku, a URL já vem configurada automaticamente

## Comandos Úteis

```bash
# Ver variáveis de ambiente
heroku config

# Ver logs em tempo real
heroku logs --tail

# Abrir console Python no Heroku
heroku run python

# Reiniciar a aplicação
heroku restart

# Ver status dos dynos
heroku ps

# Executar comando no Heroku
heroku run <comando>
```
