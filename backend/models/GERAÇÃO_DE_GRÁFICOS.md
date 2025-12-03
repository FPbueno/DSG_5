# 📊 Sistema de Geração de Gráficos de Treinamento

Este documento explica o sistema implementado para gerar gráficos e documentação dos resultados de treinamento dos modelos de Machine Learning.

## 🎯 O que foi criado

### 1. Módulo de Visualização (`training_visualizer.py`)

Classe `TrainingVisualizer` que gera automaticamente:

#### Gráficos Gerados:

1. **Matriz de Confusão** (`*_confusion_matrix_category.png`)

   - Visualização da performance do modelo de classificação
   - Mostra acertos e erros por categoria

2. **Métricas por Categoria** (`*_metrics_by_category.png`)

   - Precisão, Recall e F1-Score para cada categoria
   - Gráfico de barras comparativo

3. **Scatter Plot de Preços** (`*_scatter_price.png`)

   - Valores reais vs valores preditos
   - Mostra MAE, RMSE e R² no título
   - Linha de predição perfeita (y=x)

4. **Distribuição de Erros** (`*_error_distribution_price.png`)

   - Histogramas de erros absolutos (R$) e percentuais (%)
   - Ajuda a identificar viés e outliers

5. **Preço por Categoria** (`*_price_by_category.png`)

   - Box plots comparativos de preços reais vs preditos
   - Análise por categoria

6. **Resumo das Métricas** (`*_training_summary.png`)
   - Dashboard com todas as métricas principais
   - Indicadores visuais de aprovação/reprovação baseado em thresholds

#### Relatórios Gerados:

- **Relatório em Texto** (`*_training_report.txt`)
  - Todas as métricas formatadas
  - Informações dos modelos
  - Status de aprovação baseado em thresholds

### 2. Pasta de Resultados (`models/training_results/`)

- Pasta criada automaticamente para armazenar todos os resultados
- Cada execução gera arquivos com timestamp único
- README.md com documentação completa

### 3. Integração com Script de Treinamento

O script `train_models.py` foi atualizado para:

- Gerar gráficos automaticamente após o treinamento
- Salvar todos os resultados na pasta `training_results/`
- Criar relatório detalhado das métricas

## 🚀 Como Usar

### Instalar Dependências

As novas dependências já foram adicionadas ao `requirements.txt`:

```bash
pip install matplotlib seaborn
```

Ou instale todas as dependências:

```bash
cd backend
pip install -r requirements.txt
```

### Executar Treinamento com Gráficos

Simplesmente execute o script de treinamento:

```bash
cd backend
python train_models.py
```

O script irá:

1. Treinar os modelos
2. Salvar os modelos (.pkl)
3. **Gerar automaticamente todos os gráficos**
4. **Criar relatório de treinamento**

### Visualizar Resultados

1. Navegue até `backend/models/training_results/`
2. Encontre os arquivos com timestamp mais recente
3. Abra os arquivos `.png` para ver os gráficos
4. Leia o arquivo `*_training_report.txt` para detalhes

## 📁 Estrutura de Arquivos Gerados

```
backend/models/training_results/
├── README.md                                    # Documentação da pasta
├── .gitkeep                                     # Mantém pasta no git
├── .gitignore                                   # Ignora arquivos gerados
│
├── 20250115_143022_confusion_matrix_category.png
├── 20250115_143022_metrics_by_category.png
├── 20250115_143022_scatter_price.png
├── 20250115_143022_error_distribution_price.png
├── 20250115_143022_price_by_category.png
├── 20250115_143022_training_summary.png
└── 20250115_143022_training_report.txt
```

**Nota**: O timestamp (`20250115_143022`) é gerado automaticamente no formato `YYYYMMDD_HHMMSS`.

## 🎨 Gráficos Detalhados

### 1. Matriz de Confusão

- **O que mostra**: Quantas predições corretas/incorretas por categoria
- **Como ler**: Diagonal = acertos, fora da diagonal = erros
- **Uso**: Identificar categorias que o modelo confunde

### 2. Scatter Plot (Preço)

- **O que mostra**: Dispersão de valores reais vs preditos
- **Como ler**: Pontos próximos da linha vermelha = predições precisas
- **Uso**: Visualizar qualidade geral das predições de preço

### 3. Distribuição de Erros

- **O que mostra**: Histograma dos erros de predição
- **Como ler**: Erro médio próximo de zero = bom, simétrico = ideal
- **Uso**: Detectar viés ou outliers

### 4. Resumo das Métricas

- **O que mostra**: Dashboard com todas as métricas principais
- **Como ler**: Verde = aprovado, vermelho = reprovado (baseado em thresholds)
- **Uso**: Visão geral rápida da qualidade dos modelos

## 📊 Thresholds de Qualidade

Os gráficos e relatórios usam os seguintes thresholds:

### Modelo de Categoria:

- **Acurácia mínima**: 60%
- ✓ Aprovado se ≥ 60%
- ✗ Reprovado se < 60%

### Modelo de Preço:

- **MAE máximo**: R$ 200,00
- **RMSE máximo**: R$ 300,00
- **R² mínimo**: 0.40
- ✓ Aprovado se dentro dos limites
- ✗ Reprovado caso contrário

## 🔧 Personalização

Para ajustar os gráficos ou adicionar novos:

1. Edite `backend/models/training_visualizer.py`
2. Adicione novos métodos na classe `TrainingVisualizer`
3. Chame os métodos no `train_models.py` após o treinamento

### Exemplo de Adicionar Novo Gráfico:

```python
# Em training_visualizer.py
def plot_novo_grafico(self, dados):
    plt.figure(figsize=(10, 6))
    # Seu código aqui
    filename = os.path.join(self.output_dir, f'{self.timestamp}_novo_grafico.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    return filename

# Em train_models.py (na função main)
print("  - Novo gráfico...")
visualizer.plot_novo_grafico(dados)
```

## 📝 Exemplo de Saída do Terminal

```
============================================================
TREINAMENTO DE MODELOS DE MACHINE LEARNING
============================================================

Carregando dataset real...
Gerando dados sintéticos de treinamento...
✓ 1000 amostras sintéticas geradas

✓ Total de 2100 amostras para treinamento
  Faixa de preços: R$ 50.00 - R$ 1500.00

Treinando modelo de categoria...
Acurácia do modelo de categoria: 0.8524

Treinando modelo de preço...
MAE (Mean Absolute Error) do modelo de preço: 142.35
RMSE (Root Mean Squared Error): 189.23
R² (Coeficiente de Determinação): 0.7234

Salvando modelos...
✓ category_model.pkl salvo
✓ category_vectorizer.pkl salvo
✓ price_model.pkl salvo
✓ price_vectorizer.pkl salvo

============================================================
GERANDO GRÁFICOS E DOCUMENTAÇÃO...
============================================================

Gerando gráficos...
  - Matriz de confusão (categoria)...
  - Métricas por categoria...
  - Scatter plot (preço)...
  - Distribuição de erros (preço)...
  - Preço por categoria...
  - Resumo das métricas...
  - Relatório de treinamento...

✓ Gráficos e relatórios salvos em: backend/models/training_results
  Timestamp: 20250115_143022
  Relatório: 20250115_143022_training_report.txt

============================================================
TREINAMENTO CONCLUÍDO COM SUCESSO!
============================================================
```

## 🐛 Troubleshooting

### Erro: "No module named 'matplotlib'"

**Solução**: Instale as dependências:

```bash
pip install matplotlib seaborn
```

### Gráficos não estão sendo gerados

**Solução**: Verifique se há erros no terminal. O script continua mesmo se a geração de gráficos falhar.

### Pasta de resultados não existe

**Solução**: A pasta é criada automaticamente. Se não existir, o script a criará.

## 📚 Arquivos Relacionados

- `backend/train_models.py` - Script principal de treinamento
- `backend/models/training_visualizer.py` - Módulo de visualização
- `backend/models/training_results/README.md` - Documentação da pasta de resultados
- `backend/requirements.txt` - Dependências (matplotlib, seaborn adicionados)

## ✅ Checklist de Funcionalidades

- [x] Geração automática de gráficos após treinamento
- [x] Matriz de confusão para modelo de categoria
- [x] Métricas detalhadas por categoria
- [x] Scatter plot para modelo de preço
- [x] Distribuição de erros
- [x] Análise de preço por categoria
- [x] Resumo visual das métricas
- [x] Relatório em texto
- [x] Pasta organizada com timestamp
- [x] Documentação completa

## 🎉 Pronto para Usar!

O sistema está completo e pronto para gerar gráficos profissionais dos seus modelos de treinamento!
