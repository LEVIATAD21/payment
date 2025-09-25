import requests
import time
from src.config.settings import CONVERSION_FEE, COINGECKO_API_URL

# Cache para preços
_price_cache = {'brl': None, 'usd': None, 'timestamp': 0}

def get_bitcoin_price(currency='brl'):
    """Obtém preço do Bitcoin via CoinGecko com cache"""
    if time.time() - _price_cache['timestamp'] < 300:  # Cache 5 min
        return _price_cache[currency]
    
    try:
        url = f"{COINGECKO_API_URL}/simple/price?ids=bitcoin&vs_currencies={currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        price = response.json()['bitcoin'][currency]
        
        # Atualiza cache
        _price_cache[currency] = price
        _price_cache['timestamp'] = time.time()
        
        return price
    except Exception as e:
        # Fallback se API falhar
        return 200000.0 if currency == 'brl' else 50000.0

def convert_fiat_to_btc(amount, currency='brl'):
    """Converte fiat para Bitcoin aplicando taxa"""
    try:
        price = get_bitcoin_price(currency)
        btc = amount / price
        return btc * (1 - CONVERSION_FEE)  # Aplica taxa de conversão
    except Exception as e:
        raise ValueError(f"Erro na conversão: {str(e)}")

def validate_payment_amount(amount):
    """Valida valor do pagamento"""
    from src.config.settings import MIN_AMOUNT, MAX_AMOUNT
    if not (MIN_AMOUNT <= amount <= MAX_AMOUNT):
        raise ValueError(f"Valor inválido: deve ser entre R${MIN_AMOUNT} e R${MAX_AMOUNT}")
    return True

def get_conversion_preview(amount, currency='brl'):
    """Retorna preview da conversão"""
    try:
        price = get_bitcoin_price(currency)
        fee_amount = amount * CONVERSION_FEE
        amount_after_fee = amount - fee_amount
        btc_amount = amount_after_fee / price
        
        return {
            'success': True,
            'original_amount': amount,
            'currency': currency.upper(),
            'btc_price': price,
            'fee_amount': fee_amount,
            'amount_after_fee': amount_after_fee,
            'btc_amount': btc_amount,
            'btc_amount_satoshi': int(btc_amount * 100000000)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def compare_exchanges():
    """Compara preços entre diferentes exchanges"""
    try:
        # Preços de diferentes fontes
        coingecko_price = get_bitcoin_price('usd')
        
        # Simular preços de outras exchanges (em produção, usar APIs reais)
        binance_price = coingecko_price * 0.999  # Binance geralmente tem preços ligeiramente menores
        coinbase_price = coingecko_price * 1.001  # Coinbase geralmente tem preços ligeiramente maiores
        
        return {
            'coingecko': {
                'price': coingecko_price,
                'name': 'CoinGecko',
                'fee': 0.0
            },
            'binance': {
                'price': binance_price,
                'name': 'Binance',
                'fee': 0.1
            },
            'coinbase': {
                'price': coinbase_price,
                'name': 'Coinbase',
                'fee': 0.5
            },
            'best_price': {
                'exchange': 'binance',
                'price': binance_price,
                'savings': coingecko_price - binance_price
            }
        }
    except Exception as e:
        return {
            'error': str(e),
            'coingecko': {'price': 50000, 'name': 'CoinGecko', 'fee': 0.0}
        }