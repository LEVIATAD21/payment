from flask import Flask, render_template, request, jsonify, session
from src.config.settings import APP_SECRET_KEY, DEBUG, STRIPE_PUBLISHABLE_KEY
from src.api.stripe_handler import create_customer, create_payment_method, create_price, create_subscription, create_payment_intent
from src.utils.bitcoin_converter import get_bitcoin_price, convert_fiat_to_btc, validate_payment_amount, get_conversion_preview
from src.webhooks.stripe_webhook import handle_webhook
from src.utils.marketing_bot import send_upsell_email, send_dropship_email
from src.utils.dropship_integration import get_dropship_products, process_dropship_order, get_sales_stats
from src.utils.fee_bypasser import get_bypass_stats, calculate_optimal_fee
from src.utils.i18n import init_babel, set_language, get_available_languages, t
from src.models.database import init_database, Payment, Subscription, DropshipOrder, MarketingCampaign, get_payment_stats, get_subscription_stats, get_dropship_stats, get_marketing_stats
from src.utils.lead_scraper import run_lead_generation, get_lead_statistics
from src.api.binance_handler import get_bitcoin_price_binance, convert_fiat_to_btc_binance, compare_exchanges
from src.utils.auth_2fa import setup_2fa, verify_2fa_setup, login_with_2fa, is_2fa_verified, logout_2fa
from src.utils.proxy_rotator import get_rotated_proxy, make_proxy_request, get_proxy_stats
from src.utils.ab_testing import get_ab_variant, get_ab_value, track_ab_conversion, get_ab_results
from src.utils.push_notifications import send_payment_notification, send_upsell_notification, get_push_stats

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

# Inicializa internacionalização
init_babel(app)

# Inicializa banco de dados
init_database(app)

# Simula DB (mantido para compatibilidade)
payments_history = []
subscriptions = []

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html', stripe_publishable_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/success')
def success():
    """Página de sucesso após pagamento"""
    return render_template('success.html')

# Dashboard removido - será redefinido abaixo com 2FA

@app.route('/api/create_payment', methods=['POST'])
def api_create_payment():
    """API para criar pagamento"""
    try:
        data = request.json
        
        # Validação hacker-proof
        if not data.get('email') or not data.get('name') or not data.get('amount'):
            return jsonify({'error': 'Dados obrigatórios: email, name, amount'}), 400
        
        validate_payment_amount(data['amount'])
        
        # Cria cliente
        customer = create_customer(data['email'], data['name'])
        
        # Cria método de pagamento (em prod, use Stripe Elements)
        pm = create_payment_method(
            data.get('card_number', '4242424242424242'),  # Teste
            data.get('exp_month', 12),
            data.get('exp_year', 2025),
            data.get('cvc', '123')
        )
        
        if data.get('type') == 'subscription':
            # Cria assinatura
            price = create_price(data['amount'], data.get('currency', 'brl'))
            sub = create_subscription(customer.id, price.id, pm.id)
            
            subscriptions.append({
                'id': sub.id,
                'customer_id': customer.id,
                'amount': data['amount'],
                'currency': data.get('currency', 'brl'),
                'status': 'active'
            })
            
            return jsonify({
                'success': True, 
                'sub_id': sub.id,
                'message': 'Assinatura criada! Conversão automática ativada.'
            })
        else:
            # Pagamento único
            intent = create_payment_intent(
                data['amount'], 
                data.get('currency', 'brl'), 
                customer.id, 
                pm.id
            )
            
            payments_history.append({
                'amount': data['amount'],
                'currency': data.get('currency', 'brl'),
                'customer_email': data['email'],
                'timestamp': str(int(time.time()))
            })
            
            return jsonify({
                'success': True, 
                'intent_id': intent.id,
                'message': 'Pagamento processado! Convertendo para Bitcoin...'
            })
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        if DEBUG:
            print(f"Erro na API: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/preview_conversion', methods=['POST'])
def api_preview_conversion():
    """API para preview da conversão"""
    try:
        data = request.json
        preview = get_conversion_preview(data['amount'], data.get('currency', 'brl'))
        return jsonify(preview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bitcoin_price')
def api_bitcoin_price():
    """API para preço do Bitcoin"""
    try:
        currency = request.args.get('currency', 'brl')
        price = get_bitcoin_price(currency)
        return jsonify({
            'success': True,
            'currency': currency.upper(),
            'price': price
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Webhook do Stripe"""
    return handle_webhook()

@app.route('/api/stats')
def api_stats():
    """API para estatísticas"""
    try:
        # Estatísticas básicas
        basic_stats = {
            'total_converted': sum(p['amount'] for p in payments_history),
            'btc_received': sum(convert_fiat_to_btc(p['amount'], p['currency']) for p in payments_history),
            'active_subs': len([s for s in subscriptions if s.get('status') == 'active']),
            'total_payments': len(payments_history),
            'btc_price': get_bitcoin_price('brl')
        }
        
        # Estatísticas de bypass de taxas
        bypass_stats = get_bypass_stats()
        
        # Estatísticas de dropship
        dropship_stats = get_sales_stats()
        
        # Combina todas as estatísticas
        stats = {
            **basic_stats,
            'fee_bypass': bypass_stats,
            'dropship': dropship_stats
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dropship_products')
def api_dropship_products():
    """API para produtos dropship"""
    try:
        products = get_dropship_products()
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dropship_order', methods=['POST'])
def api_dropship_order():
    """API para processar pedido dropship"""
    try:
        data = request.json
        order_data = {
            'id': f"dropship_{int(time.time())}",
            'email': data.get('email', 'cliente@email.com'),
            'total_price': str(data.get('amount', 100)),
            'currency': 'BRL',
            'line_items': [{
                'title': data.get('product_name', 'Produto Dropship'),
                'price': str(data.get('amount', 100)),
                'quantity': 1
            }],
            'financial_status': 'paid'
        }
        
        result = process_dropship_order(order_data)
        
        if result['success']:
            # Envia email de confirmação
            send_dropship_email(
                data.get('email', 'cliente@email.com'),
                data.get('name', 'Cliente'),
                data.get('product_name', 'Produto Dropship'),
                data.get('amount', 100)
            )
            
            return jsonify({
                'success': True,
                'message': 'Pedido dropship processado e convertido para Bitcoin!',
                'order_id': result['order_id'],
                'btc_amount': result['btc_amount']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upsell', methods=['POST'])
def api_upsell():
    """API para upsell automático"""
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        amount = data.get('amount', 100)
        
        if not email or not name:
            return jsonify({'error': 'Email e nome são obrigatórios'}), 400
        
        # Envia email de upsell
        result = send_upsell_email(email, name, amount)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Upsell enviado com sucesso!'
            })
        else:
            return jsonify({'error': 'Erro ao enviar upsell'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fee_optimization')
def api_fee_optimization():
    """API para otimização de taxas"""
    try:
        amount = float(request.args.get('amount', 100))
        fee_info = calculate_optimal_fee(amount)
        bypass_stats = get_bypass_stats()
        
        return jsonify({
            'success': True,
            'amount': amount,
            'fee_info': fee_info,
            'bypass_stats': bypass_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# NOVAS ROTAS HACKER - UPGRADES INTERGALÁCTICOS

@app.route('/api/set_language', methods=['POST'])
def api_set_language():
    """API para definir idioma"""
    try:
        data = request.json
        language = data.get('language', 'pt')
        
        if set_language(language):
            return jsonify({'success': True, 'language': language})
        else:
            return jsonify({'error': 'Idioma inválido'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/available_languages')
def api_available_languages():
    """API para idiomas disponíveis"""
    try:
        languages = get_available_languages()
        return jsonify({'success': True, 'languages': languages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lead_generation', methods=['POST'])
def api_lead_generation():
    """API para geração de leads via IA"""
    try:
        data = request.json
        max_emails = data.get('max_emails', 50)
        
        leads = run_lead_generation(max_emails)
        
        return jsonify({
            'success': True,
            'leads_found': len(leads),
            'leads': leads
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lead_statistics')
def api_lead_statistics():
    """API para estatísticas de leads"""
    try:
        stats = get_lead_statistics()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/binance_price')
def api_binance_price():
    """API para preço Bitcoin via Binance"""
    try:
        currency = request.args.get('currency', 'BRL')
        price = get_bitcoin_price_binance(currency)
        
        return jsonify({
            'success': True,
            'price': price,
            'currency': currency,
            'exchange': 'binance'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/binance_convert', methods=['POST'])
def api_binance_convert():
    """API para conversão via Binance"""
    try:
        data = request.json
        amount = data.get('amount', 100)
        currency = data.get('currency', 'BRL')
        
        result = convert_fiat_to_btc_binance(amount, currency)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare_exchanges')
def api_compare_exchanges():
    """API para comparar exchanges"""
    try:
        amount = float(request.args.get('amount', 100))
        currency = request.args.get('currency', 'BRL')
        
        comparison = compare_exchanges(amount, currency)
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/database_stats')
def api_database_stats():
    """API para estatísticas do banco de dados"""
    try:
        payment_stats = get_payment_stats()
        subscription_stats = get_subscription_stats()
        dropship_stats = get_dropship_stats()
        marketing_stats = get_marketing_stats()
        
        return jsonify({
            'success': True,
            'payments': payment_stats,
            'subscriptions': subscription_stats,
            'dropship': dropship_stats,
            'marketing': marketing_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mobile_payment', methods=['POST'])
def api_mobile_payment():
    """API específica para app mobile"""
    try:
        data = request.json
        language = data.get('language', 'pt')
        
        # Define idioma na sessão
        set_language(language)
        
        # Processa pagamento normalmente
        form_data = {
            'email': data.get('email'),
            'name': data.get('name'),
            'amount': data.get('amount'),
            'type': data.get('type', 'unique'),
            'currency': data.get('currency', 'brl'),
            'card_number': data.get('card_number'),
            'exp_month': data.get('exp_month'),
            'exp_year': data.get('exp_year'),
            'cvc': data.get('cvc')
        }
        
        # Validação
        if not form_data['email'] or not form_data['name'] or not form_data['amount']:
            return jsonify({'error': 'Campos obrigatórios não preenchidos'}), 400
        
        if not (10 <= form_data['amount'] <= 10000):
            return jsonify({'error': 'Valor deve estar entre R$ 10 e R$ 10.000'}), 400
        
        # Cria pagamento
        customer = create_customer(form_data['email'], form_data['name'])
        pm = create_payment_method(form_data['card_number'], form_data['exp_month'], form_data['exp_year'], form_data['cvc'])
        
        if form_data['type'] == 'subscription':
            price = create_price(form_data['amount'], form_data['currency'])
            sub = create_subscription(customer.id, price.id, pm.id)
            
            # Salva no banco
            subscription = Subscription(
                id=sub.id,
                customer_id=customer.id,
                customer_email=form_data['email'],
                customer_name=form_data['name'],
                amount=form_data['amount'],
                currency=form_data['currency'].upper(),
                status='active'
            )
            db.session.add(subscription)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Assinatura criada com sucesso!',
                'subscription_id': sub.id
            })
        else:
            intent = create_payment_intent(form_data['amount'], form_data['currency'], customer.id, pm.id)
            
            # Salva no banco
            payment = Payment(
                stripe_payment_id=intent.id,
                customer_email=form_data['email'],
                customer_name=form_data['name'],
                amount=form_data['amount'],
                currency=form_data['currency'].upper(),
                payment_type='unique',
                status='completed'
            )
            db.session.add(payment)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Pagamento realizado com sucesso!',
                'payment_id': intent.id
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ROTAS SUPREMAS - UPGRADES FINAIS

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Dashboard com proteção 2FA"""
    if request.method == 'POST':
        # Verifica código 2FA
        code = request.form.get('2fa_code')
        result = login_with_2fa(code)
        
        if result['success']:
            return redirect('/dashboard')
        else:
            return render_template('2fa.html', error=result['error'])
    
    # Verifica se 2FA está ativo
    if not is_2fa_verified():
        # Setup 2FA se não configurado
        if '2fa_secret' not in session:
            setup_result = setup_2fa()
            return render_template('2fa.html', 
                                qr_code=setup_result['qr_code'],
                                backup_codes=setup_result.get('backup_codes'))
        else:
            return render_template('2fa.html')
    
    # Dashboard normal
    stats = {
        'total_converted': sum(p['amount'] for p in payments_history),
        'btc_received': sum(convert_fiat_to_btc(p['amount'], p['currency']) for p in payments_history),
        'active_subs': len(subscriptions)
    }
    return render_template('dashboard.html', stats=stats, history=payments_history, subs=subscriptions)

@app.route('/api/setup_2fa', methods=['POST'])
def api_setup_2fa():
    """API para setup do 2FA"""
    try:
        data = request.json
        email = data.get('email', 'admin@bitcoinpayment.com')
        
        result = setup_2fa(email)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify_2fa_setup', methods=['POST'])
def api_verify_2fa_setup():
    """API para verificar setup do 2FA"""
    try:
        data = request.json
        code = data.get('code')
        
        result = verify_2fa_setup(code)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ab_test', methods=['POST'])
def api_ab_test():
    """API para A/B testing"""
    try:
        data = request.json
        experiment = data.get('experiment')
        event_type = data.get('event_type', 'conversion')
        value = data.get('value', 0)
        
        result = track_ab_conversion(experiment, event_type, value)
        return jsonify({'success': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ab_results/<experiment>')
def api_ab_results(experiment):
    """API para resultados A/B"""
    try:
        results = get_ab_results(experiment)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/push_notification', methods=['POST'])
def api_push_notification():
    """API para enviar notificação push"""
    try:
        data = request.json
        player_id = data.get('player_id')
        amount = data.get('amount', 0)
        btc_amount = data.get('btc_amount', 0)
        
        result = send_payment_notification(player_id, amount, btc_amount)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proxy_stats')
def api_proxy_stats():
    """API para estatísticas de proxies"""
    try:
        stats = get_proxy_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/push_stats')
def api_push_stats():
    """API para estatísticas de push"""
    try:
        stats = get_push_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics_track', methods=['POST'])
def api_analytics_track():
    """API para tracking de analytics"""
    try:
        data = request.json
        event = data.get('event')
        properties = data.get('properties', {})
        
        # Aqui você integraria com Google Analytics e Mixpanel
        # Por enquanto, apenas simula
        if DEBUG:
            print(f"📊 Analytics Event: {event} - {properties}")
        
        return jsonify({'success': True, 'tracked': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def api_health():
    """API de health check para monitoramento"""
    try:
        health_data = {
            'status': 'healthy',
            'timestamp': time.time(),
            'version': '2.0.0',
            'features': {
                '2fa': True,
                'ab_testing': True,
                'push_notifications': True,
                'proxy_rotation': True,
                'multi_language': True,
                'database': True,
                'lead_generation': True,
                'mobile_app': True,
                'binance_integration': True
            }
        }
        return jsonify(health_data)
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    import time
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)