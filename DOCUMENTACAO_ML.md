# 📘 Documentação de Machine Learning (ML) – Projeto ABP WorcaFlow

## Visão Geral

O sistema de ML auxilia a criar e orçar serviços residenciais com:

- Predição de categoria do serviço a partir do texto
- Predição de preço sugerido a partir do texto (com limites mínimo e máximo)
- Sugestões de título e descrição profissionais

Os modelos ficam em `backend/models/`:

- `category_model.pkl`, `category_vectorizer.pkl`
- `price_model.pkl`, `price_vectorizer.pkl`

O serviço ML está em `backend/api/v1/services/ml_service.py` e é exposto por rotas em `backend/api/v1/routes/ml.py`.

## Arquitetura

- Vetorização de texto com `vectorizer.pkl` (TF-IDF ou similar)
- Modelos `*.pkl` treinados com scikit-learn
- Serviço ML carrega os modelos e expõe funções:
  - `predizer_categoria(descricao)` → string
  - `predizer_preco(descricao)` → float
  - `calcular_limites_preco(categoria, descricao, localizacao)` → {valor_minimo, valor_sugerido, valor_maximo, categoria_predita}
  - Classe `MLService` com métodos compatíveis para rotas antigas (`predict_category`, `predict_price`, etc.)

## Lógica de Preço (Limites)

Dado o preço sugerido p:

- mínimo = 0.7 × p
- máximo = 1.5 × p
- Na compatibilidade antiga (MLService.predict_price): min = 0.8 × p, max = 1.2 × p

Essa diferença existe por compatibilidade. Preferir `calcular_limites_preco` como referência atual.

## Endpoints Principais

Rotas em `backend/api/v1/routes/ml.py`:

1. Predição de categoria

- Método: GET
- Path: `/api/v1/ml/predict-category?name=Texto do serviço`
- Retorno: `{ service_name, predicted_category, confidence }`

2. Predição de preço

- Método: GET
- Path: `/api/v1/ml/predict-price?name=Texto&category=Opcional`
- Retorno: `{ service_name, category, suggested_price, min_price, max_price }`

3. Criação inteligente (ML + Excel)

- Método: POST
- Path: `/api/v1/ml/smart-create?name=Texto&user_description=Opcional`
- Fluxo:
  - Prediz categoria e preço
  - Gera título/descrição profissionais
  - Cria `Service` no Excel (`excel_service`)
  - Garante um `Client` padrão
  - Cria um `Quote` com 1 item referenciando o `Service`
- Retorno: predições + IDs criados (service_id, quote_id, quote_number)

4. Retreinar modelos (placeholder)

- Método: POST
- Path: `/api/v1/ml/retrain`
- Retorno: mensagem de sucesso (simulado)

5. Popular dados de treino (Excel)

- Método: POST
- Path: `/api/v1/ml/populate-training-data`
- Adiciona serviços de treino no Excel para enriquecer dados

## Integração com Excel

`excel_service.py` mantém um “banco” em `quotes_data.xlsx` com abas:

- `clients`, `services`, `quotes`, `quote_items`

O endpoint `smart-create` usa ML para sugerir valores e salva diretamente no Excel:

- Cria `Service` com preço sugerido
- Garante `Client` padrão
- Gera `Quote` com item referenciando o serviço

## Como Usar (Exemplos via curl)

- Predizer categoria:

```bash
curl "http://localhost:8000/api/v1/ml/predict-category?name=Instalação de chuveiro elétrico"
```

- Predizer preço:

```bash
curl "http://localhost:8000/api/v1/ml/predict-price?name=Instalação de chuveiro elétrico&category=Elétrica"
```

- Criar serviço inteligente e orçamento:

```bash
curl -X POST "http://localhost:8000/api/v1/ml/smart-create?name=Instalação de torneira&user_description=Troca com vedação"
```

## Treinamento/Atualização de Modelos

Os arquivos `*.pkl` são carregados em tempo de execução. Para atualizar:

1. Treine modelos offline e gere novos `*.pkl`
2. Substitua os arquivos em `backend/models/`
3. Reinicie o backend

O endpoint `/ml/retrain` é um placeholder e pode ser conectado a um pipeline real no futuro.

## Tratamento de Falhas

- Se modelos não carregarem, o serviço retorna valores default (ex.: preço 500.0, categoria "Serviços Gerais")
- Logs simples no console para diagnóstico

## Boas Práticas e Próximos Passos

- Padronizar limites usando `calcular_limites_preco`
- Persistir histórico de predições para analytics
- Implementar retreinamento real com dados do Excel
- Validar entrada de texto (limpeza/normalização)
- Adicionar testes unitários para ML e integração com rotas
