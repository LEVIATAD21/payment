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