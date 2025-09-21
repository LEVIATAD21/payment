import requests
import hashlib
import ecdsa
import base64
from src.config.settings import BITPAY_API_TOKEN, BITPAY_PRIVATE_KEY_HEX, BITPAY_PUBLIC_KEY_HEX, BITCOIN_WALLET_ADDRESS, BITPAY_API_URL

# Validação de chaves ECDSA
def validate_hex_key(key, length=64):
    """Valida se a chave é hexadecimal com o tamanho correto"""
    if not key or len(key) != length:
        return False
    try:
        int(key, 16)
        return True
    except ValueError:
        return False

# Configuração das chaves ECDSA com fallback
if BITPAY_PRIVATE_KEY_HEX and validate_hex_key(BITPAY_PRIVATE_KEY_HEX):
    try:
        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(BITPAY_PRIVATE_KEY_HEX), curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        BITPAY_ENABLED = True
    except Exception as e:
        print(f"⚠️ Erro ao configurar chaves BitPay: {e}")
        BITPAY_ENABLED = False
        private_key = None
        public_key = None
else:
    print("⚠️ BitPay não configurado - modo de desenvolvimento")
    BITPAY_ENABLED = False
    private_key = None
    public_key = None

def sign_request(url, payload):
    """Cria assinatura ECDSA para BitPay"""
    if not BITPAY_ENABLED or not private_key:
        return "development_mode"
    
    message = url + str(payload)
    signature = private_key.sign(message.encode())
    return base64.b64encode(signature).decode()

def create_invoice(price, currency='BRL'):
    """Cria fatura BitPay"""
    if not BITPAY_ENABLED:
        # Modo de desenvolvimento - simula fatura
        return {
            'data': {
                'id': f'invoice_dev_{int(time.time())}',
                'url': 'https://bitpay.com/invoice/dev',
                'status': 'new'
            }
        }
    
    url = f'{BITPAY_API_URL}/invoices'
    headers = {
        'Content-Type': 'application/json',
        'X-Accept-Version': '2.0.0',
        'X-Identity': BITPAY_PUBLIC_KEY_HEX,
        'X-Signature': sign_request(url, {'price': price, 'currency': currency}),
        'Authorization': f'Token {BITPAY_API_TOKEN}'
    }
    payload = {'price': price, 'currency': currency, 'token': BITPAY_API_TOKEN}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def get_invoice_status(invoice_id):
    """Verifica status da fatura"""
    if not BITPAY_ENABLED:
        return {'data': {'status': 'paid'}}
    
    url = f'{BITPAY_API_URL}/invoices/{invoice_id}'
    headers = {
        'X-Accept-Version': '2.0.0',
        'X-Identity': BITPAY_PUBLIC_KEY_HEX,
        'X-Signature': sign_request(url, {}),
        'Authorization': f'Token {BITPAY_API_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def send_to_wallet(amount_btc):
    """Envia Bitcoin para wallet configurada"""
    if not BITPAY_ENABLED:
        # Modo de desenvolvimento - simula envio
        return {
            'data': {
                'id': f'payout_dev_{int(time.time())}',
                'status': 'completed',
                'amount': amount_btc,
                'address': BITCOIN_WALLET_ADDRESS or 'dev_wallet_address'
            }
        }
    
    url = f'{BITPAY_API_URL}/payouts'
    headers = {
        'Content-Type': 'application/json',
        'X-Accept-Version': '2.0.0',
        'X-Identity': BITPAY_PUBLIC_KEY_HEX,
        'X-Signature': sign_request(url, {'amount': amount_btc, 'address': BITCOIN_WALLET_ADDRESS}),
        'Authorization': f'Token {BITPAY_API_TOKEN}'
    }
    payload = {'amount': amount_btc, 'currency': 'BTC', 'address': BITCOIN_WALLET_ADDRESS}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def process_payment_conversion(fiat_amount, currency):
    """Processa conversão completa: cria fatura, converte e envia"""
    try:
        import time
        
        # Cria fatura BitPay
        invoice = create_invoice(fiat_amount, currency)
        
        # Converte para Bitcoin
        from src.utils.bitcoin_converter import convert_fiat_to_btc
        btc_amount = convert_fiat_to_btc(fiat_amount, currency)
        
        # Envia para wallet
        payout = send_to_wallet(btc_amount)
        
        return {
            'success': True,
            'invoice_id': invoice.get('data', {}).get('id'),
            'btc_amount': btc_amount,
            'payout_id': payout.get('data', {}).get('id'),
            'wallet_address': BITCOIN_WALLET_ADDRESS or 'dev_wallet_address',
            'mode': 'development' if not BITPAY_ENABLED else 'production'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }