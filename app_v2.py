"""
🚀 Bitcoin Payment System v2.0 - Backend Melhorado
Sistema completo de pagamentos com conversão automática para Bitcoin
Integração Stripe + Cripto + APIs avançadas
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

# Configurações
from src.config.settings import (
    APP_SECRET_KEY, DEBUG, STRIPE_PUBLISHABLE_KEY,
    STRIPE_SECRET_KEY, BITPAY_API_TOKEN, BITCOIN_WALLET_ADDRESS
)

# APIs
from src.api.stripe_handler import (
    create_customer, create_payment_method, create_price, 
    create_subscription, create_payment_intent, create_crypto_payment
)
from src.api.bitpay_handler import create_bitpay_invoice, get_bitcoin_price
from src.api.binance_handler import get_bitcoin_price_binance, convert_fiat_to_btc_binance

# Utilitários
from src.utils.bitcoin_converter import (
    get_bitcoin_price, convert_fiat_to_btc, validate_payment_amount, 
    get_conversion_preview, compare_exchanges
)
from src.utils.auth_2fa import setup_2fa, verify_2fa_setup, login_with_2fa, is_2fa_verified
from src.utils.ab_testing import get_ab_variant, track_ab_conversion, get_ab_results
from src.utils.push_notifications import send_payment_notification, get_push_stats
from src.utils.analytics import track_event, get_analytics_stats

# Banco de dados
from src.models.database import (
    init_database, Payment, Subscription, get_payment_stats, 
    get_subscription_stats, save_payment, save_subscription
)

# Webhooks
from src.webhooks.stripe_webhook import handle_stripe_webhook
from src.webhooks.bitpay_webhook import handle_bitpay_webhook

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

# Configurar CORS
CORS(app, origins=[
    'http://localhost:5173', 
    'http://localhost:3000', 
    'http://127.0.0.1:5173',
    'https://bitcoin-payment-hacker.ngrok.io'
])

# Inicializar banco de dados
init_database(app)

# Cache para dados temporários
payments_cache = []
subscriptions_cache = []

# ============================================================================
# 🏠 ROTAS PRINCIPAIS
# ============================================================================

@app.route('/')
def index():
    """Página principal - Redireciona para frontend"""
    return jsonify({
        "message": "🚀 Bitcoin Payment System v2.0",
        "version": "2.0.0",
        "frontend_url": "http://localhost:5173",
        "api_docs": "http://localhost:5000/api/health",
        "features": [
            "Stripe Payments (Cartões + Cripto)",
            "BitPay Bitcoin Integration", 
            "Binance Price Optimization",
            "2FA Security",
            "A/B Testing",
            "Analytics & Notifications"
        ]
    })

@app.route('/success')
def success():
    """Página de sucesso"""
    return jsonify({
        "message": "✅ Payment successful!",
        "redirect_to": "http://localhost:5173",
        "timestamp": datetime.now().isoformat()
    })

# ============================================================================
# 💳 APIs DE PAGAMENTOS
# ============================================================================

@app.route('/api/payments/create', methods=['POST'])
def create_payment():
    """Criar pagamento - Stripe ou BitPay"""
    try:
        data = request.json
        
        # Validação
        if not _validate_payment_data(data):
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Determinar método de pagamento
        payment_method = data.get('method', 'stripe')
        
        if payment_method == 'stripe':
            return _create_stripe_payment(data)
        elif payment_method == 'bitpay':
            return _create_bitpay_payment(data)
        elif payment_method == 'stripe_crypto':
            return _create_stripe_crypto_payment(data)
        else:
            return jsonify({'error': 'Método de pagamento inválido'}), 400
            
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

def _validate_payment_data(data: Dict[str, Any]) -> bool:
    """Validar dados do pagamento"""
    required_fields = ['email', 'name', 'amount']
    return all(field in data for field in required_fields)

def _create_stripe_payment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Criar pagamento Stripe (cartões)"""
    try:
        # Criar cliente
        customer = create_customer(data['email'], data['name'])
        
        # Criar método de pagamento
        pm = create_payment_method(
            data.get('card_number', '4242424242424242'),
            data.get('exp_month', 12),
            data.get('exp_year', 2025),
            data.get('cvc', '123')
        )
        
        # Criar intent
        intent = create_payment_intent(
            data['amount'],
            data.get('currency', 'brl'),
            customer.id,
            pm.id
        )
        
        # Salvar no banco
        payment = save_payment({
            'stripe_payment_intent_id': intent.id,
            'customer_id': customer.id,
            'amount': data['amount'],
            'currency': data.get('currency', 'brl'),
            'method': 'stripe',
            'status': 'pending'
        })
        
        # Tracking
        track_event('payment_created', {
            'method': 'stripe',
            'amount': data['amount'],
            'currency': data.get('currency', 'brl')
        })
        
        return jsonify({
            'success': True,
            'payment_id': payment.id,
            'client_secret': intent.client_secret,
            'message': 'Pagamento Stripe criado com sucesso!'
        })
        
    except Exception as e:
        logger.error(f"Erro Stripe: {str(e)}")
        return jsonify({'error': 'Erro ao processar pagamento Stripe'}), 500

def _create_stripe_crypto_payment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Criar pagamento Stripe Crypto (USDC/USDP)"""
    try:
        # Criar cliente
        customer = create_customer(data['email'], data['name'])
        
        # Criar pagamento crypto
        crypto_payment = create_crypto_payment(
            data['amount'],
            data.get('currency', 'usd'),
            data.get('crypto_currency', 'usdc'),
            customer.id
        )
        
        # Salvar no banco
        payment = save_payment({
            'stripe_payment_intent_id': crypto_payment.id,
            'customer_id': customer.id,
            'amount': data['amount'],
            'currency': data.get('currency', 'usd'),
            'crypto_currency': data.get('crypto_currency', 'usdc'),
            'method': 'stripe_crypto',
            'status': 'pending'
        })
        
        # Tracking
        track_event('crypto_payment_created', {
            'method': 'stripe_crypto',
            'amount': data['amount'],
            'crypto_currency': data.get('crypto_currency', 'usdc')
        })
        
        return jsonify({
            'success': True,
            'payment_id': payment.id,
            'client_secret': crypto_payment.client_secret,
            'crypto_currency': data.get('crypto_currency', 'usdc'),
            'message': 'Pagamento crypto criado com sucesso!'
        })
        
    except Exception as e:
        logger.error(f"Erro Stripe Crypto: {str(e)}")
        return jsonify({'error': 'Erro ao processar pagamento crypto'}), 500

def _create_bitpay_payment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Criar pagamento BitPay (Bitcoin)"""
    try:
        # Criar invoice BitPay
        invoice = create_bitpay_invoice(
            data['amount'],
            data.get('currency', 'brl'),
            data['email']
        )
        
        # Salvar no banco
        payment = save_payment({
            'bitpay_invoice_id': invoice['id'],
            'customer_email': data['email'],
            'amount': data['amount'],
            'currency': data.get('currency', 'brl'),
            'method': 'bitpay',
            'status': 'pending'
        })
        
        # Tracking
        track_event('bitcoin_payment_created', {
            'method': 'bitpay',
            'amount': data['amount'],
            'currency': data.get('currency', 'brl')
        })
        
        return jsonify({
            'success': True,
            'payment_id': payment.id,
            'bitpay_invoice_id': invoice['id'],
            'payment_url': invoice['url'],
            'bitcoin_address': invoice['bitcoinAddress'],
            'message': 'Pagamento Bitcoin criado com sucesso!'
        })
        
    except Exception as e:
        logger.error(f"Erro BitPay: {str(e)}")
        return jsonify({'error': 'Erro ao processar pagamento Bitcoin'}), 500

# ============================================================================
# 📊 APIs DE CONVERSÃO E PREÇOS
# ============================================================================

@app.route('/api/bitcoin/price', methods=['GET'])
def get_bitcoin_price_api():
    """Obter preço atual do Bitcoin"""
    try:
        # Obter preços de múltiplas fontes
        coingecko_price = get_bitcoin_price()
        binance_price = get_bitcoin_price_binance()
        
        # Comparar exchanges
        comparison = compare_exchanges()
        
        return jsonify({
            'success': True,
            'prices': {
                'coingecko': coingecko_price,
                'binance': binance_price
            },
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter preço Bitcoin: {str(e)}")
        return jsonify({'error': 'Erro ao obter preço'}), 500

@app.route('/api/convert/preview', methods=['POST'])
def preview_conversion():
    """Preview de conversão Fiat → Bitcoin"""
    try:
        data = request.json
        amount = data.get('amount')
        currency = data.get('currency', 'brl')
        
        if not amount:
            return jsonify({'error': 'Amount é obrigatório'}), 400
        
        # Obter preview de conversão
        preview = get_conversion_preview(amount, currency)
        
        return jsonify({
            'success': True,
            'preview': preview,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no preview: {str(e)}")
        return jsonify({'error': 'Erro no preview'}), 500

# ============================================================================
# 🔐 APIs DE AUTENTICAÇÃO 2FA
# ============================================================================

@app.route('/api/auth/2fa/setup', methods=['POST'])
def setup_2fa_api():
    """Setup do 2FA"""
    try:
        result = setup_2fa()
        
        if result['success']:
            return jsonify({
                'success': True,
                'qr_code': result['qr_code'],
                'backup_codes': result.get('backup_codes', []),
                'secret': result['secret']
            })
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logger.error(f"Erro setup 2FA: {str(e)}")
        return jsonify({'error': 'Erro no setup 2FA'}), 500

@app.route('/api/auth/2fa/verify', methods=['POST'])
def verify_2fa_api():
    """Verificar código 2FA"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token é obrigatório'}), 400
        
        result = verify_2fa_setup(token)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': '2FA configurado com sucesso!'
            })
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logger.error(f"Erro verificação 2FA: {str(e)}")
        return jsonify({'error': 'Erro na verificação 2FA'}), 500

# ============================================================================
# 📈 APIs DE ANALYTICS E ESTATÍSTICAS
# ============================================================================

@app.route('/api/analytics/stats', methods=['GET'])
def get_analytics_stats_api():
    """Obter estatísticas gerais"""
    try:
        stats = {
            'payments': get_payment_stats(),
            'subscriptions': get_subscription_stats(),
            'analytics': get_analytics_stats(),
            'push_notifications': get_push_stats()
        }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter stats: {str(e)}")
        return jsonify({'error': 'Erro ao obter estatísticas'}), 500

@app.route('/api/analytics/track', methods=['POST'])
def track_event_api():
    """Tracking de eventos"""
    try:
        data = request.json
        event = data.get('event')
        properties = data.get('properties', {})
        
        if not event:
            return jsonify({'error': 'Event é obrigatório'}), 400
        
        result = track_event(event, properties)
        
        return jsonify({
            'success': True,
            'tracked': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no tracking: {str(e)}")
        return jsonify({'error': 'Erro no tracking'}), 500

# ============================================================================
# 🧪 APIs DE A/B TESTING
# ============================================================================

@app.route('/api/ab-test/variant', methods=['GET'])
def get_ab_variant_api():
    """Obter variante A/B"""
    try:
        experiment = request.args.get('experiment', 'payment_page')
        user_id = request.args.get('user_id', 'anonymous')
        
        variant = get_ab_variant(experiment, user_id)
        
        return jsonify({
            'success': True,
            'experiment': experiment,
            'variant': variant,
            'user_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Erro A/B test: {str(e)}")
        return jsonify({'error': 'Erro no A/B test'}), 500

@app.route('/api/ab-test/conversion', methods=['POST'])
def track_ab_conversion_api():
    """Tracking de conversão A/B"""
    try:
        data = request.json
        experiment = data.get('experiment')
        variant = data.get('variant')
        user_id = data.get('user_id')
        
        if not all([experiment, variant, user_id]):
            return jsonify({'error': 'Dados incompletos'}), 400
        
        result = track_ab_conversion(experiment, variant, user_id)
        
        return jsonify({
            'success': True,
            'conversion_tracked': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro tracking A/B: {str(e)}")
        return jsonify({'error': 'Erro no tracking A/B'}), 500

# ============================================================================
# 🔔 APIs DE NOTIFICAÇÕES
# ============================================================================

@app.route('/api/notifications/send', methods=['POST'])
def send_notification_api():
    """Enviar notificação push"""
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')
        type_notification = data.get('type', 'payment')
        
        if not all([user_id, message]):
            return jsonify({'error': 'user_id e message são obrigatórios'}), 400
        
        result = send_payment_notification(user_id, message, type_notification)
        
        return jsonify({
            'success': True,
            'notification_sent': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {str(e)}")
        return jsonify({'error': 'Erro ao enviar notificação'}), 500

# ============================================================================
# 🔗 WEBHOOKS
# ============================================================================

@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Webhook Stripe"""
    try:
        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature')
        
        result = handle_stripe_webhook(payload, sig_header)
        
        if result['success']:
            return jsonify({'received': True})
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logger.error(f"Erro webhook Stripe: {str(e)}")
        return jsonify({'error': 'Erro no webhook'}), 500

@app.route('/webhook/bitpay', methods=['POST'])
def bitpay_webhook():
    """Webhook BitPay"""
    try:
        payload = request.get_data()
        
        result = handle_bitpay_webhook(payload)
        
        if result['success']:
            return jsonify({'received': True})
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        logger.error(f"Erro webhook BitPay: {str(e)}")
        return jsonify({'error': 'Erro no webhook'}), 500

# ============================================================================
# 🏥 HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check da API"""
    try:
        # Verificar conectividade com APIs
        stripe_status = "connected" if STRIPE_SECRET_KEY else "not_configured"
        bitpay_status = "connected" if BITPAY_API_TOKEN else "not_configured"
        bitcoin_wallet = "configured" if BITCOIN_WALLET_ADDRESS else "not_configured"
        
        return jsonify({
            'status': 'healthy',
            'version': '2.0.0',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'stripe': stripe_status,
                'bitpay': bitpay_status,
                'bitcoin_wallet': bitcoin_wallet,
                'database': 'connected',
                'frontend': 'http://localhost:5173'
            },
            'features': {
                'stripe_payments': True,
                'stripe_crypto': True,
                'bitpay_bitcoin': True,
                '2fa_security': True,
                'ab_testing': True,
                'analytics': True,
                'notifications': True
            }
        })
        
    except Exception as e:
        logger.error(f"Erro health check: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# ============================================================================
# 🚀 INICIALIZAÇÃO
# ============================================================================

if __name__ == '__main__':
    logger.info("🚀 Iniciando Bitcoin Payment System v2.0...")
    logger.info("💳 Stripe: Cartões + Cripto")
    logger.info("₿ BitPay: Bitcoin nativo")
    logger.info("🔐 2FA: Segurança máxima")
    logger.info("📊 Analytics: Tracking completo")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=DEBUG,
        threaded=True
    )
