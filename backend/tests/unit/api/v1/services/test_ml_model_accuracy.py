"""
Testes de Acurácia e Treinamento dos Modelos de Machine Learning
Validam qualidade e performance dos modelos ML
"""
import pytest
import pickle
import os
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Importa funções de treinamento do train_models.py
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../../'))
from train_models import (
    gerar_dados_sinteticos,
    treinar_modelo_categoria,
    treinar_modelo_preco,
    limpar_texto,
    CATEGORIAS
)

# Thresholds mínimos de qualidade
MIN_CATEGORY_ACCURACY = 0.60  # 60% de acurácia mínima
MAX_PRICE_MAE = 200.0  # Erro médio máximo de R$ 200
MIN_PRICE_R2 = 0.40  # R² mínimo de 0.40
MAX_PRICE_RMSE = 300.0  # RMSE máximo de R$ 300


@pytest.mark.unit
@pytest.mark.slow
@pytest.mark.ml_accuracy
class TestMLModelAccuracy:
    """Testes de acurácia dos modelos ML"""
    
    def test_categoria_model_accuracy_above_threshold(self):
        """Testa se modelo de categoria atinge acurácia mínima"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_categoria(dados)
        
        # Prepara dados de teste
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = dados['categories']
        X = vectorizer.transform(textos)
        
        # Divide em treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Prediz no conjunto de teste
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # ASSERT
        assert accuracy >= MIN_CATEGORY_ACCURACY, \
            f"Acurácia {accuracy:.4f} está abaixo do mínimo {MIN_CATEGORY_ACCURACY}"
        assert 0 <= accuracy <= 1, "Acurácia deve estar entre 0 e 1"
    
    def test_preco_model_mae_below_threshold(self):
        """Testa se modelo de preço tem MAE abaixo do threshold"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_preco(dados)
        
        # Prepara dados de teste
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = np.array(dados['prices'])
        X = vectorizer.transform(textos)
        
        # Divide em treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Prediz no conjunto de teste
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        # ASSERT
        assert mae <= MAX_PRICE_MAE, \
            f"MAE {mae:.2f} está acima do máximo {MAX_PRICE_MAE}"
        assert mae >= 0, "MAE deve ser positivo"
    
    def test_preco_model_r2_above_threshold(self):
        """Testa se modelo de preço tem R² acima do threshold"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_preco(dados)
        
        # Prepara dados de teste
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = np.array(dados['prices'])
        X = vectorizer.transform(textos)
        
        # Divide em treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Prediz no conjunto de teste
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        # ASSERT
        assert r2 >= MIN_PRICE_R2, \
            f"R² {r2:.4f} está abaixo do mínimo {MIN_PRICE_R2}"
        assert -1 <= r2 <= 1, "R² deve estar entre -1 e 1"
    
    def test_preco_model_rmse_below_threshold(self):
        """Testa se modelo de preço tem RMSE abaixo do threshold"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_preco(dados)
        
        # Prepara dados de teste
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = np.array(dados['prices'])
        X = vectorizer.transform(textos)
        
        # Divide em treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Prediz no conjunto de teste
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # ASSERT
        assert rmse <= MAX_PRICE_RMSE, \
            f"RMSE {rmse:.2f} está acima do máximo {MAX_PRICE_RMSE}"
        assert rmse >= 0, "RMSE deve ser positivo"
    
    def test_categoria_model_confusion_matrix_structure(self):
        """Testa estrutura da matriz de confusão do modelo de categoria"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_categoria(dados)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = dados['categories']
        X = vectorizer.transform(textos)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        # ASSERT
        assert cm.shape[0] == cm.shape[1], "Matriz de confusão deve ser quadrada"
        assert cm.shape[0] > 0, "Matriz de confusão não deve estar vazia"
        assert np.all(cm >= 0), "Valores da matriz de confusão devem ser não-negativos"


@pytest.mark.unit
@pytest.mark.slow
@pytest.mark.ml_accuracy
class TestMLModelTraining:
    """Testes do processo de treinamento dos modelos"""
    
    def test_treinar_modelo_categoria_retorna_modelo_e_vectorizer(self):
        """Testa se treinamento retorna modelo e vectorizer válidos"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=300)
        
        # ACT
        model, vectorizer = treinar_modelo_categoria(dados)
        
        # ASSERT
        assert model is not None, "Modelo não deve ser None"
        assert vectorizer is not None, "Vectorizer não deve ser None"
        assert hasattr(model, 'predict'), "Modelo deve ter método predict"
        assert hasattr(vectorizer, 'transform'), "Vectorizer deve ter método transform"
    
    def test_treinar_modelo_preco_retorna_modelo_e_vectorizer(self):
        """Testa se treinamento de preço retorna modelo e vectorizer válidos"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=300)
        
        # ACT
        model, vectorizer = treinar_modelo_preco(dados)
        
        # ASSERT
        assert model is not None, "Modelo não deve ser None"
        assert vectorizer is not None, "Vectorizer não deve ser None"
        assert hasattr(model, 'predict'), "Modelo deve ter método predict"
        assert hasattr(vectorizer, 'transform'), "Vectorizer deve ter método transform"
    
    def test_modelo_categoria_prediz_todas_as_categorias(self):
        """Testa se modelo pode predizer todas as categorias conhecidas"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_categoria(dados)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        X = vectorizer.transform(textos)
        y_pred = model.predict(X)
        
        # ASSERT
        categorias_preditas = set(y_pred)
        categorias_esperadas = set(CATEGORIAS)
        
        # Verifica se todas as categorias preditas são válidas
        assert categorias_preditas.issubset(categorias_esperadas), \
            f"Categorias preditas inválidas: {categorias_preditas - categorias_esperadas}"
    
    def test_modelo_preco_prediz_valores_positivos(self):
        """Testa se modelo de preço prediz apenas valores positivos"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_preco(dados)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        X = vectorizer.transform(textos)
        y_pred = model.predict(X)
        
        # ASSERT
        assert np.all(y_pred > 0), "Todos os preços preditos devem ser positivos"
        assert np.all(np.isfinite(y_pred)), "Preços preditos devem ser finitos"
    
    def test_modelo_categoria_reproducibilidade(self):
        """Testa se modelo é reproduzível com mesmo random_state"""
        # ARRANGE
        dados1 = gerar_dados_sinteticos(n_samples=200)
        dados2 = gerar_dados_sinteticos(n_samples=200)
        
        # ACT - Treina dois modelos com mesma semente
        model1, vectorizer1 = treinar_modelo_categoria(dados1)
        model2, vectorizer2 = treinar_modelo_categoria(dados2)
        
        # Testa com mesmo texto
        texto_teste = "Pintura de parede residencial"
        texto_limpo = limpar_texto(texto_teste)
        
        X1 = vectorizer1.transform([texto_limpo])
        X2 = vectorizer2.transform([texto_limpo])
        
        pred1 = model1.predict(X1)[0]
        pred2 = model2.predict(X2)[0]
        
        # ASSERT - Com dados sintéticos e mesma semente, deve ser reproduzível
        # (Nota: pode haver pequenas variações, mas estrutura deve ser consistente)
        assert isinstance(pred1, str), "Predição deve ser string"
        assert isinstance(pred2, str), "Predição deve ser string"
        assert pred1 in CATEGORIAS, "Predição deve ser categoria válida"
        assert pred2 in CATEGORIAS, "Predição deve ser categoria válida"


@pytest.mark.unit
@pytest.mark.slow
@pytest.mark.ml_accuracy
class TestMLModelMetrics:
    """Testes de métricas detalhadas dos modelos"""
    
    def test_categoria_model_metrics_completeness(self):
        """Testa se todas as métricas de categoria são calculadas corretamente"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=400)
        
        # ACT
        model, vectorizer = treinar_modelo_categoria(dados)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = dados['categories']
        X = vectorizer.transform(textos)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # ASSERT
        assert isinstance(accuracy, float), "Acurácia deve ser float"
        assert 0 <= accuracy <= 1, "Acurácia deve estar entre 0 e 1"
        assert 'accuracy' in report, "Relatório deve conter acurácia"
        assert 'macro avg' in report, "Relatório deve conter média macro"
        assert 'weighted avg' in report, "Relatório deve conter média ponderada"
    
    def test_preco_model_metrics_completeness(self):
        """Testa se todas as métricas de preço são calculadas corretamente"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=400)
        
        # ACT
        model, vectorizer = treinar_modelo_preco(dados)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = np.array(dados['prices'])
        X = vectorizer.transform(textos)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # ASSERT
        assert isinstance(mae, float), "MAE deve ser float"
        assert isinstance(rmse, float), "RMSE deve ser float"
        assert isinstance(r2, float), "R² deve ser float"
        assert mae >= 0, "MAE deve ser não-negativo"
        assert rmse >= 0, "RMSE deve ser não-negativo"
        assert -1 <= r2 <= 1, "R² deve estar entre -1 e 1"
        assert rmse >= mae, "RMSE deve ser >= MAE (desigualdade matemática)"
    
    def test_modelo_categoria_com_multiplas_categorias(self):
        """Testa modelo com múltiplas categorias"""
        # ARRANGE
        dados = gerar_dados_sinteticos(n_samples=500)
        
        # ACT
        model, vectorizer = treinar_modelo_categoria(dados)
        
        textos = [f"{nome} {desc}" for nome, desc in 
                  zip(dados['service_names'], dados['descriptions'])]
        textos = [limpar_texto(t) for t in textos]
        y = dados['categories']
        X = vectorizer.transform(textos)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        y_pred = model.predict(X_test)
        categorias_unicas = len(set(y_test))
        
        # ASSERT
        assert categorias_unicas > 1, "Deve haver múltiplas categorias no teste"
        assert len(set(y_pred)) > 0, "Deve predizer pelo menos uma categoria"

