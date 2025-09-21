"""
Integração Binance API - Conversão BTC com Taxas Menores
Sistema hacker para reduzir custos de conversão
"""

import requests
import hmac
import hashlib
import time
import json
from urllib.parse import urlencode
from src.config.settings import DEBUG

class BinanceHandler:
    """Handler para integração com Binance API"""
    
    def __init__(self):
        # Configure suas chaves Binance no .env
        self.api_key = None  # Será carregado do .env
        self.secret_key = None  # Será carregado do .env
        self.base_url = 'https://api.binance.com'
        self.testnet_url = 'https://testnet.binance.vision'
        self.use_testnet = True  # Use testnet para desenvolvimento
        
        # Taxas Binance (menores que BitPay)
        self.trading_fee = 0.001  # 0.1% por trade
        self.withdrawal_fee = 0.0005  # 0.0005 BTC por saque
        
        # Cache de preços
        self.price_cache = {}
        self.cache_timestamp = 0
        self.cache_duration = 60  # 1 minuto
    
    def load_credentials(self):
        """Carrega credenciais do .env"""
        try:
            from src.config.settings import BINANCE_API_KEY, BINANCE_SECRET_KEY
            self.api_key = BINANCE_API_KEY
            self.secret_key = BINANCE_SECRET_KEY
            
            if not self.api_key or not self.secret_key:
                if DEBUG:
                    print("⚠️ Chaves Binance não configuradas - usando modo simulação")
                return False
            
            return True
            
        except ImportError:
            if DEBUG:
                print("⚠️ Chaves Binance não encontradas no .env")
            return False
    
    def create_signature(self, query_string):
        """Cria assinatura HMAC para autenticação"""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def get_timestamp(self):
        """Retorna timestamp atual em milissegundos"""
        return int(time.time() * 1000)
    
    def make_request(self, endpoint, params=None, method='GET'):
        """Faz requisição autenticada para Binance"""
        try:
            if not self.load_credentials():
                return self._simulate_response(endpoint, params)
            
            url = f"{self.testnet_url if self.use_testnet else self.base_url}{endpoint}"
            
            if params is None:
                params = {}
            
            # Adiciona timestamp
            params['timestamp'] = self.get_timestamp()
            
            # Cria query string
            query_string = urlencode(params)
            
            # Cria assinatura
            signature = self.create_signature(query_string)
            params['signature'] = signature
            
            # Headers
            headers = {
                'X-MBX-APIKEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            # Faz requisição
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            else:
                response = requests.post(url, data=params, headers=headers, timeout=10)
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na requisição Binance: {e}")
            return self._simulate_response(endpoint, params)
    
    def _simulate_response(self, endpoint, params):
        """Simula resposta para desenvolvimento"""
        if 'ticker/price' in endpoint:
            return {'symbol': 'BTCBRL', 'price': '400000.00'}
        elif 'account' in endpoint:
            return {'accountType': 'SPOT', 'balances': []}
        else:
            return {'success': True, 'data': 'simulated'}
    
    def get_bitcoin_price(self, currency='BRL'):
        """Obtém preço atual do Bitcoin"""
        try:
            # Verifica cache
            cache_key = f"btc_{currency.lower()}"
            if (time.time() - self.cache_timestamp) < self.cache_duration:
                if cache_key in self.price_cache:
                    return self.price_cache[cache_key]
            
            # Faz requisição
            symbol = f"BTC{currency.upper()}"
            response = self.make_request('/api/v3/ticker/price', {'symbol': symbol})
            
            if 'price' in response:
                price = float(response['price'])
                self.price_cache[cache_key] = price
                self.cache_timestamp = time.time()
                
                if DEBUG:
                    print(f"💰 Preço BTC via Binance: {currency} {price:,.2f}")
                
                return price
            else:
                raise Exception("Preço não encontrado na resposta")
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao obter preço BTC: {e}")
            # Fallback para preço simulado
            return 400000.0 if currency.upper() == 'BRL' else 80000.0
    
    def convert_fiat_to_btc(self, amount, currency='BRL'):
        """Converte fiat para Bitcoin via Binance"""
        try:
            # Obtém preço atual
            btc_price = self.get_bitcoin_price(currency)
            
            # Calcula quantidade de BTC
            btc_amount = amount / btc_price
            
            # Aplica taxa de trading
            btc_amount_after_fee = btc_amount * (1 - self.trading_fee)
            
            if DEBUG:
                print(f"🔄 Conversão via Binance: {currency} {amount:,.2f} = {btc_amount_after_fee:.8f} BTC")
            
            return {
                'success': True,
                'btc_amount': btc_amount_after_fee,
                'btc_price': btc_price,
                'trading_fee': self.trading_fee,
                'fee_amount': btc_amount * self.trading_fee,
                'exchange': 'binance'
            }
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na conversão Binance: {e}")
            return {
                'success': False,
                'error': str(e),
                'exchange': 'binance'
            }
    
    def get_account_balance(self):
        """Obtém saldo da conta Binance"""
        try:
            response = self.make_request('/api/v3/account')
            
            if 'balances' in response:
                btc_balance = 0
                for balance in response['balances']:
                    if balance['asset'] == 'BTC':
                        btc_balance = float(balance['free'])
                        break
                
                return {
                    'success': True,
                    'btc_balance': btc_balance,
                    'balances': response['balances']
                }
            else:
                raise Exception("Saldo não encontrado")
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao obter saldo: {e}")
            return {
                'success': False,
                'error': str(e),
                'btc_balance': 0
            }
    
    def create_buy_order(self, amount, currency='BRL'):
        """Cria ordem de compra de Bitcoin"""
        try:
            # Obtém preço atual
            btc_price = self.get_bitcoin_price(currency)
            
            # Calcula quantidade de BTC
            btc_quantity = amount / btc_price
            
            # Parâmetros da ordem
            params = {
                'symbol': f'BTC{currency.upper()}',
                'side': 'BUY',
                'type': 'MARKET',
                'quantity': f"{btc_quantity:.8f}"
            }
            
            response = self.make_request('/api/v3/order', params, 'POST')
            
            if 'orderId' in response:
                if DEBUG:
                    print(f"✅ Ordem de compra criada: {response['orderId']}")
                
                return {
                    'success': True,
                    'order_id': response['orderId'],
                    'btc_quantity': btc_quantity,
                    'btc_price': btc_price
                }
            else:
                raise Exception("Ordem não criada")
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao criar ordem: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_trading_fees(self):
        """Obtém taxas de trading"""
        return {
            'trading_fee': self.trading_fee,
            'withdrawal_fee': self.withdrawal_fee,
            'total_fee_percent': self.trading_fee * 100
        }
    
    def compare_with_bitpay(self, amount, currency='BRL'):
        """Compara taxas Binance vs BitPay"""
        try:
            # Taxa BitPay (1%)
            bitpay_fee = 0.01
            bitpay_btc = amount / 400000 * (1 - bitpay_fee)  # Preço simulado
            
            # Taxa Binance (0.1%)
            binance_btc = self.convert_fiat_to_btc(amount, currency)
            
            if binance_btc['success']:
                savings = bitpay_btc - binance_btc['btc_amount']
                savings_percent = (savings / bitpay_btc) * 100
                
                return {
                    'bitpay_btc': bitpay_btc,
                    'binance_btc': binance_btc['btc_amount'],
                    'savings': savings,
                    'savings_percent': savings_percent,
                    'better_exchange': 'binance' if savings > 0 else 'bitpay'
                }
            else:
                return {
                    'error': 'Erro na comparação',
                    'bitpay_btc': bitpay_btc
                }
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na comparação: {e}")
            return {'error': str(e)}

# Instância global do handler
binance_handler = BinanceHandler()

# Funções de conveniência
def get_bitcoin_price_binance(currency='BRL'):
    """Obtém preço BTC via Binance"""
    return binance_handler.get_bitcoin_price(currency)

def convert_fiat_to_btc_binance(amount, currency='BRL'):
    """Converte fiat para BTC via Binance"""
    return binance_handler.convert_fiat_to_btc(amount, currency)

def get_account_balance_binance():
    """Obtém saldo da conta Binance"""
    return binance_handler.get_account_balance()

def compare_exchanges(amount, currency='BRL'):
    """Compara Binance vs BitPay"""
    return binance_handler.compare_with_bitpay(amount, currency)
