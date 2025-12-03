"""
Testes de Validação dos Modelos ML Carregados
Valida qualidade dos modelos já treinados e salvos
"""
import pytest
import pickle
import os
import numpy as np
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Importa funções necessárias
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../../'))
from train_models import gerar_dados_sinteticos, limpar_texto, CATEGORIAS

# Caminho dos modelos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Thresholds mínimos de qualidade para modelos em produção
MIN_PRODUCTION_CATEGORY_ACCURACY = 0.50  # 50% mínimo para modelo em produção
MAX_PRODUCTION_PRICE_MAE = 250.0  # Erro médio máximo aceitável
MIN_PRODUCTION_PRICE_R2 = 0.30  # R² mínimo aceitável


@pytest.mark.unit
@pytest.mark.slow
@pytest.mark.ml_accuracy
class TestLoadedModelValidation:
    """Testa modelos já carregados (em produção)"""
    
    @pytest.fixture
    def load_models(self):
        """Carrega modelos salvos, se existirem"""
        models = {}
        try:
            # Tenta carregar modelo de categoria
            category_model_path = os.path.join(MODELS_DIR, "category_model.pkl")
            category_vectorizer_path = os.path.join(MODELS_DIR, "category_vectorizer.pkl")
            
            if os.path.exists(category_model_path) and os.path.exists(category_vectorizer_path):
                with open(category_model_path, "rb") as f:
                    models['category_model'] = pickle.load(f)
                with open(category_vectorizer_path, "rb") as f:
                    models['category_vectorizer'] = pickle.load(f)
            
            # Tenta carregar modelo de preço
            price_model_path = os.path.join(MODELS_DIR, "price_model.pkl")
            price_vectorizer_path = os.path.join(MODELS_DIR, "price_vectorizer.pkl")
            
            if os.path.exists(price_model_path) and os.path.exists(price_vectorizer_path):
                with open(price_model_path, "rb") as f:
                    models['price_model'] = pickle.load(f)
                with open(price_vectorizer_path, "rb") as f:
                    models['price_vectorizer'] = pickle.load(f)
                    
        except Exception as e:
            pytest.skip(f"Modelos não puderam ser carregados: {e}")
        
        if not models:
            pytest.skip("Modelos não encontrados. Execute train_models.py primeiro.")
        
        return models
    
    def test_loaded_category_model_has_acceptable_accuracy(self, load_models):
        """Testa se modelo de categoria carregado tem acurácia aceitável"""
        # ARRANGE
        if 'category_model' not in load_models:
            pytest.skip("Modelo de categoria não encontrado")
        
        model = load_models['category_model']
        vectorizer = load_models['category_vectorizer']
        
        # Gera dados de teste
        dados = gerar_dados_sinteticos(n_samples=200)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = dados['categories']
        
        # ACT
        X = vectorizer.transform(textos)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # ASSERT
        assert accuracy >= MIN_PRODUCTION_CATEGORY_ACCURACY, \
            f"Acurácia {accuracy:.4f} está abaixo do mínimo aceitável {MIN_PRODUCTION_CATEGORY_ACCURACY}"
    
    def test_loaded_price_model_has_acceptable_mae(self, load_models):
        """Testa se modelo de preço carregado tem MAE aceitável"""
        # ARRANGE
        if 'price_model' not in load_models:
            pytest.skip("Modelo de preço não encontrado")
        
        model = load_models['price_model']
        vectorizer = load_models['price_vectorizer']
        
        # Gera dados de teste
        dados = gerar_dados_sinteticos(n_samples=200)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = np.array(dados['prices'])
        
        # ACT
        X = vectorizer.transform(textos)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        # ASSERT
        assert mae <= MAX_PRODUCTION_PRICE_MAE, \
            f"MAE {mae:.2f} está acima do máximo aceitável {MAX_PRODUCTION_PRICE_MAE}"
    
    def test_loaded_price_model_has_acceptable_r2(self, load_models):
        """Testa se modelo de preço carregado tem R² aceitável"""
        # ARRANGE
        if 'price_model' not in load_models:
            pytest.skip("Modelo de preço não encontrado")
        
        model = load_models['price_model']
        vectorizer = load_models['price_vectorizer']
        
        # Gera dados de teste
        dados = gerar_dados_sinteticos(n_samples=200)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = np.array(dados['prices'])
        
        # ACT
        X = vectorizer.transform(textos)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        # ASSERT
        assert r2 >= MIN_PRODUCTION_PRICE_R2, \
            f"R² {r2:.4f} está abaixo do mínimo aceitável {MIN_PRODUCTION_PRICE_R2}"
    
    def test_loaded_models_can_predict(self, load_models):
        """Testa se modelos carregados podem fazer predições básicas"""
        # ARRANGE
        textos_teste = [
            "Pintura de parede residencial",
            "Instalação elétrica completa",
            "Limpeza geral de casa",
            "Poda de árvores no jardim"
        ]
        
        # ACT & ASSERT - Testa modelo de categoria
        if 'category_model' in load_models and 'category_vectorizer' in load_models:
            model = load_models['category_model']
            vectorizer = load_models['category_vectorizer']
            
            for texto in textos_teste:
                texto_limpo = limpar_texto(texto)
                X = vectorizer.transform([texto_limpo])
                predicao = model.predict(X)[0]
                
                assert isinstance(predicao, str), f"Predição deve ser string para: {texto}"
                assert len(predicao) > 0, f"Predição não deve estar vazia para: {texto}"
                assert predicao in CATEGORIAS, f"Predição '{predicao}' deve ser categoria válida para: {texto}"
        
        # ACT & ASSERT - Testa modelo de preço
        if 'price_model' in load_models and 'price_vectorizer' in load_models:
            model = load_models['price_model']
            vectorizer = load_models['price_vectorizer']
            
            for texto in textos_teste:
                texto_limpo = limpar_texto(texto)
                X = vectorizer.transform([texto_limpo])
                predicao = model.predict(X)[0]
                
                assert isinstance(predicao, (int, float, np.number)), \
                    f"Predição deve ser numérica para: {texto}"
                assert predicao > 0, f"Preço predito deve ser positivo para: {texto}"
                assert np.isfinite(predicao), f"Preço predito deve ser finito para: {texto}"
    
    def test_loaded_models_consistency(self, load_models):
        """Testa consistência dos modelos carregados"""
        # ARRANGE
        texto_teste = "Instalação de torneira na cozinha"
        
        # ACT & ASSERT
        if 'category_model' in load_models:
            model = load_models['category_model']
            assert hasattr(model, 'predict'), "Modelo de categoria deve ter método predict"
            assert hasattr(model, 'fit'), "Modelo de categoria deve ter método fit"
        
        if 'category_vectorizer' in load_models:
            vectorizer = load_models['category_vectorizer']
            assert hasattr(vectorizer, 'transform'), "Vectorizer deve ter método transform"
            assert hasattr(vectorizer, 'fit'), "Vectorizer deve ter método fit"
            
            # Testa transformação
            texto_limpo = limpar_texto(texto_teste)
            X = vectorizer.transform([texto_limpo])
            assert X.shape[0] == 1, "Transformação deve retornar 1 amostra"
            assert X.shape[1] > 0, "Transformação deve retornar features"
        
        if 'price_model' in load_models:
            model = load_models['price_model']
            assert hasattr(model, 'predict'), "Modelo de preço deve ter método predict"
            assert hasattr(model, 'fit'), "Modelo de preço deve ter método fit"
        
        if 'price_vectorizer' in load_models:
            vectorizer = load_models['price_vectorizer']
            assert hasattr(vectorizer, 'transform'), "Vectorizer deve ter método transform"
            
            # Testa transformação
            texto_limpo = limpar_texto(texto_teste)
            X = vectorizer.transform([texto_limpo])
            assert X.shape[0] == 1, "Transformação deve retornar 1 amostra"
            assert X.shape[1] > 0, "Transformação deve retornar features"

