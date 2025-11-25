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
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report
import re

# Diretório dos modelos
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

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
        
        # Gera preço baseado na categoria
        min_price, max_price = faixas_preco.get(categoria, (100, 500))
        price = np.random.uniform(min_price, max_price)
        
        # Adiciona variação de preço baseada em palavras-chave
        if "completo" in service_name.lower() or "com material" in service_name.lower():
            price *= 1.2
        elif "sem material" in service_name.lower():
            price *= 0.8
        
        # Gera descrição
        descricao = f"{service_name} na categoria {categoria}"
        if np.random.random() > 0.5:
            descricao += f" com qualidade profissional"
        
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
    
    # Treina modelo
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    print("Treinando Random Forest para categorias...")
    model.fit(X_train, y_train)
    
    # Avalia modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Acurácia do modelo de categoria: {accuracy:.4f}")
    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))
    
    return model, vectorizer

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
    
    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Treina modelo
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    print("Treinando Random Forest para preços...")
    model.fit(X_train, y_train)
    
    # Avalia modelo
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"MAE (Mean Absolute Error) do modelo de preço: {mae:.2f}")
    print(f"Erro médio: R$ {mae:.2f}")
    
    return model, vectorizer

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
    category_model, category_vectorizer = treinar_modelo_categoria(dados)
    
    # Treina modelo de preço
    price_model, price_vectorizer = treinar_modelo_preco(dados)
    
    # Salva modelos
    salvar_modelos(category_model, category_vectorizer, price_model, price_vectorizer)
    
    print("\n" + "=" * 60)
    print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    main()

