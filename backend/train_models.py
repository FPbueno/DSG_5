"""
Script de Treinamento dos Modelos de Machine Learning
Treina modelos para predição de categoria e preço de serviços residenciais

Como usar:
    python backend/train_models.py

O script irá:
    1. Gerar dados sintéticos de treinamento (2000 amostras)
    2. Treinar modelo de classificação para categorias (Random Forest)
    3. Treinar modelo de regressão para preços (Random Forest)
    4. Salvar modelos em backend/models/*.pkl

Modelos gerados:
    - category_model.pkl: Modelo de classificação de categorias
    - category_vectorizer.pkl: Vetorizador TF-IDF para categorias
    - price_model.pkl: Modelo de regressão de preços
    - price_vectorizer.pkl: Vetorizador TF-IDF para preços
"""
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import (
    accuracy_score, 
    mean_absolute_error, 
    mean_squared_error,
    r2_score,
    classification_report
)
import re

# Diretório dos modelos
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Diretório para resultados e gráficos
RESULTS_DIR = os.path.join(MODELS_DIR, "training_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Categorias de serviços
CATEGORIAS = [
    "Pintura", "Elétrica", "Hidráulica", "Encanamento", 
    "Limpeza", "Jardim", "Pedreiro", "Gesso", 
    "Marcenaria", "Vidraçaria", "Serralheria", "Ar-condicionado",
    "Eletrodomésticos", "Montagem de Móveis", "Faxina", 
    "Jardinagem", "Dedetização", "Limpeza de Estofados",
    "Serviços Gerais"
]

def gerar_dados_sinteticos(n_samples=1000):
    """
    Gera dados sintéticos de treinamento para os modelos
    """
    np.random.seed(42)
    
    # Padrões de serviços por categoria
    padroes_servicos = {
        "Pintura": [
            "Pintura de parede", "Pintura de teto", "Pintura externa",
            "Pintura de portas", "Pintura de janelas", "Pintura de muro",
            "Preparação de superfície", "Aplicação de tinta", "Lixamento"
        ],
        "Elétrica": [
            "Instalação elétrica", "Troca de fiação", "Instalação de chuveiro",
            "Instalação de tomadas", "Reparo elétrico", "Instalação de disjuntores",
            "Troca de lâmpadas", "Instalação de ventilador", "Fiação elétrica"
        ],
        "Hidráulica": [
            "Instalação de torneira", "Troca de registro", "Desentupimento",
            "Instalação de chuveiro", "Reparo de vazamento", "Instalação de pia",
            "Troca de canos", "Instalação de válvula", "Manutenção hidráulica"
        ],
        "Encanamento": [
            "Desentupimento de pia", "Desentupimento de vaso", "Troca de canos",
            "Instalação de encanamento", "Reparo de vazamento", "Instalação de torneira",
            "Manutenção de encanamento", "Substituição de tubulação"
        ],
        "Limpeza": [
            "Limpeza geral", "Limpeza pós-obra", "Limpeza de janelas",
            "Limpeza de estofados", "Limpeza profunda", "Faxina completa",
            "Limpeza de carpetes", "Limpeza de cortinas"
        ],
        "Jardim": [
            "Poda de árvores", "Corte de grama", "Plantio de mudas",
            "Manutenção de jardim", "Paisagismo", "Instalação de irrigação",
            "Adubação", "Controle de pragas"
        ],
        "Pedreiro": [
            "Reboco de parede", "Assentamento de azulejo", "Construção de muro",
            "Reforma de banheiro", "Reforma de cozinha", "Construção de calçada",
            "Alvenaria", "Acabamento"
        ],
        "Gesso": [
            "Instalação de gesso", "Reparo de gesso", "Pintura de gesso",
            "Gesso decorativo", "Sancas de gesso", "Revestimento de gesso"
        ],
        "Marcenaria": [
            "Fabricação de móveis", "Instalação de armários", "Reparo de móveis",
            "Montagem de móveis", "Restauração de móveis", "Instalação de prateleiras"
        ],
        "Vidraçaria": [
            "Troca de vidros", "Instalação de vidros", "Reparo de vidros",
            "Instalação de box", "Espelhos", "Vidros temperados"
        ],
        "Serralheria": [
            "Fabricação de portões", "Instalação de grades", "Reparo de portões",
            "Solda", "Instalação de corrimão", "Fabricação de estruturas"
        ],
        "Ar-condicionado": [
            "Instalação de ar-condicionado", "Manutenção de ar-condicionado",
            "Limpeza de ar-condicionado", "Troca de gás", "Reparo de ar-condicionado"
        ],
        "Eletrodomésticos": [
            "Instalação de máquina de lavar", "Instalação de geladeira",
            "Reparo de eletrodomésticos", "Manutenção de eletrodomésticos"
        ],
        "Montagem de Móveis": [
            "Montagem de guarda-roupas", "Montagem de camas", "Montagem de mesas",
            "Montagem de estantes", "Montagem de móveis planejados"
        ],
        "Faxina": [
            "Faxina completa", "Faxina semanal", "Faxina mensal",
            "Faxina pós-obra", "Faxina de mudança"
        ],
        "Jardinagem": [
            "Jardinagem completa", "Manutenção de jardim", "Paisagismo",
            "Corte e poda", "Plantio"
        ],
        "Dedetização": [
            "Dedetização residencial", "Controle de pragas", "Fumigação",
            "Desinsetização", "Desratização"
        ],
        "Limpeza de Estofados": [
            "Limpeza de sofás", "Limpeza de cadeiras", "Limpeza de colchões",
            "Limpeza de tapetes", "Limpeza de cortinas"
        ],
        "Serviços Gerais": [
            "Serviço geral", "Manutenção geral", "Reparo geral",
            "Serviço residencial", "Manutenção residencial"
        ]
    }
    
    # Faixas de preço por categoria (em reais)
    faixas_preco = {
        "Pintura": (150, 800),
        "Elétrica": (100, 600),
        "Hidráulica": (80, 500),
        "Encanamento": (100, 600),
        "Limpeza": (50, 300),
        "Jardim": (80, 400),
        "Pedreiro": (200, 1000),
        "Gesso": (150, 700),
        "Marcenaria": (300, 1500),
        "Vidraçaria": (100, 600),
        "Serralheria": (200, 1200),
        "Ar-condicionado": (200, 800),
        "Eletrodomésticos": (100, 500),
        "Montagem de Móveis": (150, 600),
        "Faxina": (80, 250),
        "Jardinagem": (100, 400),
        "Dedetização": (150, 500),
        "Limpeza de Estofados": (100, 400),
        "Serviços Gerais": (100, 500)
    }
    
    service_names = []
    categories = []
    prices = []
    descriptions = []
    
    for _ in range(n_samples):
        # Seleciona categoria aleatória
        categoria = np.random.choice(CATEGORIAS)
        
        # Seleciona serviço da categoria
        servicos = padroes_servicos.get(categoria, ["Serviço geral"])
        servico_base = np.random.choice(servicos)
        
        # Adiciona variações ao nome do serviço
        variacoes = [
            f"{servico_base}",
            f"{servico_base} residencial",
            f"{servico_base} completo",
            f"{servico_base} profissional",
            f"Serviço de {servico_base}",
            f"{servico_base} com material",
            f"{servico_base} sem material"
        ]
        service_name = np.random.choice(variacoes)
        
        # Gera preço baseado na categoria com mais variação (mais realista)
        min_price, max_price = faixas_preco.get(categoria, (100, 500))
        # Adiciona mais variabilidade usando distribuição normal truncada
        price_mean = (min_price + max_price) / 2
        price_std = (max_price - min_price) / 4
        price = np.random.normal(price_mean, price_std)
        # Garante que está dentro da faixa
        price = np.clip(price, min_price, max_price)
        
        # Adiciona variação de preço baseada em palavras-chave (com ruído)
        if "completo" in service_name.lower() or "com material" in service_name.lower():
            price *= (1.15 + np.random.uniform(-0.1, 0.15))  # Variação ao invés de fixo
        elif "sem material" in service_name.lower():
            price *= (0.85 + np.random.uniform(-0.1, 0.1))  # Variação ao invés de fixo
        
        # Adiciona ruído aleatório (5-10%) para tornar mais realista
        price *= (1 + np.random.uniform(-0.05, 0.1))
        
        # Gera descrição mais variada e realista
        descricoes_variadas = [
            f"{service_name} na categoria {categoria}",
            f"{service_name} - {categoria}",
            f"Serviço de {service_name}",
            f"{service_name} profissional",
            f"{service_name} completo",
            f"{service_name} com material incluso",
            f"{service_name} sem material"
        ]
        descricao = np.random.choice(descricoes_variadas)
        
        # Adiciona variações aleatórias de texto
        if np.random.random() > 0.7:
            variações = [" de qualidade", " especializado", " rápido", " eficiente"]
            descricao += np.random.choice(variações)
        
        service_names.append(service_name)
        categories.append(categoria)
        prices.append(round(price, 2))
        descriptions.append(descricao)
    
    return {
        'service_names': service_names,
        'categories': categories,
        'prices': prices,
        'descriptions': descriptions
    }

def carregar_dataset_real():
    """
    Carrega dataset real de serviços se disponível
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "models", "training_model", "services_dataset.csv")
    
    if not os.path.exists(dataset_path):
        print(f"⚠️ Dataset real não encontrado em {dataset_path}")
        return None
    
    try:
        df = pd.read_csv(dataset_path)
        
        # Prepara dados no formato esperado
        service_names = df['service_name'].fillna('').astype(str).tolist()
        categories = df['category'].fillna('Serviços Gerais').astype(str).tolist()
        prices = df['total_price'].fillna(500.0).astype(float).tolist()
        
        # Cria descrições combinando informações disponíveis
        descriptions = []
        for idx, row in df.iterrows():
            desc = f"{row['service_name']} {row['category']}"
            if pd.notna(row.get('complexity_level')):
                desc += f" {row['complexity_level']}"
            descriptions.append(desc)
        
        print(f"✓ Dataset real carregado: {len(service_names)} amostras")
        print(f"  Faixa de preços: R$ {min(prices):.2f} - R$ {max(prices):.2f}")
        
        return {
            'service_names': service_names,
            'categories': categories,
            'prices': prices,
            'descriptions': descriptions
        }
    except Exception as e:
        print(f"⚠️ Erro ao carregar dataset real: {e}")
        return None

def limpar_texto(texto):
    """
    Limpa e normaliza texto para processamento
    """
    if not isinstance(texto, str):
        texto = str(texto)
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def treinar_modelo_categoria(dados):
    """
    Treina modelo de classificação para categorias
    """
    print("Treinando modelo de categoria...")
    
    # Prepara dados
    textos = [f"{nome} {desc}" for nome, desc in zip(dados['service_names'], dados['descriptions'])]
    textos = [limpar_texto(t) for t in textos]
    y = dados['categories']
    
    # Vetorização TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    X = vectorizer.fit_transform(textos)
    
    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Treina modelo com hiperparâmetros ajustados para reduzir overfitting
    # Reduzido max_depth, aumentado min_samples para maior regularização
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,  # Reduzido de 20 para 10 (reduz complexidade)
        min_samples_split=10,  # Aumentado de 5 para 10 (mais regularização)
        min_samples_leaf=5,  # Aumentado de 2 para 5 (mais regularização)
        max_features='sqrt',  # Limita features por split (reduz overfitting)
        random_state=42,
        n_jobs=-1
    )
    
    print("Treinando Random Forest para categorias...")
    model.fit(X_train, y_train)
    
    # Avalia modelo no conjunto de teste
    y_pred = model.predict(X_test)
    accuracy_test = accuracy_score(y_test, y_pred)
    
    # Avalia modelo no conjunto de treino (para detectar overfitting)
    y_pred_train = model.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    
    # Validação cruzada para melhor estimativa
    print("\nExecutando validação cruzada (5-fold)...")
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    print(f"\n{'='*60}")
    print("RESULTADOS - MODELO DE CATEGORIA")
    print(f"{'='*60}")
    print(f"Acurácia no TREINO: {accuracy_train:.4f} ({accuracy_train*100:.2f}%)")
    print(f"Acurácia no TESTE:  {accuracy_test:.4f} ({accuracy_test*100:.2f}%)")
    print(f"Validação Cruzada:  {cv_mean:.4f} ± {cv_std:.4f}")
    
    # Detecta overfitting
    diff = accuracy_train - accuracy_test
    if diff > 0.15:  # Diferença maior que 15% indica overfitting
        print(f"\n⚠️  ATENÇÃO: Possível overfitting detectado!")
        print(f"    Diferença Treino-Teste: {diff:.4f} ({diff*100:.2f}%)")
    elif diff > 0.10:
        print(f"\n⚠️  ATENÇÃO: Diferença moderada detectada.")
        print(f"    Diferença Treino-Teste: {diff:.4f} ({diff*100:.2f}%)")
    else:
        print(f"\n✓ Diferença Treino-Teste aceitável: {diff:.4f} ({diff*100:.2f}%)")
    
    print(f"\nRelatório de classificação (TESTE):")
    print(classification_report(y_test, y_pred))
    
    return model, vectorizer, (X_test, y_test, y_pred)

def treinar_modelo_preco(dados):
    """
    Treina modelo de regressão para preços
    """
    print("\nTreinando modelo de preço...")
    
    # Prepara dados
    textos = [f"{nome} {desc}" for nome, desc in zip(dados['service_names'], dados['descriptions'])]
    textos = [limpar_texto(t) for t in textos]
    y = np.array(dados['prices'])
    
    # Vetorização TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    X = vectorizer.fit_transform(textos)
    
    # Divisão treino/teste (com índices para obter categorias depois)
    indices = np.arange(len(y))
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(
        X, y, indices, test_size=0.2, random_state=42
    )
    
    # Treina modelo com hiperparâmetros ajustados para reduzir overfitting
    # Reduzido max_depth, aumentado min_samples para maior regularização
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,  # Reduzido de 20 para 10 (reduz complexidade)
        min_samples_split=10,  # Aumentado de 5 para 10 (mais regularização)
        min_samples_leaf=5,  # Aumentado de 2 para 5 (mais regularização)
        max_features='sqrt',  # Limita features por split (reduz overfitting)
        random_state=42,
        n_jobs=-1
    )
    
    print("Treinando Random Forest para preços...")
    model.fit(X_train, y_train)
    
    # Avalia modelo no conjunto de teste
    y_pred = model.predict(X_test)
    mae_test = mean_absolute_error(y_test, y_pred)
    mse_test = mean_squared_error(y_test, y_pred)
    rmse_test = np.sqrt(mse_test)
    r2_test = r2_score(y_test, y_pred)
    
    # Avalia modelo no conjunto de treino (para detectar overfitting)
    y_pred_train = model.predict(X_train)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    mse_train = mean_squared_error(y_train, y_pred_train)
    rmse_train = np.sqrt(mse_train)
    r2_train = r2_score(y_train, y_pred_train)
    
    # Validação cruzada para melhor estimativa
    print("\nExecutando validação cruzada (5-fold) para R²...")
    cv_scores_r2 = cross_val_score(model, X_train, y_train, cv=5, scoring='r2', n_jobs=-1)
    cv_r2_mean = cv_scores_r2.mean()
    cv_r2_std = cv_scores_r2.std()
    
    print(f"\n{'='*60}")
    print("RESULTADOS - MODELO DE PREÇO")
    print(f"{'='*60}")
    print(f"\nMÉTRICAS NO TREINO:")
    print(f"  MAE:  R$ {mae_train:.2f}")
    print(f"  RMSE: R$ {rmse_train:.2f}")
    print(f"  R²:   {r2_train:.4f}")
    
    print(f"\nMÉTRICAS NO TESTE:")
    print(f"  MAE:  R$ {mae_test:.2f}")
    print(f"  RMSE: R$ {rmse_test:.2f}")
    print(f"  R²:   {r2_test:.4f}")
    
    print(f"\nVALIDAÇÃO CRUZADA (R²):")
    print(f"  Média: {cv_r2_mean:.4f} ± {cv_r2_std:.4f}")
    
    # Detecta overfitting
    r2_diff = r2_train - r2_test
    mae_diff = mae_test - mae_train  # Normalmente teste tem MAE maior
    
    if r2_diff > 0.20:  # Diferença grande no R² indica overfitting
        print(f"\n⚠️  ATENÇÃO: Possível overfitting detectado!")
        print(f"    Diferença R² Treino-Teste: {r2_diff:.4f} ({r2_diff*100:.2f}%)")
    elif r2_diff > 0.15:
        print(f"\n⚠️  ATENÇÃO: Diferença moderada no R².")
        print(f"    Diferença R² Treino-Teste: {r2_diff:.4f} ({r2_diff*100:.2f}%)")
    else:
        print(f"\n✓ Diferença R² Treino-Teste aceitável: {r2_diff:.4f} ({r2_diff*100:.2f}%)")
    
    # Usa métricas de teste para retorno
    mae = mae_test
    rmse = rmse_test
    r2 = r2_test
    
    # Retorna também índices de teste e categorias para visualização
    categories_test = [dados['categories'][i] for i in indices_test]
    
    return model, vectorizer, (X_test, y_test, y_pred, indices_test, categories_test)

def salvar_modelos(category_model, category_vectorizer, price_model, price_vectorizer):
    """
    Salva modelos e vectorizers em arquivos .pkl
    """
    print("\nSalvando modelos...")
    
    # Salva modelo de categoria
    with open(os.path.join(MODELS_DIR, "category_model.pkl"), "wb") as f:
        pickle.dump(category_model, f)
    print("✓ category_model.pkl salvo")
    
    # Salva vectorizer de categoria
    with open(os.path.join(MODELS_DIR, "category_vectorizer.pkl"), "wb") as f:
        pickle.dump(category_vectorizer, f)
    print("✓ category_vectorizer.pkl salvo")
    
    # Salva modelo de preço
    with open(os.path.join(MODELS_DIR, "price_model.pkl"), "wb") as f:
        pickle.dump(price_model, f)
    print("✓ price_model.pkl salvo")
    
    # Salva vectorizer de preço
    with open(os.path.join(MODELS_DIR, "price_vectorizer.pkl"), "wb") as f:
        pickle.dump(price_vectorizer, f)
    print("✓ price_vectorizer.pkl salvo")
    
    print(f"\nModelos salvos em: {MODELS_DIR}")

def combinar_dados(dados_real, dados_sinteticos):
    """
    Combina dados reais e sintéticos
    """
    if dados_real is None:
        return dados_sinteticos
    
    # Combina os dados
    dados_combinados = {
        'service_names': dados_real['service_names'] + dados_sinteticos['service_names'],
        'categories': dados_real['categories'] + dados_sinteticos['categories'],
        'prices': dados_real['prices'] + dados_sinteticos['prices'],
        'descriptions': dados_real['descriptions'] + dados_sinteticos['descriptions']
    }
    
    return dados_combinados

def main():
    """
    Função principal de treinamento
    """
    print("=" * 60)
    print("TREINAMENTO DE MODELOS DE MACHINE LEARNING")
    print("=" * 60)
    
    # Carrega dataset real
    print("\nCarregando dataset real...")
    dados_real = carregar_dataset_real()
    
    # Gera dados sintéticos
    print("\nGerando dados sintéticos de treinamento...")
    dados_sinteticos = gerar_dados_sinteticos(n_samples=1000)
    print(f"✓ {len(dados_sinteticos['service_names'])} amostras sintéticas geradas")
    
    # Combina dados
    dados = combinar_dados(dados_real, dados_sinteticos)
    print(f"\n✓ Total de {len(dados['service_names'])} amostras para treinamento")
    print(f"  Faixa de preços: R$ {min(dados['prices']):.2f} - R$ {max(dados['prices']):.2f}")
    
    # Treina modelo de categoria
    category_model, category_vectorizer, (X_test_cat, y_test_cat, y_pred_cat) = treinar_modelo_categoria(dados)
    
    # Treina modelo de preço
    price_model, price_vectorizer, (X_test_price, y_test_price, y_pred_price, indices_test_price, categories_test_price) = treinar_modelo_preco(dados)
    
    # Salva modelos
    salvar_modelos(category_model, category_vectorizer, price_model, price_vectorizer)
    
    # Gera gráficos e documentação
    print("\n" + "=" * 60)
    print("GERANDO GRÁFICOS E DOCUMENTAÇÃO...")
    print("=" * 60)
    
    try:
        from models.training_visualizer import TrainingVisualizer
        
        visualizer = TrainingVisualizer(RESULTS_DIR)
        
        # Calcula métricas
        category_accuracy = accuracy_score(y_test_cat, y_pred_cat)
        price_mae = mean_absolute_error(y_test_price, y_pred_price)
        price_rmse = np.sqrt(mean_squared_error(y_test_price, y_pred_price))
        price_r2 = r2_score(y_test_price, y_pred_price)
        
        metrics = {
            'category_accuracy': category_accuracy,
            'price_mae': price_mae,
            'price_rmse': price_rmse,
            'price_r2': price_r2
        }
        
        model_info = {
            'Modelo de Categoria': 'Random Forest Classifier',
            'Modelo de Preço': 'Random Forest Regressor',
            'Total de Amostras': len(dados['service_names']),
            'Amostras de Treino': int(len(dados['service_names']) * 0.8),
            'Amostras de Teste': int(len(dados['service_names']) * 0.2),
            'Categorias': len(CATEGORIAS)
        }
        
        # Gera gráficos
        print("\nGerando gráficos...")
        
        # Matriz de confusão - categoria
        print("  - Matriz de confusão (categoria)...")
        visualizer.plot_category_confusion_matrix(y_test_cat, y_pred_cat, CATEGORIAS)
        
        # Métricas por categoria
        print("  - Métricas por categoria...")
        visualizer.plot_category_accuracy_by_class(y_test_cat, y_pred_cat, CATEGORIAS)
        
        # Scatter plot - preço
        print("  - Scatter plot (preço)...")
        visualizer.plot_price_prediction_scatter(y_test_price, y_pred_price)
        
        # Distribuição de erros - preço
        print("  - Distribuição de erros (preço)...")
        visualizer.plot_price_error_distribution(y_test_price, y_pred_price)
        
        # Preço por categoria - usa dados de teste do modelo de preço
        dados_test_price = {
            'categories': categories_test_price,
            'prices': y_test_price.tolist() if isinstance(y_test_price, np.ndarray) else list(y_test_price)
        }
        
        print("  - Preço por categoria...")
        visualizer.plot_price_by_category(dados_test_price, y_pred_price, y_test_price)
        
        # Resumo das métricas
        print("  - Resumo das métricas...")
        visualizer.plot_training_summary(metrics)
        
        # Gera relatório
        print("  - Relatório de treinamento...")
        report_file = visualizer.generate_report(metrics, model_info)
        
        print(f"\n✓ Gráficos e relatórios salvos em: {RESULTS_DIR}")
        print(f"  Timestamp: {visualizer.timestamp}")
        print(f"  Relatório: {os.path.basename(report_file)}")
        
    except ImportError as e:
        print(f"\n⚠️ Aviso: Não foi possível gerar gráficos: {e}")
        print("  Instale matplotlib e seaborn: pip install matplotlib seaborn")
    except Exception as e:
        print(f"\n⚠️ Aviso: Erro ao gerar gráficos: {e}")
    
    print("\n" + "=" * 60)
    print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    main()

