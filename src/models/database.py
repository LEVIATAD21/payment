"""
Banco de Dados Persistente - SQLAlchemy
Migração de in-memory para PostgreSQL
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

db = SQLAlchemy()

class Payment(db.Model):
    """Modelo para pagamentos"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    stripe_payment_id = db.Column(db.String(100), unique=True, nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='BRL')
    btc_amount = db.Column(db.Float, nullable=True)
    btc_price = db.Column(db.Float, nullable=True)
    conversion_fee = db.Column(db.Float, nullable=True)
    payment_type = db.Column(db.String(20), nullable=False)  # 'unique' ou 'subscription'
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.id}: {self.customer_email} - R${self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'stripe_payment_id': self.stripe_payment_id,
            'customer_email': self.customer_email,
            'customer_name': self.customer_name,
            'amount': self.amount,
            'currency': self.currency,
            'btc_amount': self.btc_amount,
            'btc_price': self.btc_price,
            'conversion_fee': self.conversion_fee,
            'payment_type': self.payment_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Subscription(db.Model):
    """Modelo para assinaturas"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.String(100), primary_key=True)  # Stripe subscription ID
    customer_id = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='BRL')
    status = db.Column(db.String(20), nullable=False, default='active')
    current_period_start = db.Column(db.DateTime, nullable=True)
    current_period_end = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Subscription {self.id}: {self.customer_email} - R${self.amount}/mês>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_email': self.customer_email,
            'customer_name': self.customer_name,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DropshipOrder(db.Model):
    """Modelo para pedidos dropship"""
    __tablename__ = 'dropship_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    btc_amount = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DropshipOrder {self.id}: {self.product_name} - R${self.price}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'customer_email': self.customer_email,
            'customer_name': self.customer_name,
            'product_name': self.product_name,
            'product_id': self.product_id,
            'price': self.price,
            'profit': self.profit,
            'btc_amount': self.btc_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MarketingCampaign(db.Model):
    """Modelo para campanhas de marketing"""
    __tablename__ = 'marketing_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(100), nullable=False)
    campaign_type = db.Column(db.String(50), nullable=False)  # 'upsell', 'follow_up', 'dropship'
    target_email = db.Column(db.String(120), nullable=False)
    target_name = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='sent')
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened_at = db.Column(db.DateTime, nullable=True)
    clicked_at = db.Column(db.DateTime, nullable=True)
    converted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<MarketingCampaign {self.id}: {self.campaign_name} - {self.target_email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_name': self.campaign_name,
            'campaign_type': self.campaign_type,
            'target_email': self.target_email,
            'target_name': self.target_name,
            'amount': self.amount,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'clicked_at': self.clicked_at.isoformat() if self.clicked_at else None,
            'converted_at': self.converted_at.isoformat() if self.converted_at else None
        }

class SystemStats(db.Model):
    """Modelo para estatísticas do sistema"""
    __tablename__ = 'system_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    stat_name = db.Column(db.String(50), unique=True, nullable=False)
    stat_value = db.Column(db.Float, nullable=False)
    stat_data = db.Column(db.JSON, nullable=True)  # Dados adicionais em JSON
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemStats {self.stat_name}: {self.stat_value}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'stat_name': self.stat_name,
            'stat_value': self.stat_value,
            'stat_data': self.stat_data,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Funções de conveniência para consultas
def get_payment_stats():
    """Retorna estatísticas de pagamentos"""
    total_converted = db.session.query(func.sum(Payment.amount)).filter(Payment.status == 'completed').scalar() or 0
    btc_received = db.session.query(func.sum(Payment.btc_amount)).filter(Payment.status == 'completed').scalar() or 0
    total_payments = Payment.query.filter(Payment.status == 'completed').count()
    
    return {
        'total_converted': float(total_converted),
        'btc_received': float(btc_received),
        'total_payments': total_payments
    }

def get_subscription_stats():
    """Retorna estatísticas de assinaturas"""
    active_subs = Subscription.query.filter_by(status='active').count()
    total_revenue = db.session.query(func.sum(Subscription.amount)).filter(Subscription.status == 'active').scalar() or 0
    
    return {
        'active_subs': active_subs,
        'total_revenue': float(total_revenue)
    }

def get_dropship_stats():
    """Retorna estatísticas de dropship"""
    total_orders = DropshipOrder.query.count()
    total_profit = db.session.query(func.sum(DropshipOrder.profit)).scalar() or 0
    total_btc = db.session.query(func.sum(DropshipOrder.btc_amount)).scalar() or 0
    
    return {
        'total_orders': total_orders,
        'total_profit': float(total_profit),
        'total_btc': float(total_btc)
    }

def get_marketing_stats():
    """Retorna estatísticas de marketing"""
    total_campaigns = MarketingCampaign.query.count()
    opened_campaigns = MarketingCampaign.query.filter(MarketingCampaign.opened_at.isnot(None)).count()
    clicked_campaigns = MarketingCampaign.query.filter(MarketingCampaign.clicked_at.isnot(None)).count()
    converted_campaigns = MarketingCampaign.query.filter(MarketingCampaign.converted_at.isnot(None)).count()
    
    return {
        'total_campaigns': total_campaigns,
        'opened_campaigns': opened_campaigns,
        'clicked_campaigns': clicked_campaigns,
        'converted_campaigns': converted_campaigns,
        'open_rate': (opened_campaigns / total_campaigns * 100) if total_campaigns > 0 else 0,
        'click_rate': (clicked_campaigns / total_campaigns * 100) if total_campaigns > 0 else 0,
        'conversion_rate': (converted_campaigns / total_campaigns * 100) if total_campaigns > 0 else 0
    }

def init_database(app):
    """Inicializa o banco de dados"""
    # Configura SQLite como fallback se não houver configuração
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bitcoin_payment.db'
    
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")

# ============================================================================
# 🆕 FUNÇÕES ADICIONAIS PARA APP_V2
# ============================================================================

def save_payment(payment_data: dict) -> Payment:
    """Salvar pagamento no banco de dados"""
    try:
        payment = Payment(
            stripe_payment_id=payment_data.get('stripe_payment_intent_id', ''),
            customer_email=payment_data.get('customer_email', ''),
            customer_name=payment_data.get('customer_name', ''),
            amount=payment_data.get('amount', 0),
            currency=payment_data.get('currency', 'brl'),
            btc_amount=payment_data.get('btc_amount'),
            btc_price=payment_data.get('btc_price'),
            conversion_fee=payment_data.get('conversion_fee'),
            payment_type=payment_data.get('payment_type', 'unique'),
            status=payment_data.get('status', 'pending')
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return payment
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar pagamento: {e}")
        raise

def save_subscription(subscription_data: dict) -> Subscription:
    """Salvar assinatura no banco de dados"""
    try:
        subscription = Subscription(
            stripe_subscription_id=subscription_data.get('stripe_subscription_id', ''),
            customer_email=subscription_data.get('customer_email', ''),
            customer_name=subscription_data.get('customer_name', ''),
            amount=subscription_data.get('amount', 0),
            currency=subscription_data.get('currency', 'brl'),
            status=subscription_data.get('status', 'active')
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return subscription
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar assinatura: {e}")
        raise
