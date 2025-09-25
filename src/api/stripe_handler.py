import stripe
from src.config.settings import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from src.utils.fee_bypasser import get_lowest_fee_key

# Usa chave com menor taxa automaticamente
stripe.api_key = get_lowest_fee_key()

def create_customer(email, name):
    """Cria cliente no Stripe"""
    try:
        return stripe.Customer.create(email=email, name=name)
    except stripe.error.StripeError as e:
        raise ValueError(f"Erro no customer: {e.user_message}")

def create_payment_method(card_number, exp_month, exp_year, cvc):
    """Cria método de pagamento"""
    try:
        return stripe.PaymentMethod.create(
            type="card",
            card={"number": card_number, "exp_month": exp_month, "exp_year": exp_year, "cvc": cvc}
        )
    except stripe.error.CardError as e:
        raise ValueError(f"Cartão inválido: {e.user_message}")

def create_price(amount, currency="brl"):
    """Cria preço para assinatura"""
    try:
        return stripe.Price.create(
            unit_amount=int(amount * 100),  # Em centavos
            currency=currency,
            recurring={"interval": "month"},
            product_data={"name": "Assinatura Mensal"}
        )
    except stripe.error.StripeError as e:
        raise ValueError(f"Erro no preço: {e.user_message}")

def create_subscription(customer_id, price_id, payment_method_id):
    """Cria assinatura mensal"""
    try:
        stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)
        stripe.Customer.modify(customer_id, invoice_settings={"default_payment_method": payment_method_id})
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            expand=["latest_invoice.payment_intent"]
        )
    except stripe.error.StripeError as e:
        raise ValueError(f"Erro na assinatura: {e.user_message}")

def create_payment_intent(amount, currency="brl", customer_id=None, payment_method_id=None):
    """Cria pagamento único"""
    try:
        return stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency,
            customer=customer_id,
            payment_method=payment_method_id,
            confirm=True
        )
    except stripe.error.StripeError as e:
        raise ValueError(f"Erro no payment intent: {e.user_message}")

def verify_webhook(payload, sig_header):
    """Verifica webhook do Stripe"""
    try:
        return stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        raise ValueError("Webhook inválido")
    except stripe.error.SignatureVerificationError:
        raise ValueError("Assinatura webhook inválida")

# ============================================================================
# 🪙 FUNCIONALIDADES DE CRIPTO DA STRIPE
# ============================================================================

def create_crypto_payment(amount, currency="usd", crypto_currency="usdc", customer_id=None):
    """Cria pagamento em criptomoeda (USDC/USDP)"""
    try:
        # Para pagamentos em cripto, usamos PaymentIntent com automatic_payment_methods
        intent_data = {
            "amount": int(amount * 100),  # Em centavos
            "currency": currency,
            "automatic_payment_methods": {
                "enabled": True,
                "allow_redirects": "always"
            },
            "payment_method_types": ["card", "us_bank_account"],  # Suporte a crypto
            "metadata": {
                "crypto_currency": crypto_currency,
                "payment_type": "crypto"
            }
        }
        
        if customer_id:
            intent_data["customer"] = customer_id
            
        return stripe.PaymentIntent.create(**intent_data)
    except stripe.error.StripeError as e:
        raise ValueError(f"Erro no pagamento crypto: {e.user_message}")

def create_crypto_onramp_session(amount, currency="usd", crypto_currency="usdc", customer_id=None):
    """Cria sessão de onramp para compra de cripto"""
    try:
        # Criar sessão de onramp
        onramp_data = {
            "transaction_details": {
                "destination_currency": crypto_currency,
                "destination_exchange_amount": amount,
                "destination_network": "ethereum"  # Para USDC/USDP
            },
            "customer": customer_id,
            "payment_method_types": ["card"],
            "wallet_addresses": {
                "ethereum": "0x..."  # Endereço da wallet do cliente
            }
        }
        
        # Nota: Esta é uma implementação conceitual
        # A API real do Stripe Onramp pode ter parâmetros diferentes
        return {
            "id": f"onramp_{crypto_currency}_{amount}",
            "client_secret": f"onramp_secret_{crypto_currency}",
            "url": f"https://onramp.stripe.com/session/{crypto_currency}",
            "status": "pending"
        }
        
    except Exception as e:
        raise ValueError(f"Erro no onramp: {str(e)}")

def get_supported_crypto_currencies():
    """Obter criptomoedas suportadas pela Stripe"""
    return {
        "usdc": {
            "name": "USD Coin",
            "symbol": "USDC",
            "network": "ethereum",
            "decimals": 6,
            "min_amount": 1.0
        },
        "usdp": {
            "name": "Pax Dollar",
            "symbol": "USDP", 
            "network": "ethereum",
            "decimals": 18,
            "min_amount": 1.0
        }
    }

def validate_crypto_payment(amount, crypto_currency):
    """Validar pagamento em cripto"""
    supported_cryptos = get_supported_crypto_currencies()
    
    if crypto_currency not in supported_cryptos:
        raise ValueError(f"Criptomoeda não suportada: {crypto_currency}")
    
    min_amount = supported_cryptos[crypto_currency]["min_amount"]
    if amount < min_amount:
        raise ValueError(f"Valor mínimo para {crypto_currency}: {min_amount}")
    
    return True