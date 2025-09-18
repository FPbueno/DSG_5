import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
from typing import Dict, List, Optional, Any, Tuple
import re
import pickle
import os
from datetime import datetime
from ..core.config import EXCEL_FILE

class MLService:
    def __init__(self):
        self.excel_file = EXCEL_FILE
        self.models = {}
        self.encoders = {}
        self.vectorizers = {}
        self.is_trained = False
        
        # Dados de treinamento para serviços residenciais
        self.training_data = self._get_training_data()
        
        # Carrega modelos se existirem, senão treina novos
        self._load_or_train_models()
    
    def _get_training_data(self) -> Dict[str, List]:
        """Dados de treinamento expandidos para serviços residenciais"""
        return {
            'service_names': [
                # Elétrica
                'instalacao eletrica', 'manutencao eletrica', 'troca lampada', 
                'instalacao tomada', 'instalacao interruptor', 'quadro eletrico',
                'chuveiro eletrico', 'ventilador teto', 'ar condicionado',
                
                # Hidráulica
                'encanamento', 'vazamento', 'desentupimento', 'instalacao pia',
                'torneira', 'vaso sanitario', 'chuveiro', 'caixa agua',
                'bomba agua', 'filtro agua',
                
                # Pintura
                'pintura parede', 'pintura teto', 'pintura porta', 'pintura janela',
                'textura parede', 'massa corrida', 'primer', 'verniz',
                'pintura externa', 'pintura interna',
                
                # Construção
                'alvenaria', 'reboco', 'contrapiso', 'ceramica', 'azulejo',
                'gesso', 'drywall', 'forro', 'laje', 'fundacao',
                
                # Carpintaria
                'porta madeira', 'janela madeira', 'armario', 'estante',
                'mesa', 'cadeira', 'cama', 'guarda roupa', 'deck madeira',
                
                # Jardinagem
                'poda arvore', 'plantio grama', 'jardim', 'irrigacao',
                'paisagismo', 'cerca viva', 'flores', 'horta',
                
                # Limpeza
                'limpeza casa', 'limpeza pos obra', 'lavagem', 'enceramento',
                'limpeza vidros', 'limpeza carpete', 'dedetizacao',
                
                # Manutenção Geral
                'conserto', 'reparo', 'manutencao', 'ajuste', 'troca',
                'instalacao', 'montagem', 'desmontagem'
            ],
            'categories': [
                'eletrica', 'eletrica', 'eletrica', 'eletrica', 'eletrica', 'eletrica',
                'eletrica', 'eletrica', 'eletrica',
                
                'hidraulica', 'hidraulica', 'hidraulica', 'hidraulica', 'hidraulica',
                'hidraulica', 'hidraulica', 'hidraulica', 'hidraulica', 'hidraulica',
                
                'pintura', 'pintura', 'pintura', 'pintura', 'pintura', 'pintura',
                'pintura', 'pintura', 'pintura', 'pintura',
                
                'construcao', 'construcao', 'construcao', 'construcao', 'construcao',
                'construcao', 'construcao', 'construcao', 'construcao', 'construcao',
                
                'carpintaria', 'carpintaria', 'carpintaria', 'carpintaria', 'carpintaria',
                'carpintaria', 'carpintaria', 'carpintaria', 'carpintaria',
                
                'jardinagem', 'jardinagem', 'jardinagem', 'jardinagem', 'jardinagem',
                'jardinagem', 'jardinagem', 'jardinagem',
                
                'limpeza', 'limpeza', 'limpeza', 'limpeza', 'limpeza', 'limpeza', 'limpeza',
                
                'manutencao', 'manutencao', 'manutencao', 'manutencao', 'manutencao',
                'manutencao', 'manutencao', 'manutencao'
            ],
            'prices': [
                # Elétrica (R$)
                150, 200, 25, 80, 60, 400, 120, 180, 350,
                
                # Hidráulica (R$)
                200, 150, 100, 250, 80, 180, 120, 300, 400, 150,
                
                # Pintura (R$ por m²)
                15, 18, 120, 100, 25, 12, 8, 35, 20, 16,
                
                # Construção (R$ por m²)
                45, 35, 40, 60, 50, 30, 55, 40, 180, 120,
                
                # Carpintaria (R$)
                300, 250, 800, 400, 200, 150, 400, 1200, 80,
                
                # Jardinagem (R$)
                80, 25, 200, 150, 500, 60, 100, 300,
                
                # Limpeza (R$)
                8, 20, 15, 12, 6, 18, 200,
                
                # Manutenção (R$)
                100, 120, 150, 80, 90, 110, 130, 90
            ],
            'descriptions': [
                # Elétrica
                'Instalação elétrica residencial completa com materiais de qualidade',
                'Manutenção preventiva e corretiva em sistemas elétricos residenciais',
                'Troca de lâmpadas LED e convencionais com garantia',
                'Instalação de tomadas padrão NBR com aterramento',
                'Instalação de interruptores simples e paralelos',
                'Montagem e instalação de quadro elétrico residencial',
                'Instalação de chuveiro elétrico com disjuntor dedicado',
                'Instalação de ventilador de teto com controle remoto',
                'Instalação de ar condicionado split com tubulação',
                
                # Hidráulica
                'Serviços de encanamento residencial com tubos PVC e conexões',
                'Reparo de vazamentos em tubulações e conexões hidráulicas',
                'Desentupimento de pias, ralos e vasos sanitários',
                'Instalação de pia com torneira e sifão inclusos',
                'Instalação e reparo de torneiras diversas',
                'Instalação de vaso sanitário com caixa acoplada',
                'Instalação de chuveiro com registro e ducha',
                'Instalação de caixa d\'água com bóia e conexões',
                'Instalação de bomba d\'água pressurizadora',
                'Instalação de filtro de água residencial',
                
                # Pintura
                'Pintura de paredes internas com tinta acrílica premium',
                'Pintura de teto com tinta específica anti-mofo',
                'Pintura de portas de madeira com tinta esmalte',
                'Pintura de janelas com tinta específica para madeira',
                'Aplicação de textura decorativa em paredes',
                'Aplicação de massa corrida para regularização',
                'Aplicação de primer selador antes da pintura',
                'Aplicação de verniz em madeiras para proteção',
                'Pintura externa com tinta acrílica resistente',
                'Pintura interna com acabamento fosco ou acetinado',
                
                # Construção
                'Serviços de alvenaria com tijolos e argamassa',
                'Reboco de paredes com argamassa de cimento e areia',
                'Execução de contrapiso nivelado com argamassa',
                'Assentamento de cerâmica com rejunte incluso',
                'Assentamento de azulejos em banheiros e cozinhas',
                'Aplicação de gesso liso em paredes e tetos',
                'Instalação de drywall com estrutura metálica',
                'Instalação de forro PVC ou gesso',
                'Execução de laje pré-moldada com vigotas',
                'Execução de fundação com sapata e baldrame',
                
                # Carpintaria
                'Fabricação e instalação de porta de madeira maciça',
                'Fabricação e instalação de janela de madeira',
                'Fabricação de armário planejado sob medida',
                'Fabricação de estante de madeira personalizada',
                'Fabricação de mesa de madeira maciça',
                'Fabricação de cadeiras de madeira torneada',
                'Fabricação de cama de casal em madeira',
                'Fabricação de guarda-roupa planejado',
                'Instalação de deck de madeira tratada',
                
                # Jardinagem
                'Poda técnica de árvores e arbustos',
                'Plantio de grama esmeralda ou são carlos',
                'Criação e manutenção de jardim residencial',
                'Instalação de sistema de irrigação automática',
                'Projeto de paisagismo com plantas ornamentais',
                'Plantio e manutenção de cerca viva',
                'Plantio de flores sazonais e ornamentais',
                'Criação de horta orgânica residencial',
                
                # Limpeza
                'Limpeza residencial completa com produtos profissionais',
                'Limpeza pós-obra com remoção de entulhos',
                'Lavagem de pisos com enceramento',
                'Enceramento de pisos com cera líquida',
                'Limpeza de vidros e esquadrias',
                'Limpeza de carpetes com produtos específicos',
                'Dedetização residencial contra pragas urbanas',
                
                # Manutenção
                'Conserto de equipamentos e utensílios domésticos',
                'Reparo de móveis e estruturas de madeira',
                'Manutenção preventiva de sistemas residenciais',
                'Ajuste de portas e janelas desalinhadas',
                'Troca de peças e componentes diversos',
                'Instalação de equipamentos e acessórios',
                'Montagem de móveis e estruturas',
                'Desmontagem cuidadosa de móveis e equipamentos'
            ]
        }
    
    def _load_or_train_models(self):
        """Carrega modelos salvos ou treina novos"""
        model_files = [
            'price_model.pkl', 'category_model.pkl', 
            'price_vectorizer.pkl', 'category_vectorizer.pkl',
            'category_encoder.pkl'
        ]
        
        models_exist = all(os.path.exists(f'models/{file}') for file in model_files)
        
        if models_exist:
            self._load_models()
        else:
            self._train_models()
    
    def _train_models(self):
        """Treina os modelos de ML"""
        print("🤖 Treinando modelos de Machine Learning...")
        
        # Prepara dados históricos do Excel
        historical_data = self._load_historical_data()
        training_data = self.training_data
        
        # Combina dados históricos com dados de treinamento
        all_names = historical_data['names'] + training_data['service_names']
        all_categories = historical_data['categories'] + training_data['categories']
        all_prices = historical_data['prices'] + training_data['prices']
        
        # Treina modelo de categorização
        self._train_category_model(all_names, all_categories)
        
        # Treina modelo de preços
        self._train_price_model(all_names, all_categories, all_prices)
        
        # Salva os modelos
        self._save_models()
        
        self.is_trained = True
        print("✅ Modelos treinados com sucesso!")
    
    def _load_historical_data(self) -> Dict[str, List]:
        """Carrega dados históricos do Excel"""
        try:
            # Carrega dados dos serviços
            services_df = pd.read_excel(self.excel_file, sheet_name='services')
            quotes_df = pd.read_excel(self.excel_file, sheet_name='quotes')
            quote_items_df = pd.read_excel(self.excel_file, sheet_name='quote_items')
            
            names = services_df['name'].tolist() if not services_df.empty else []
            categories = services_df['category'].tolist() if 'category' in services_df.columns else []
            prices = services_df['unit_price'].tolist() if not services_df.empty else []
            
            # Se não há categorias, infere das descrições
            if not categories and names:
                categories = [self._infer_category_from_name(name) for name in names]
            
            return {
                'names': names,
                'categories': categories,
                'prices': prices
            }
        except Exception as e:
            print(f"⚠️ Erro ao carregar dados históricos: {e}")
            return {'names': [], 'categories': [], 'prices': []}
    
    def _infer_category_from_name(self, name: str) -> str:
        """Infere categoria baseada no nome do serviço"""
        name_lower = name.lower()
        
        if any(word in name_lower for word in ['eletric', 'lampada', 'tomada', 'fio', 'chuveiro']):
            return 'eletrica'
        elif any(word in name_lower for word in ['agua', 'encanamento', 'torneira', 'vaso', 'pia']):
            return 'hidraulica'
        elif any(word in name_lower for word in ['pintura', 'tinta', 'parede', 'massa']):
            return 'pintura'
        elif any(word in name_lower for word in ['alvenaria', 'construcao', 'reboco', 'ceramica']):
            return 'construcao'
        elif any(word in name_lower for word in ['madeira', 'porta', 'janela', 'armario']):
            return 'carpintaria'
        elif any(word in name_lower for word in ['jardim', 'poda', 'grama', 'planta']):
            return 'jardinagem'
        elif any(word in name_lower for word in ['limpeza', 'lavagem', 'faxina']):
            return 'limpeza'
        else:
            return 'manutencao'
    
    def _train_category_model(self, names: List[str], categories: List[str]):
        """Treina modelo de classificação de categorias"""
        if not names or not categories:
            print("⚠️ Dados insuficientes para treinar modelo de categorias")
            return
        
        # Vetorização dos nomes
        self.vectorizers['category'] = TfidfVectorizer(max_features=100, stop_words=None)
        X = self.vectorizers['category'].fit_transform(names)
        
        # Codificação das categorias
        self.encoders['category'] = LabelEncoder()
        y = self.encoders['category'].fit_transform(categories)
        
        # Treina o modelo
        self.models['category'] = RandomForestClassifier(n_estimators=50, random_state=42)
        self.models['category'].fit(X, y)
        
        # Calcula acurácia
        y_pred = self.models['category'].predict(X)
        accuracy = accuracy_score(y, y_pred)
        print(f"📊 Acurácia do modelo de categorias: {accuracy:.2f}")
    
    def _train_price_model(self, names: List[str], categories: List[str], prices: List[float]):
        """Treina modelo de regressão de preços"""
        if not names or not prices:
            print("⚠️ Dados insuficientes para treinar modelo de preços")
            return
        
        # Combina nome e categoria para features
        features = [f"{name} {cat}" for name, cat in zip(names, categories)]
        
        # Vetorização
        self.vectorizers['price'] = TfidfVectorizer(max_features=100, stop_words=None)
        X = self.vectorizers['price'].fit_transform(features)
        
        # Treina o modelo
        self.models['price'] = RandomForestRegressor(n_estimators=50, random_state=42)
        self.models['price'].fit(X, prices)
        
        # Calcula erro médio
        y_pred = self.models['price'].predict(X)
        mae = mean_absolute_error(prices, y_pred)
        print(f"📊 Erro médio do modelo de preços: R$ {mae:.2f}")
    
    def _save_models(self):
        """Salva os modelos treinados"""
        os.makedirs('models', exist_ok=True)
        
        if 'price' in self.models:
            with open('models/price_model.pkl', 'wb') as f:
                pickle.dump(self.models['price'], f)
        
        if 'category' in self.models:
            with open('models/category_model.pkl', 'wb') as f:
                pickle.dump(self.models['category'], f)
        
        if 'price' in self.vectorizers:
            with open('models/price_vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizers['price'], f)
        
        if 'category' in self.vectorizers:
            with open('models/category_vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizers['category'], f)
        
        if 'category' in self.encoders:
            with open('models/category_encoder.pkl', 'wb') as f:
                pickle.dump(self.encoders['category'], f)
    
    def _load_models(self):
        """Carrega modelos salvos"""
        try:
            with open('models/price_model.pkl', 'rb') as f:
                self.models['price'] = pickle.load(f)
            
            with open('models/category_model.pkl', 'rb') as f:
                self.models['category'] = pickle.load(f)
            
            with open('models/price_vectorizer.pkl', 'rb') as f:
                self.vectorizers['price'] = pickle.load(f)
            
            with open('models/category_vectorizer.pkl', 'rb') as f:
                self.vectorizers['category'] = pickle.load(f)
            
            with open('models/category_encoder.pkl', 'rb') as f:
                self.encoders['category'] = pickle.load(f)
            
            self.is_trained = True
            print("✅ Modelos carregados com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar modelos: {e}")
            self._train_models()
    
    def predict_category(self, service_name: str) -> str:
        """Prediz a categoria de um serviço"""
        if not self.is_trained or 'category' not in self.models:
            return self._infer_category_from_name(service_name)
        
        try:
            # Vetoriza o nome
            X = self.vectorizers['category'].transform([service_name])
            
            # Prediz
            prediction = self.models['category'].predict(X)[0]
            
            # Verifica se a predição é válida
            if np.isnan(prediction):
                print(f"Predição NaN para '{service_name}', usando inferência")
                return self._infer_category_from_name(service_name)
            
            category = self.encoders['category'].inverse_transform([int(prediction)])[0]
            
            # Verifica se a categoria é válida
            if pd.isna(category) or category == 'nan':
                print(f"Categoria inválida para '{service_name}', usando inferência")
                return self._infer_category_from_name(service_name)
            
            return str(category)
        except Exception as e:
            print(f"Erro na predição de categoria: {e}")
            return self._infer_category_from_name(service_name)
    
    def predict_price(self, service_name: str, category: str = None) -> Dict[str, Any]:
        """Prediz o preço de um serviço"""
        if not category:
            category = self.predict_category(service_name)
        
        # Garante que a categoria é válida
        if not category or category == 'nan' or pd.isna(category):
            category = self._infer_category_from_name(service_name)
        
        if not self.is_trained or 'price' not in self.models:
            return self._get_default_price(service_name, category)
        
        try:
            # Combina nome e categoria
            feature = f"{service_name} {category}"
            X = self.vectorizers['price'].transform([feature])
            
            # Prediz preço
            predicted_price = self.models['price'].predict(X)[0]
            
            # Verifica se o preço é válido
            if np.isnan(predicted_price) or predicted_price <= 0:
                print(f"Preço inválido para '{service_name}', usando preço padrão")
                return self._get_default_price(service_name, category)
            
            # Determina faixa de preço
            price_range = self._determine_price_range(predicted_price)
            
            # Gera variações de preço
            min_price = predicted_price * 0.8
            max_price = predicted_price * 1.2
            
            return {
                "suggested_price": round(float(predicted_price), 2),
                "min_price": round(float(min_price), 2),
                "max_price": round(float(max_price), 2),
                "price_range": price_range,
                "confidence": 0.85,  # Simulado baseado na acurácia
                "reasoning": f"Preço baseado em análise de dados históricos para {category}"
            }
        except Exception as e:
            print(f"Erro na predição de preço: {e}")
            return self._get_default_price(service_name, category)
    
    def _determine_price_range(self, price: float) -> str:
        """Determina a faixa de preço"""
        if price < 100:
            return "Econômico"
        elif price < 300:
            return "Médio"
        else:
            return "Premium"
    
    def _get_default_price(self, service_name: str, category: str) -> Dict[str, Any]:
        """Retorna preço padrão quando modelo não está disponível"""
        # Preços base por categoria
        base_prices = {
            'eletrica': 150,
            'hidraulica': 180,
            'pintura': 20,
            'construcao': 50,
            'carpintaria': 300,
            'jardinagem': 120,
            'limpeza': 15,
            'manutencao': 100
        }
        
        base_price = base_prices.get(category, 100)
        
        return {
            "suggested_price": base_price,
            "min_price": base_price * 0.8,
            "max_price": base_price * 1.2,
            "price_range": self._determine_price_range(base_price),
            "confidence": 0.6,
            "reasoning": f"Preço base estimado para categoria {category}"
        }
    
    def generate_service_description(self, name: str, category: str = None) -> str:
        """Gera descrição do serviço baseada em padrões"""
        if not category:
            category = self.predict_category(name)
        
        # Templates de descrição por categoria
        templates = {
            'eletrica': "Serviço elétrico residencial {} com materiais de qualidade e garantia de segurança",
            'hidraulica': "Serviço hidráulico {} com tubulações e conexões de primeira linha",
            'pintura': "Pintura {} com tintas premium e acabamento profissional",
            'construcao': "Serviço de construção {} com materiais certificados e mão de obra qualificada",
            'carpintaria': "Trabalho em madeira {} com acabamento artesanal e materiais selecionados",
            'jardinagem': "Serviço de jardinagem {} com plantas de qualidade e técnicas especializadas",
            'limpeza': "Serviço de limpeza {} com produtos profissionais e equipamentos adequados",
            'manutencao': "Manutenção {} com diagnóstico preciso e reparo definitivo"
        }
        
        template = templates.get(category, "Serviço residencial {} de alta qualidade")
        return template.format(name.lower())
    
    def generate_quote_title(self, client_name: str, services: List[str]) -> str:
        """Gera título do orçamento"""
        if len(services) == 1:
            return f"Orçamento {client_name} - {services[0]}"
        elif len(services) <= 3:
            return f"Orçamento {client_name} - {', '.join(services)}"
        else:
            return f"Orçamento {client_name} - {len(services)} serviços"
    
    def suggest_quote_notes(self, services: List[str], total_value: float) -> str:
        """Sugere observações para o orçamento"""
        notes = []
        
        # Validade baseada no valor
        if total_value > 1000:
            notes.append("Proposta válida por 15 dias.")
        else:
            notes.append("Proposta válida por 30 dias.")
        
        # Condições de pagamento
        if total_value > 500:
            notes.append("Condições: 50% entrada e 50% na conclusão.")
        else:
            notes.append("Pagamento à vista ou conforme acordado.")
        
        # Garantia baseada nos serviços
        has_installation = any('instalacao' in s.lower() for s in services)
        if has_installation:
            notes.append("Garantia de 6 meses nos serviços executados.")
        else:
            notes.append("Garantia de 3 meses nos serviços executados.")
        
        return " ".join(notes)
    
    def retrain_with_new_data(self):
        """Retreina os modelos com novos dados do Excel"""
        print("🔄 Retreinando modelos com novos dados...")
        self._train_models()
        return True

# Instância global do serviço ML
ml_service = MLService()
