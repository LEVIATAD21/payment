import json
from flask import request
from src.api.stripe_handler import verify_webhook
from src.api.bitpay_handler import process_payment_conversion
from src.config.settings import DEBUG
from src.utils.marketing_bot import send_upsell_email, schedule_follow_ups
from src.utils.dropship_integration import create_dropship_upsell

def handle_webhook():
    """Processa webhooks do Stripe"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = verify_webhook(payload, sig_header)
        
        if event['type'] == 'payment_intent.succeeded':
            return _handle_payment_success(event['data']['object'])
        elif event['type'] == 'invoice.paid':
            return _handle_subscription_payment(event['data']['object'])
        elif event['type'] == 'invoice.payment_succeeded':
            return _handle_subscription_created(event['data']['object'])
        elif event['type'] == 'invoice.updated':
            return _handle_subscription_updated(event['data']['object'])
        elif event['type'] == 'customer.subscription.deleted':
            return _handle_subscription_cancelled(event['data']['object'])
        
        return json.dumps({'success': True, 'message': 'Evento ignorado'}), 200
        
    except Exception as e:
        if DEBUG:
            print(f"Erro no webhook: {str(e)}")
        return json.dumps({'error': str(e)}), 400

def _handle_payment_success(payment_intent):
    """Processa pagamento único bem-sucedido"""
    try:
        amount = payment_intent['amount'] / 100
        currency = payment_intent['currency']
        customer_id = payment_intent.get('customer')
        
        # Converte para Bitcoin
        result = process_payment_conversion(amount, currency)
        
        if result['success']:
            if DEBUG:
                print(f"Pagamento único sucesso: R${amount} convertido para {result['btc_amount']} BTC")
            
            # HACK: Marketing automático pós-pagamento
            try:
                # Simula dados do cliente (em produção, busque no Stripe)
                customer_email = f"cliente_{customer_id}@email.com" if customer_id else "cliente@email.com"
                customer_name = f"Cliente {customer_id}" if customer_id else "Cliente"
                
                # Envia email de upsell
                send_upsell_email(customer_email, customer_name, amount)
                
                # Agenda follow-ups
                schedule_follow_ups(customer_email, customer_name, amount)
                
                # Cria upsell dropship
                dropship_upsell = create_dropship_upsell(customer_email, customer_name, amount)
                if dropship_upsell:
                    if DEBUG:
                        print(f"🛍️ Upsell dropship criado: {dropship_upsell['suggested_product']['name']}")
                
            except Exception as e:
                if DEBUG:
                    print(f"⚠️ Erro no marketing automático: {e}")
            
            return json.dumps({'success': True, 'conversion': result}), 200
        else:
            if DEBUG:
                print(f"Erro na conversão: {result['error']}")
            return json.dumps({'error': result['error']}), 500
            
    except Exception as e:
        if DEBUG:
            print(f"Erro ao processar pagamento: {str(e)}")
        return json.dumps({'error': str(e)}), 500

def _handle_subscription_payment(invoice):
    """Processa pagamento de assinatura"""
    try:
        amount = invoice['amount_paid'] / 100
        currency = invoice['currency']
        
        # Converte para Bitcoin
        result = process_payment_conversion(amount, currency)
        
        if result['success']:
            if DEBUG:
                print(f"Pagamento assinatura: R${amount} convertido para {result['btc_amount']} BTC")
            return json.dumps({'success': True, 'conversion': result}), 200
        else:
            if DEBUG:
                print(f"Erro na conversão da assinatura: {result['error']}")
            return json.dumps({'error': result['error']}), 500
            
    except Exception as e:
        if DEBUG:
            print(f"Erro ao processar assinatura: {str(e)}")
        return json.dumps({'error': str(e)}), 500

def _handle_subscription_created(invoice):
    """Processa criação de assinatura"""
    if DEBUG:
        print("Nova assinatura criada")
    return json.dumps({'success': True, 'message': 'Assinatura criada'}), 200

def _handle_subscription_updated(invoice):
    """Processa atualização de assinatura"""
    if DEBUG:
        print("Assinatura atualizada")
    return json.dumps({'success': True, 'message': 'Assinatura atualizada'}), 200

def _handle_subscription_cancelled(subscription):
    """Processa cancelamento de assinatura"""
    if DEBUG:
        print("Assinatura cancelada")
    return json.dumps({'success': True, 'message': 'Assinatura cancelada'}), 200

# ============================================================================
# 🆕 FUNÇÃO PARA APP_V2
# ============================================================================

def handle_stripe_webhook(payload: bytes, sig_header: str) -> dict:
    """
    Processa webhook do Stripe para app_v2
    
    Args:
        payload: Dados do webhook em bytes
        sig_header: Cabeçalho de assinatura
    
    Returns:
        Dict com resultado do processamento
    """
    try:
        # Verificar webhook
        event = verify_webhook(payload, sig_header)
        
        event_type = event['type']
        
        if event_type == 'payment_intent.succeeded':
            return _handle_payment_success_v2(event['data']['object'])
        elif event_type == 'invoice.paid':
            return _handle_subscription_payment_v2(event['data']['object'])
        elif event_type == 'customer.subscription.created':
            return _handle_subscription_created_v2(event['data']['object'])
        else:
            return {'success': True, 'message': 'Evento ignorado'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def _handle_payment_success_v2(payment_intent: dict) -> dict:
    """Processa pagamento bem-sucedido para app_v2"""
    try:
        amount = payment_intent['amount'] / 100
        currency = payment_intent['currency']
        customer_id = payment_intent.get('customer')
        
        # TODO: Implementar conversão para Bitcoin
        # TODO: Atualizar banco de dados
        # TODO: Enviar notificações
        
        return {
            'success': True,
            'message': 'Pagamento processado',
            'amount': amount,
            'currency': currency,
            'customer_id': customer_id
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def _handle_subscription_payment_v2(invoice: dict) -> dict:
    """Processa pagamento de assinatura para app_v2"""
    try:
        amount = invoice['amount_paid'] / 100
        currency = invoice['currency']
        
        # TODO: Implementar processamento de assinatura
        
        return {
            'success': True,
            'message': 'Pagamento de assinatura processado',
            'amount': amount,
            'currency': currency
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def _handle_subscription_created_v2(subscription: dict) -> dict:
    """Processa criação de assinatura para app_v2"""
    try:
        subscription_id = subscription['id']
        customer_id = subscription['customer']
        
        # TODO: Implementar criação de assinatura
        
        return {
            'success': True,
            'message': 'Assinatura criada',
            'subscription_id': subscription_id,
            'customer_id': customer_id
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}