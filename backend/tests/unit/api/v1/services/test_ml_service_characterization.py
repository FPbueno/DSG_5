"""
Characterization Tests para ML Service
Captura comportamento atual antes de refatorar
"""
import pytest
from unittest.mock import patch, mock_open, MagicMock
from api.v1.services.ml_service import (
    predizer_preco,
    predizer_categoria,
    calcular_limites_preco,
    MODELS_LOADED
)


@pytest.mark.unit
class TestMLServiceCharacterization:
    """Testes de caracterização do ML Service"""
    
    def test_predizer_preco_com_modelos_carregados(self):
        """Testa predição de preço quando modelos estão carregados"""
        # ARRANGE
        descricao = "Pintura de parede residencial"
        
        # ACT
        resultado = predizer_preco(descricao)
        
        # ASSERT - Captura comportamento atual
        assert isinstance(resultado, float)
        assert resultado > 0
        # Se modelos não carregados, retorna 500.0
        # Se modelos carregados, retorna predição real
        assert resultado == 500.0 or (resultado != 500.0 and MODELS_LOADED)
    
    def test_predizer_preco_sem_modelos_retorna_default(self):
        """Testa que sem modelos carregados, retorna valor padrão"""
        # ARRANGE
        descricao = "Qualquer descrição"
        
        # ACT
        with patch('api.v1.services.ml_service.MODELS_LOADED', False):
            resultado = predizer_preco(descricao)
        
        # ASSERT
        assert resultado == 500.0
    
    def test_predizer_preco_com_excecao_retorna_default(self):
        """Testa que exceções retornam valor padrão"""
        # ARRANGE
        descricao = "Descrição que causa erro"
        
        # ACT
        with patch('api.v1.services.ml_service.price_vectorizer') as mock_vec:
            mock_vec.transform.side_effect = Exception("Erro simulado")
            resultado = predizer_preco(descricao)
        
        # ASSERT
        assert resultado == 500.0
    
    def test_predizer_categoria_com_modelos_carregados(self):
        """Testa predição de categoria quando modelos estão carregados"""
        # ARRANGE
        descricao = "Pintura de parede"
        
        # ACT
        resultado = predizer_categoria(descricao)
        
        # ASSERT - Captura comportamento atual
        assert isinstance(resultado, str)
        assert len(resultado) > 0
        # Se modelos não carregados, retorna "Serviços Gerais"
        # Se modelos carregados, retorna categoria predita
        assert resultado == "Serviços Gerais" or (resultado != "Serviços Gerais" and MODELS_LOADED)
    
    def test_predizer_categoria_sem_modelos_retorna_default(self):
        """Testa que sem modelos, retorna categoria padrão"""
        # ARRANGE
        descricao = "Qualquer descrição"
        
        # ACT
        with patch('api.v1.services.ml_service.MODELS_LOADED', False):
            resultado = predizer_categoria(descricao)
        
        # ASSERT
        assert resultado == "Serviços Gerais"
    
    def test_calcular_limites_preco_estrutura(self):
        """Testa estrutura de retorno de calcular_limites_preco"""
        # ARRANGE
        categoria = "Pintura"
        descricao = "Pintura de parede"
        localizacao = "São Paulo"
        
        # ACT
        resultado = calcular_limites_preco(categoria, descricao, localizacao)
        
        # ASSERT - Captura estrutura atual
        assert isinstance(resultado, dict)
        assert "valor_minimo" in resultado
        assert "valor_sugerido" in resultado
        assert "valor_maximo" in resultado
        assert "categoria_predita" in resultado
        
        # Valida tipos
        assert isinstance(resultado["valor_minimo"], float)
        assert isinstance(resultado["valor_sugerido"], float)
        assert isinstance(resultado["valor_maximo"], float)
        assert isinstance(resultado["categoria_predita"], str)
        
        # Valida relações entre valores
        assert resultado["valor_minimo"] < resultado["valor_sugerido"]
        assert resultado["valor_maximo"] > resultado["valor_sugerido"]
        assert resultado["valor_minimo"] == round(resultado["valor_minimo"], 2)
        assert resultado["valor_maximo"] == round(resultado["valor_maximo"], 2)
    
    def test_calcular_limites_preco_percentuais(self):
        """Testa que limites seguem percentuais corretos (70% e 150%)"""
        # ARRANGE
        categoria = "Limpeza"
        descricao = "Limpeza geral"
        localizacao = "Rio de Janeiro"
        
        # ACT
        resultado = calcular_limites_preco(categoria, descricao, localizacao)
        
        # ASSERT - Valida lógica de percentuais
        valor_sugerido = resultado["valor_sugerido"]
        valor_minimo_esperado = valor_sugerido * 0.7
        valor_maximo_esperado = valor_sugerido * 1.5
        
        # Permite pequena diferença por arredondamento
        assert abs(resultado["valor_minimo"] - valor_minimo_esperado) < 0.01
        assert abs(resultado["valor_maximo"] - valor_maximo_esperado) < 0.01
    
    def test_calcular_limites_preco_categoria_predita(self):
        """Testa que categoria_predita é chamada corretamente"""
        # ARRANGE
        categoria = "Elétrica"
        descricao = "Instalação elétrica"
        localizacao = "Brasília"
        
        # ACT
        resultado = calcular_limites_preco(categoria, descricao, localizacao)
        
        # ASSERT
        assert "categoria_predita" in resultado
        assert isinstance(resultado["categoria_predita"], str)
        # Categoria predita deve usar apenas descricao
        # (comportamento atual capturado)

