"""
Integração Dropshipping - Sistema Hacker
Conecta com Shopify e converte vendas para Bitcoin automaticamente
"""

import requests
import time
import random
from src.config.settings import DEBUG

class DropshipIntegration:
    """Sistema de integração com dropshipping"""
    
    def __init__(self):
        # Configurações Shopify (configure suas credenciais)
        self.shopify_config = {
            'shop_domain': 'tua-loja.myshopify.com',
            'access_token': 'seu_token_shopify_aqui',
            'api_version': '2025-01'
        }
        
        # Produtos dropship disponíveis
        self.dropship_products = [
            {
                'id': 'prod_1',
                'name': 'Fone Bluetooth Premium',
                'price': 89.90,
                'category': 'Eletrônicos',
                'supplier': 'AliExpress',
                'profit_margin': 0.4
            },
            {
                'id': 'prod_2', 
                'name': 'Smartwatch Fitness',
                'price': 199.90,
                'category': 'Wearables',
                'supplier': 'AliExpress',
                'profit_margin': 0.5
            },
            {
                'id': 'prod_3',
                'name': 'Câmera 4K Portátil',
                'price': 299.90,
                'category': 'Fotografia',
                'supplier': 'AliExpress',
                'profit_margin': 0.6
            },
            {
                'id': 'prod_4',
                'name': 'Kit Ferramentas Profissional',
                'price': 149.90,
                'category': 'Ferramentas',
                'supplier': 'AliExpress',
                'profit_margin': 0.7
            },
            {
                'id': 'prod_5',
                'name': 'Suplemento Fitness Premium',
                'price': 79.90,
                'category': 'Saúde',
                'supplier': 'AliExpress',
                'profit_margin': 0.8
            }
        ]
        
        # Histórico de vendas
        self.sales_history = []
    
    def get_shopify_orders(self, limit=50):
        """Busca pedidos do Shopify"""
        try:
            url = f"https://{self.shopify_config['shop_domain']}/admin/api/{self.shopify_config['api_version']}/orders.json"
            headers = {
                'X-Shopify-Access-Token': self.shopify_config['access_token'],
                'Content-Type': 'application/json'
            }
            params = {
                'limit': limit,
                'status': 'any',
                'created_at_min': self._get_last_sync_time()
            }
            
            if DEBUG:
                print(f"🛍️ Buscando pedidos Shopify...")
                # Simula resposta (em produção, use requests.get)
                return self._simulate_shopify_orders()
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"❌ Erro ao buscar pedidos Shopify: {e}")
            return {'orders': []}
    
    def _simulate_shopify_orders(self):
        """Simula pedidos do Shopify para desenvolvimento"""
        orders = []
        for i in range(random.randint(1, 5)):
            product = random.choice(self.dropship_products)
            order = {
                'id': f'order_{int(time.time())}_{i}',
                'email': f'cliente{i}@email.com',
                'total_price': str(product['price']),
                'currency': 'BRL',
                'line_items': [{
                    'title': product['name'],
                    'price': str(product['price']),
                    'quantity': 1
                }],
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S-03:00'),
                'financial_status': 'paid'
            }
            orders.append(order)
        
        return {'orders': orders}
    
    def process_dropship_order(self, order_data):
        """Processa pedido dropship e converte para Bitcoin"""
        try:
            order_id = order_data['id']
            email = order_data['email']
            total_price = float(order_data['total_price'])
            
            # Calcula lucro do dropship
            product = self._find_product_by_price(total_price)
            if product:
                profit = total_price * product['profit_margin']
                btc_amount = self._convert_to_btc(profit)
            else:
                # Fallback: 30% do valor como lucro
                profit = total_price * 0.3
                btc_amount = self._convert_to_btc(profit)
            
            # Registra venda
            sale_record = {
                'order_id': order_id,
                'email': email,
                'total_price': total_price,
                'profit': profit,
                'btc_amount': btc_amount,
                'timestamp': time.time(),
                'status': 'processed'
            }
            self.sales_history.append(sale_record)
            
            if DEBUG:
                print(f"🛍️ Pedido dropship processado: {order_id}")
                print(f"💰 Lucro: R${profit:.2f} = {btc_amount:.8f} BTC")
            
            return {
                'success': True,
                'order_id': order_id,
                'profit': profit,
                'btc_amount': btc_amount,
                'conversion_rate': btc_amount / total_price
            }
            
        except Exception as e:
            print(f"❌ Erro ao processar pedido dropship: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _find_product_by_price(self, price):
        """Encontra produto pelo preço"""
        for product in self.dropship_products:
            if abs(product['price'] - price) < 0.01:
                return product
        return None
    
    def _convert_to_btc(self, amount_brl):
        """Converte valor em reais para Bitcoin"""
        try:
            # Simula preço do Bitcoin (em produção, use API real)
            btc_price = 80000  # R$ 80.000 por BTC
            return amount_brl / btc_price
        except Exception as e:
            print(f"❌ Erro na conversão BTC: {e}")
            return 0
    
    def _get_last_sync_time(self):
        """Retorna timestamp da última sincronização"""
        if self.sales_history:
            last_sale = max(self.sales_history, key=lambda x: x['timestamp'])
            return time.strftime('%Y-%m-%dT%H:%M:%S-03:00', time.localtime(last_sale['timestamp']))
        else:
            # Últimas 24 horas
            return time.strftime('%Y-%m-%dT%H:%M:%S-03:00', time.localtime(time.time() - 86400))
    
    def get_dropship_products(self):
        """Retorna lista de produtos dropship"""
        return self.dropship_products
    
    def get_sales_stats(self):
        """Retorna estatísticas de vendas"""
        try:
            if not self.sales_history:
                return {
                    'total_orders': 0,
                    'total_revenue': 0,
                    'total_profit': 0,
                    'total_btc': 0,
                    'avg_profit_margin': 0
                }
            
            total_orders = len(self.sales_history)
            total_revenue = sum(sale['total_price'] for sale in self.sales_history)
            total_profit = sum(sale['profit'] for sale in self.sales_history)
            total_btc = sum(sale['btc_amount'] for sale in self.sales_history)
            avg_profit_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
            
            return {
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'total_profit': total_profit,
                'total_btc': total_btc,
                'avg_profit_margin': avg_profit_margin
            }
            
        except Exception as e:
            print(f"❌ Erro nas estatísticas: {e}")
            return {
                'total_orders': 0,
                'total_revenue': 0,
                'total_profit': 0,
                'total_btc': 0,
                'avg_profit_margin': 0
            }
    
    def create_dropship_upsell(self, customer_email, customer_name, last_purchase_amount):
        """Cria upsell de produto dropship"""
        try:
            # Seleciona produto baseado no valor da última compra
            if last_purchase_amount < 100:
                suggested_products = [p for p in self.dropship_products if p['price'] < 100]
            elif last_purchase_amount < 300:
                suggested_products = [p for p in self.dropship_products if 100 <= p['price'] < 300]
            else:
                suggested_products = [p for p in self.dropship_products if p['price'] >= 300]
            
            if not suggested_products:
                suggested_products = self.dropship_products
            
            product = random.choice(suggested_products)
            
            upsell_data = {
                'customer_email': customer_email,
                'customer_name': customer_name,
                'suggested_product': product,
                'upsell_price': product['price'],
                'expected_profit': product['price'] * product['profit_margin'],
                'btc_potential': self._convert_to_btc(product['price'] * product['profit_margin'])
            }
            
            if DEBUG:
                print(f"🛍️ Upsell dropship criado para {customer_email}: {product['name']}")
            
            return upsell_data
            
        except Exception as e:
            print(f"❌ Erro no upsell dropship: {e}")
            return None
    
    def sync_orders_automatically(self):
        """Sincroniza pedidos automaticamente"""
        try:
            orders = self.get_shopify_orders()
            processed_count = 0
            
            for order in orders.get('orders', []):
                if order['financial_status'] == 'paid':
                    result = self.process_dropship_order(order)
                    if result['success']:
                        processed_count += 1
            
            if DEBUG:
                print(f"🔄 Sincronização automática: {processed_count} pedidos processados")
            
            return {
                'success': True,
                'processed_orders': processed_count,
                'total_orders': len(orders.get('orders', []))
            }
            
        except Exception as e:
            print(f"❌ Erro na sincronização automática: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Instância global do dropship
dropship_integration = DropshipIntegration()

# Funções de conveniência
def process_dropship_order(order_data):
    """Processa pedido dropship"""
    return dropship_integration.process_dropship_order(order_data)

def get_dropship_products():
    """Retorna produtos dropship"""
    return dropship_integration.get_dropship_products()

def get_sales_stats():
    """Retorna estatísticas de vendas"""
    return dropship_integration.get_sales_stats()

def create_dropship_upsell(customer_email, customer_name, last_purchase_amount):
    """Cria upsell dropship"""
    return dropship_integration.create_dropship_upsell(customer_email, customer_name, last_purchase_amount)

def sync_orders_automatically():
    """Sincroniza pedidos automaticamente"""
    return dropship_integration.sync_orders_automatically()

