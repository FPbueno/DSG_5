# 📊 Resultados de Treinamento - Modelos de Machine Learning

Esta pasta contém os gráficos e relatórios gerados automaticamente durante o treinamento dos modelos de ML.

## 📁 Estrutura dos Arquivos

Os arquivos são gerados com um timestamp no formato `YYYYMMDD_HHMMSS` para identificar cada execução de treinamento:

### Gráficos Gerados

1. **`*_confusion_matrix_category.png`**

   - Matriz de confusão do modelo de classificação de categorias
   - Mostra quantas predições corretas e incorretas por categoria

2. **`*_metrics_by_category.png`**

   - Métricas detalhadas por categoria (Precisão, Recall, F1-Score)
   - Ajuda a identificar categorias com melhor/pior performance

3. **`*_scatter_price.png`**

   - Gráfico de dispersão: Valores Reais vs Preditos
   - Mostra MAE, RMSE e R² no título
   - A linha vermelha representa predição perfeita (y=x)

4. **`*_error_distribution_price.png`**

   - Distribuição dos erros de predição
   - Erros absolutos (R$) e percentuais (%)
   - Ajuda a identificar viés ou outliers

5. **`*_price_by_category.png`**

   - Distribuição de preços reais e preditos por categoria
   - Box plots comparativos

6. **`*_training_summary.png`**
   - Resumo visual das métricas principais
   - Acurácia, MAE, R², RMSE com thresholds indicados

### Relatórios

- **`*_training_report.txt`**
  - Relatório em texto com todas as métricas
  - Informações dos modelos
  - Status de aprovação baseado nos thresholds

## 🎯 Thresholds de Qualidade

### Modelo de Categoria

- **Acurácia mínima**: 60%
- Status: ✓ APROVADO se ≥ 60% | ✗ REPROVADO se < 60%

### Modelo de Preço

- **MAE máximo**: R$ 200,00
- **RMSE máximo**: R$ 300,00
- **R² mínimo**: 0.40
- Status: ✓ APROVADO se dentro dos limites | ✗ REPROVADO caso contrário

## 📝 Como Usar

### Gerar Novos Resultados

Execute o script de treinamento:

```bash
cd backend
python train_models.py
```

Os gráficos e relatórios serão gerados automaticamente na pasta `models/training_results/`.

### Visualizar Resultados

1. Navegue até a pasta `backend/models/training_results/`
2. Os arquivos mais recentes terão o timestamp mais recente
3. Abra os arquivos PNG para visualizar os gráficos
4. Leia o relatório `.txt` para detalhes das métricas

## 🔍 Interpretação dos Gráficos

### Matriz de Confusão

- **Diagonal principal**: Predições corretas (quanto maior, melhor)
- **Fora da diagonal**: Erros de classificação
- Use para identificar confusões entre categorias

### Scatter Plot (Preço)

- **Pontos próximos da linha vermelha**: Predições precisas
- **Pontos distantes**: Erros maiores
- **R² alto (>0.5)**: Boa correlação entre real e predito

### Distribuição de Erros

- **Erro médio próximo de zero**: Modelo não tendencioso
- **Erros distribuídos simetricamente**: Bom sinal
- **Outliers**: Pode indicar dados problemáticos ou casos difíceis

### Métricas por Categoria

- **Precisão alta**: Quando prediz, geralmente acerta
- **Recall alto**: Captura bem os casos dessa categoria
- **F1-Score**: Média harmônica entre precisão e recall

## 📊 Exemplo de Estrutura

```
training_results/
├── README.md
├── .gitkeep
├── 20250115_143022_confusion_matrix_category.png
├── 20250115_143022_metrics_by_category.png
├── 20250115_143022_scatter_price.png
├── 20250115_143022_error_distribution_price.png
├── 20250115_143022_price_by_category.png
├── 20250115_143022_training_summary.png
└── 20250115_143022_training_report.txt
```

**Nota**: Os gráficos e relatórios gerados **são commitados no git** para histórico de treinamentos.

## 🚀 Próximos Passos

Após revisar os resultados:

1. **Se métricas estão boas**: Os modelos podem ser usados em produção
2. **Se métricas estão abaixo do esperado**: Considere:
   - Coletar mais dados de treinamento
   - Ajustar hiperparâmetros dos modelos
   - Feature engineering adicional
   - Tentar outros algoritmos

## 📚 Documentação Relacionada

- [`ANÁLISE_DE_RESULTADOS.md`](ANÁLISE_DE_RESULTADOS.md) - **Análise completa dos resultados** (recomendado)
- [`train_models.py`](../train_models.py) - Script de treinamento
- [`training_visualizer.py`](../training_visualizer.py) - Módulo de visualização
- [`MELHORIAS_ANTI_OVERFITTING.md`](../MELHORIAS_ANTI_OVERFITTING.md) - Melhorias implementadas
- [`DOCUMENTACAO_ML.md`](../../DOCUMENTACAO_ML.md) - Documentação geral de ML
