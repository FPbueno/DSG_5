"""
Serviço de Machine Learning para Predição de Preços e Categorias
"""
import pickle
import os
from typing import Dict

# Caminhos dos modelos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Carregar modelos
try:
    with open(os.path.join(MODELS_DIR, "price_model.pkl"), "rb") as f:
        price_model = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "price_vectorizer.pkl"), "rb") as f:
        price_vectorizer = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "category_model.pkl"), "rb") as f:
        category_model = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "category_vectorizer.pkl"), "rb") as f:
        category_vectorizer = pickle.load(f)
    
    MODELS_LOADED = True
except Exception as e:
    print(f"⚠️ Aviso: Modelos ML não carregados: {e}")
    MODELS_LOADED = False

def predizer_preco(descricao: str) -> float:
    """Prediz preço baseado na descrição do serviço"""
    if not MODELS_LOADED:
        return 500.0
    
    try:
        X = price_vectorizer.transform([descricao])
        preco = price_model.predict(X)[0]
        return float(preco)
    except Exception as e:
        print(f"Erro ao predizer preço: {e}")
        return 500.0

def predizer_categoria(descricao: str) -> str:
    """Prediz categoria baseada na descrição do serviço"""
    if not MODELS_LOADED:
        return "Serviços Gerais"
    
    try:
        X = category_vectorizer.transform([descricao])
        categoria = category_model.predict(X)[0]
        return str(categoria)
    except Exception as e:
        print(f"Erro ao predizer categoria: {e}")
        return "Serviços Gerais"

def calcular_limites_preco(
    categoria: str,
    descricao: str,
    localizacao: str
) -> Dict[str, float]:
    """
    Calcula limites de preço (mínimo, sugerido, máximo)
    para orientação do prestador
    
    Lógica:
    - Valor sugerido: predição do ML
    - Valor mínimo: 70% do valor sugerido
    - Valor máximo: 150% do valor sugerido
    """
    texto_completo = f"{categoria} {descricao} {localizacao}"
    valor_sugerido = predizer_preco(texto_completo)
    
    valor_minimo = valor_sugerido * 0.7
    valor_maximo = valor_sugerido * 1.5
    
    return {
        "valor_minimo": round(valor_minimo, 2),
        "valor_sugerido": round(valor_sugerido, 2),
        "valor_maximo": round(valor_maximo, 2),
        "categoria_predita": predizer_categoria(descricao)
    }

# ============= CLASSE PARA COMPATIBILIDADE COM CÓDIGO ANTIGO =============

class MLService:
    """Classe de serviço ML para compatibilidade com rotas antigas"""
    
    def __init__(self):
        self.training_data = {
            'service_names': [],
            'categories': [],
            'prices': [],
            'descriptions': []
        }
    
    def predict_category(self, name: str) -> str:
        """Prediz categoria"""
        return predizer_categoria(name)
    
    def predict_price(self, name: str, category: str = None) -> dict:
        """Prediz preço"""
        texto = f"{category} {name}" if category else name
        preco = predizer_preco(texto)
        return {
            "suggested_price": preco,
            "min_price": preco * 0.8,
            "max_price": preco * 1.2
        }
    
    def generate_professional_description(self, name: str, category: str) -> str:
        """Gera descrição profissional"""
        return f"Serviço de {category}: {name}"
    
    def generate_professional_title(self, name: str, category: str) -> str:
        """Gera título profissional"""
        return f"{category} - {name}"
    
    def retrain_with_new_data(self) -> bool:
        """Retreina modelos (placeholder)"""
        return True

# Instância global para compatibilidade
ml_service = MLService()
