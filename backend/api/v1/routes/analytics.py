from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..services.excel_service import excel_service

router = APIRouter()

@router.get("/analytics/overview")
async def get_analytics_overview():
    """Retorna visão geral dos dados para analytics"""
    try:
        # Busca todos os dados
        quotes = excel_service.get_all_quotes()
        services = excel_service.get_all_services()
        clients = excel_service.get_all_clients()
        
        # Estatísticas básicas
        total_quotes = len(quotes)
        total_services = len(services)
        total_clients = len(clients)
        
        # Valores financeiros
        total_revenue = sum(quote.total for quote in quotes)
        avg_quote_value = total_revenue / total_quotes if total_quotes > 0 else 0
        
        # Status dos orçamentos
        status_counts = {}
        for quote in quotes:
            status = quote.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Serviços mais populares
        service_usage = {}
        for quote in quotes:
            for item in quote.items:
                service_name = item.service_name
                service_usage[service_name] = service_usage.get(service_name, 0) + 1
        
        # Top 5 serviços mais usados
        top_services = sorted(service_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Análise temporal (últimos 30 dias)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_quotes = [q for q in quotes if q.created_at >= thirty_days_ago]
        recent_revenue = sum(quote.total for quote in recent_quotes)
        
        # Análise por mês (últimos 6 meses)
        monthly_data = {}
        for quote in quotes:
            month_key = quote.created_at.strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"count": 0, "revenue": 0}
            monthly_data[month_key]["count"] += 1
            monthly_data[month_key]["revenue"] += quote.total
        
        # Ordena por mês
        sorted_monthly = sorted(monthly_data.items())[-6:]  # Últimos 6 meses
        
        return {
            "overview": {
                "total_quotes": total_quotes,
                "total_services": total_services,
                "total_clients": total_clients,
                "total_revenue": total_revenue,
                "avg_quote_value": avg_quote_value,
                "recent_revenue_30d": recent_revenue
            },
            "status_distribution": status_counts,
            "top_services": top_services,
            "monthly_trends": [
                {
                    "month": month,
                    "quotes_count": data["count"],
                    "revenue": data["revenue"]
                }
                for month, data in sorted_monthly
            ]
        }
    except Exception as e:
        return {"error": f"Erro ao gerar analytics: {str(e)}"}

@router.get("/analytics/services")
async def get_services_analytics():
    """Analytics específicos de serviços"""
    try:
        services = excel_service.get_all_services()
        quotes = excel_service.get_all_quotes()
        
        # Análise de preços por serviço
        service_analytics = []
        for service in services:
            # Busca itens que usam este serviço
            service_items = []
            for quote in quotes:
                for item in quote.items:
                    if item.service_id == service.id:
                        service_items.append(item)
            
            if service_items:
                prices = [item.unit_price for item in service_items]
                quantities = [item.quantity for item in service_items]
                total_usage = sum(quantities)
                
                service_analytics.append({
                    "service_id": service.id,
                    "service_name": service.name,
                    "unit": service.unit,
                    "base_price": service.unit_price,
                    "avg_price_used": sum(prices) / len(prices),
                    "min_price": min(prices),
                    "max_price": max(prices),
                    "total_usage": total_usage,
                    "times_used": len(service_items)
                })
        
        # Ordena por uso
        service_analytics.sort(key=lambda x: x["times_used"], reverse=True)
        
        return {
            "services": service_analytics,
            "total_services": len(services),
            "active_services": len([s for s in service_analytics if s["times_used"] > 0])
        }
    except Exception as e:
        return {"error": f"Erro ao gerar analytics de serviços: {str(e)}"}

@router.get("/analytics/clients")
async def get_clients_analytics():
    """Analytics específicos de clientes"""
    try:
        clients = excel_service.get_all_clients()
        quotes = excel_service.get_all_quotes()
        
        # Análise por cliente
        client_analytics = []
        for client in clients:
            client_quotes = [q for q in quotes if q.client_id == client.id]
            
            if client_quotes:
                total_spent = sum(quote.total for quote in client_quotes)
                avg_quote_value = total_spent / len(client_quotes)
                
                client_analytics.append({
                    "client_id": client.id,
                    "client_name": client.name,
                    "quotes_count": len(client_quotes),
                    "total_spent": total_spent,
                    "avg_quote_value": avg_quote_value,
                    "last_quote_date": max(quote.created_at for quote in client_quotes).isoformat()
                })
        
        # Ordena por valor total gasto
        client_analytics.sort(key=lambda x: x["total_spent"], reverse=True)
        
        return {
            "clients": client_analytics,
            "total_clients": len(clients),
            "active_clients": len(client_analytics)
        }
    except Exception as e:
        return {"error": f"Erro ao gerar analytics de clientes: {str(e)}"}
