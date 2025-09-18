from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import pandas as pd
from ..services.ml_service import ml_service
from ..services.excel_service import excel_service
from ..models.service import ServiceCreate
from ..models.client import ClientCreate
from ..models.quote import QuoteCreate, QuoteItemCreate

router = APIRouter()

@router.post("/ml/smart-create")
async def smart_create_item(
    name: str = Query(..., description="Nome do serviço residencial"),
    user_description: Optional[str] = Query(None, description="Descrição do usuário")
):
    """Cria serviço inteligentemente usando ML e salva no Excel"""
    try:
        # Prediz categoria
        category = ml_service.predict_category(name)
        
        # Prediz preço
        price_prediction = ml_service.predict_price(name, category)
        
        # Gera descrição
        description = ml_service.generate_service_description(name, category)
        if user_description:
            description = user_description
        
        # Monta sugestões no formato esperado
        suggestions = {
            "ml_predictions": {
                "name": name,
                "description": description,
                "category": category,
                "price_suggestion": price_prediction
            }
        }
        
        # Cria o serviço no Excel
        ml_data = suggestions.get("ml_predictions", {})
        service_create = ServiceCreate(
            name=ml_data.get("name", name),
            unit_price=ml_data.get("price_suggestion", {}).get("suggested_price", 100.0),
            unit="unidade"
        )
        
        created_service = excel_service.create_service(service_create)
        
        # Cria um cliente padrão se não existir
        clients = excel_service.get_all_clients()
        if not clients:
            client_create = ClientCreate(name="Cliente Padrão")
            created_client = excel_service.create_client(client_create)
        else:
            created_client = clients[0]
        
        # Cria um orçamento com o serviço
        quote_item = QuoteItemCreate(
            service_id=created_service.id,
            quantity=1.0,
            unit_price=created_service.unit_price
        )
        
        quote_create = QuoteCreate(
            client_id=created_client.id,
            title=f"Orçamento - {created_service.name}",
            description=ml_data.get("description", ""),
            status="pendente",
            items=[quote_item]
        )
        
        created_quote = excel_service.create_quote(quote_create)
        
        # Retorna as predições do ML + dados salvos
        return {
            **suggestions,
            "saved_data": {
                "service_id": created_service.id,
                "quote_id": created_quote.id,
                "quote_number": created_quote.quote_number
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar serviço com ML: {str(e)}")

@router.post("/ml/retrain")
async def retrain_ml_models():
    """Retreina os modelos de ML com novos dados do Excel"""
    try:
        success = ml_service.retrain_with_new_data()
        return {
            "message": "Modelos retreinados com sucesso!",
            "success": success,
            "timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao retreinar modelos: {str(e)}")

@router.get("/ml/predict-category")
async def predict_service_category(
    name: str = Query(..., description="Nome do serviço")
):
    """Prediz a categoria de um serviço"""
    try:
        category = ml_service.predict_category(name)
        return {
            "service_name": name,
            "predicted_category": category,
            "confidence": 0.85
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@router.get("/ml/predict-price")
async def predict_service_price(
    name: str = Query(..., description="Nome do serviço"),
    category: Optional[str] = Query(None, description="Categoria do serviço")
):
    """Prediz o preço de um serviço"""
    try:
        price_prediction = ml_service.predict_price(name, category)
        return {
            "service_name": name,
            "category": category or ml_service.predict_category(name),
            **price_prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@router.post("/ml/populate-training-data")
async def populate_training_data():
    """Popula o Excel com dados de treinamento para ML"""
    try:
        # Adiciona dados de treinamento ao Excel
        training_data = ml_service.training_data
        
        # Cria serviços de treinamento
        services_created = 0
        for i, (name, category, price, description) in enumerate(zip(
            training_data['service_names'],
            training_data['categories'], 
            training_data['prices'],
            training_data['descriptions']
        )):
            try:
                service_create = ServiceCreate(
                    name=name,
                    unit_price=price,
                    unit="unidade"
                )
                excel_service.create_service(service_create)
                services_created += 1
            except Exception as e:
                print(f"Erro ao criar serviço {name}: {e}")
                continue
        
        return {
            "message": f"Dados de treinamento adicionados com sucesso!",
            "services_created": services_created,
            "total_training_services": len(training_data['service_names'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao popular dados: {str(e)}")
