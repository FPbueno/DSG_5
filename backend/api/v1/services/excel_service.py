import pandas as pd
import os
from datetime import datetime
from typing import List, Optional
from ..models import (
    Client, ClientCreate, ClientUpdate,
    Service, ServiceCreate, ServiceUpdate,
    Quote, QuoteCreate, QuoteUpdate,
    QuoteItem, QuoteItemCreate, QuoteItemUpdate
)
from ..core.config import EXCEL_FILE

class ExcelService:
    def __init__(self):
        self.file_path = EXCEL_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Cria o arquivo Excel se não existir"""
        if not os.path.exists(self.file_path):
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                # Aba de Clientes
                clients_df = pd.DataFrame(columns=[
                    'id', 'name', 'created_at', 'updated_at'
                ])
                clients_df.to_excel(writer, sheet_name='clients', index=False)
                
                # Aba de Serviços
                services_df = pd.DataFrame(columns=[
                    'id', 'name', 'unit_price', 'unit', 'created_at', 'updated_at'
                ])
                services_df.to_excel(writer, sheet_name='services', index=False)
                
                # Aba de Orçamentos
                quotes_df = pd.DataFrame(columns=[
                    'id', 'quote_number', 'client_id', 'title', 'description', 
                    'status', 'total', 'created_at', 'updated_at'
                ])
                quotes_df.to_excel(writer, sheet_name='quotes', index=False)
                
                # Aba de Itens dos Orçamentos
                quote_items_df = pd.DataFrame(columns=[
                    'id', 'quote_id', 'service_id', 'quantity', 'unit_price', 
                    'total_price', 'service_name', 'service_unit', 'created_at'
                ])
                quote_items_df.to_excel(writer, sheet_name='quote_items', index=False)
    
    def _read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Lê uma aba específica do Excel"""
        return pd.read_excel(self.file_path, sheet_name=sheet_name)
    
    def _save_sheet(self, df: pd.DataFrame, sheet_name: str):
        """Salva dados em uma aba específica do Excel"""
        with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def _get_next_id(self, sheet_name: str) -> int:
        """Gera próximo ID para uma aba"""
        df = self._read_sheet(sheet_name)
        return df['id'].max() + 1 if not df.empty else 1
    
    def _generate_quote_number(self) -> str:
        """Gera número do orçamento"""
        year = datetime.now().year
        month = datetime.now().month
        quotes_df = self._read_sheet('quotes')
        count = len(quotes_df[quotes_df['quote_number'].str.startswith(f"ORC{year}{month:02d}")])
        return f"ORC{year}{month:02d}{count + 1:03d}"

    # MÉTODOS PARA CLIENTES
    def get_all_clients(self) -> List[Client]:
        """Retorna todos os clientes"""
        df = self._read_sheet('clients')
        clients = []
        for _, row in df.iterrows():
            clients.append(Client(
                id=int(row['id']),
                name=row['name'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            ))
        return clients

    def create_client(self, client: ClientCreate) -> Client:
        """Cria novo cliente"""
        df = self._read_sheet('clients')
        new_id = self._get_next_id('clients')
        now = datetime.now().isoformat()
        
        new_row = pd.DataFrame([{
            'id': new_id,
            'name': client.name,
            'created_at': now,
            'updated_at': now
        }])
        
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_sheet(df, 'clients')
        
        return Client(
            id=new_id,
            name=client.name,
            created_at=datetime.fromisoformat(now),
            updated_at=datetime.fromisoformat(now)
        )

    # MÉTODOS PARA SERVIÇOS
    def get_all_services(self) -> List[Service]:
        """Retorna todos os serviços"""
        df = self._read_sheet('services')
        services = []
        for _, row in df.iterrows():
            services.append(Service(
                id=int(row['id']),
                name=row['name'],
                unit_price=float(row['unit_price']),
                unit=row['unit'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            ))
        return services

    def create_service(self, service: ServiceCreate) -> Service:
        """Cria novo serviço"""
        df = self._read_sheet('services')
        new_id = self._get_next_id('services')
        now = datetime.now().isoformat()
        
        new_row = pd.DataFrame([{
            'id': new_id,
            'name': service.name,
            'unit_price': service.unit_price,
            'unit': service.unit,
            'created_at': now,
            'updated_at': now
        }])
        
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_sheet(df, 'services')
        
        return Service(
            id=new_id,
            name=service.name,
            unit_price=service.unit_price,
            unit=service.unit,
            created_at=datetime.fromisoformat(now),
            updated_at=datetime.fromisoformat(now)
        )

    # MÉTODOS PARA ORÇAMENTOS
    def get_all_quotes(self) -> List[Quote]:
        """Retorna todos os orçamentos"""
        quotes_df = self._read_sheet('quotes')
        clients_df = self._read_sheet('clients')
        quote_items_df = self._read_sheet('quote_items')
        services_df = self._read_sheet('services')
        
        quotes = []
        for _, quote_row in quotes_df.iterrows():
            # Busca cliente
            client_row = clients_df[clients_df['id'] == quote_row['client_id']].iloc[0]
            client = Client(
                id=int(client_row['id']),
                name=client_row['name'],
                created_at=datetime.fromisoformat(client_row['created_at']),
                updated_at=datetime.fromisoformat(client_row['updated_at'])
            )
            
            # Busca itens do orçamento
            items = []
            quote_items = quote_items_df[quote_items_df['quote_id'] == quote_row['id']]
            for _, item_row in quote_items.iterrows():
                service_row = services_df[services_df['id'] == item_row['service_id']].iloc[0]
                items.append(QuoteItem(
                    id=int(item_row['id']),
                    service_id=int(item_row['service_id']),
                    quantity=float(item_row['quantity']),
                    unit_price=float(item_row['unit_price']),
                    total_price=float(item_row['total_price']),
                    service_name=service_row['name'],
                    service_unit=service_row['unit']
                ))
            
            quotes.append(Quote(
                id=int(quote_row['id']),
                quote_number=quote_row['quote_number'],
                client_id=int(quote_row['client_id']),
                title=quote_row['title'],
                description=quote_row['description'] if pd.notna(quote_row['description']) else None,
                status=quote_row['status'],
                total=float(quote_row['total']),
                created_at=datetime.fromisoformat(quote_row['created_at']),
                updated_at=datetime.fromisoformat(quote_row['updated_at']),
                client=client,
                items=items
            ))
        
        return quotes

    def create_quote(self, quote: QuoteCreate) -> Quote:
        """Cria novo orçamento"""
        quotes_df = self._read_sheet('quotes')
        quote_items_df = self._read_sheet('quote_items')
        
        new_id = self._get_next_id('quotes')
        quote_number = self._generate_quote_number()
        now = datetime.now().isoformat()
        
        # Calcula total
        total = sum(item.quantity * item.unit_price for item in quote.items)
        
        # Cria orçamento
        new_quote_row = pd.DataFrame([{
            'id': new_id,
            'quote_number': quote_number,
            'client_id': quote.client_id,
            'title': quote.title,
            'description': quote.description,
            'status': quote.status,
            'total': total,
            'created_at': now,
            'updated_at': now
        }])
        
        quotes_df = pd.concat([quotes_df, new_quote_row], ignore_index=True)
        self._save_sheet(quotes_df, 'quotes')
        
        # Cria itens do orçamento
        if quote.items:
            new_items = []
            for item in quote.items:
                item_id = self._get_next_id('quote_items')
                item_total = item.quantity * item.unit_price
                
                # Busca dados do serviço
                services_df = self._read_sheet('services')
                service_row = services_df[services_df['id'] == item.service_id].iloc[0]
                
                new_items.append({
                    'id': item_id,
                    'quote_id': new_id,
                    'service_id': item.service_id,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'total_price': item_total,
                    'service_name': service_row['name'],
                    'service_unit': service_row['unit'],
                    'created_at': now
                })
            
            quote_items_df = pd.concat([quote_items_df, pd.DataFrame(new_items)], ignore_index=True)
            self._save_sheet(quote_items_df, 'quote_items')
        
        # Retorna orçamento criado
        return self.get_quote_by_id(new_id)

    def get_quote_by_id(self, quote_id: int) -> Optional[Quote]:
        """Retorna orçamento por ID"""
        quotes = self.get_all_quotes()
        for quote in quotes:
            if quote.id == quote_id:
                return quote
        return None

    def update_quote(self, quote_id: int, quote_update: QuoteUpdate) -> Optional[Quote]:
        """Atualiza um orçamento existente"""
        try:
            # Lê dados atuais
            quotes_df = self._read_sheet('quotes')
            quote_items_df = self._read_sheet('quote_items')
            
            # Verifica se o orçamento existe
            quote_idx = quotes_df[quotes_df['id'] == quote_id].index
            if quote_idx.empty:
                return None
            
            # Atualiza campos do orçamento
            update_data = quote_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if field != 'items':  # items é tratado separadamente
                    quotes_df.loc[quote_idx[0], field] = value
            
            # Atualiza itens se fornecidos
            if hasattr(quote_update, 'items') and quote_update.items is not None:
                # Remove itens antigos
                quote_items_df = quote_items_df[quote_items_df['quote_id'] != quote_id]
                
                # Adiciona novos itens
                if quote_update.items:
                    new_items = []
                    for item in quote_update.items:
                        item_id = self._get_next_id('quote_items')
                        item_total = item.quantity * item.unit_price
                        
                        # Busca dados do serviço
                        services_df = self._read_sheet('services')
                        service_row = services_df[services_df['id'] == item.service_id].iloc[0]
                        
                        new_items.append({
                            'id': item_id,
                            'quote_id': quote_id,
                            'service_id': item.service_id,
                            'quantity': item.quantity,
                            'unit_price': item.unit_price,
                            'total_price': item_total,
                            'service_name': service_row['name'],
                            'service_unit': service_row['unit'],
                            'created_at': datetime.now().isoformat()
                        })
                    
                    quote_items_df = pd.concat([quote_items_df, pd.DataFrame(new_items)], ignore_index=True)
                    self._save_sheet(quote_items_df, 'quote_items')
                
                # Recalcula total
                items = quote_items_df[quote_items_df['quote_id'] == quote_id]
                total = items['total_price'].sum() if not items.empty else 0
                quotes_df.loc[quote_idx[0], 'total'] = total
            
            # Atualiza timestamp
            quotes_df.loc[quote_idx[0], 'updated_at'] = datetime.now().isoformat()
            
            # Salva alterações
            self._save_sheet(quotes_df, 'quotes')
            
            # Retorna orçamento atualizado
            return self.get_quote_by_id(quote_id)
            
        except Exception as e:
            print(f"Erro ao atualizar orçamento: {e}")
            return None

    def delete_quote(self, quote_id: int) -> bool:
        """Exclui um orçamento"""
        try:
            # Lê dados atuais
            quotes_df = self._read_sheet('quotes')
            quote_items_df = self._read_sheet('quote_items')
            
            # Verifica se o orçamento existe
            if quote_id not in quotes_df['id'].values:
                return False
            
            # Remove orçamento e seus itens
            quotes_df = quotes_df[quotes_df['id'] != quote_id]
            quote_items_df = quote_items_df[quote_items_df['quote_id'] != quote_id]
            
            # Salva alterações
            self._save_sheet(quotes_df, 'quotes')
            self._save_sheet(quote_items_df, 'quote_items')
            
            return True
            
        except Exception as e:
            print(f"Erro ao excluir orçamento: {e}")
            return False

# Instância global do serviço
excel_service = ExcelService()
