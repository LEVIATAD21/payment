import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações principais
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
BITPAY_API_TOKEN = os.getenv('BITPAY_API_TOKEN')
BITPAY_PRIVATE_KEY_HEX = os.getenv('BITPAY_PRIVATE_KEY_HEX')
BITPAY_PUBLIC_KEY_HEX = os.getenv('BITPAY_PUBLIC_KEY_HEX')
BITCOIN_WALLET_ADDRESS = os.getenv('BITCOIN_WALLET_ADDRESS')
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
CONVERSION_FEE = float(os.getenv('CONVERSION_FEE', 0.01))
MIN_AMOUNT = float(os.getenv('MIN_AMOUNT', 10.00))
MAX_AMOUNT = float(os.getenv('MAX_AMOUNT', 10000.00))

# Validação hacker-style: crasha se faltar key
required_keys = [STRIPE_SECRET_KEY, BITPAY_API_TOKEN, BITCOIN_WALLET_ADDRESS]
if any(key is None for key in required_keys):
    raise ValueError("Faltando keys no .env! Configura direito, bro.")

# URLs das APIs
BITPAY_API_URL = 'https://bitpay.com/api'
STRIPE_API_URL = 'https://api.stripe.com/v1'
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
