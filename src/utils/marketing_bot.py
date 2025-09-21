"""
Bot de Marketing Digital e Telemarketing Automático
Sistema hacker para upsell e conversões automáticas
"""

import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.settings import DEBUG

class MarketingBot:
    """Bot hacker para automação de marketing e telemarketing"""
    
    def __init__(self):
        self.smtp_configs = [
            {'host': 'smtp.gmail.com', 'port': 587},
            {'host': 'smtp.outlook.com', 'port': 587},
            {'host': 'smtp.yahoo.com', 'port': 587}
        ]
        self.email_templates = self._load_templates()
    
    def _load_templates(self):
        """Carrega templates de email hacker-style"""
        return {
            'upsell': [
                "🔥 {name}, teu pagamento de R${amount} virou BTC! Quer upar pra PREMIUM?",
                "💎 {name}, R${amount} convertido! Aproveita: +R$50/mês = 2x mais Bitcoin!",
                "🚀 {name}, BTC confirmado! Upgrade pra VIP: produtos exclusivos + BTC automático!",
                "⚡ {name}, R${amount} em Bitcoin! Quer escalar? Plano PRO = 5x mais conversões!"
            ],
            'dropship': [
                "🛍️ {name}, viu esse produto incrível? Só R$50 e vira BTC direto!",
                "💎 {name}, produto premium disponível! Compra agora = Bitcoin instantâneo!",
                "🔥 {name}, oferta relâmpago! Produto dropship + conversão BTC automática!",
                "⚡ {name}, produto viral! R$50 = BTC + frete grátis pra todo Brasil!"
            ],
            'follow_up': [
                "🎯 {name}, não perdeu a chance? BTC subindo, oferta caindo!",
                "⏰ {name}, última chance! Produto saindo de linha, BTC subindo!",
                "🔥 {name}, oferta expira em 24h! BTC + produto = combo insano!",
                "💥 {name}, estoque acabando! Últimas unidades + BTC garantido!"
            ]
        }
    
    def send_upsell_email(self, email, name, amount, product_suggestion='Produto Dropship Premium'):
        """Envia email de upsell pós-pagamento"""
        try:
            template = random.choice(self.email_templates['upsell'])
            subject = f"🔥 {name}, teu R${amount} virou BTC! Upgrade disponível!"
            
            body = f"""
            <html>
            <body style="font-family: Arial; background: #000; color: #00ff00;">
                <h2>🚀 SISTEMA BITCOIN - UPSELL AUTOMÁTICO</h2>
                <p>{template.format(name=name, amount=amount)}</p>
                
                <div style="background: #111; padding: 20px; margin: 20px 0; border: 2px solid #00ff00;">
                    <h3>💎 OFERTA EXCLUSIVA:</h3>
                    <ul>
                        <li>✅ {product_suggestion} - R$50/mês</li>
                        <li>✅ 2x mais Bitcoin por pagamento</li>
                        <li>✅ Produtos dropship premium</li>
                        <li>✅ Suporte VIP 24/7</li>
                        <li>✅ Conversão automática garantida</li>
                    </ul>
                </div>
                
                <p><strong>🔥 AÇÃO IMEDIATA:</strong> Clique aqui para upgrade instantâneo!</p>
                <p style="color: #ff0000;">⚠️ Oferta válida por 24h apenas!</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/upgrade?email={email}" 
                       style="background: #00ff00; color: #000; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px;">
                        🚀 UPGRADE AGORA - R$50/MÊS
                    </a>
                </div>
                
                <p style="font-size: 12px; color: #666;">
                    Sistema automatizado - Bitcoin Payment System<br>
                    Ignorando limites, maximizando conversões!
                </p>
            </body>
            </html>
            """
            
            self._send_email(email, subject, body)
            
            if DEBUG:
                print(f"🔥 Email upsell enviado para {email} - R${amount}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no bot de marketing: {e}")
            return False
    
    def send_dropship_email(self, email, name, product_name, price):
        """Envia email de produto dropship"""
        try:
            template = random.choice(self.email_templates['dropship'])
            subject = f"🛍️ {name}, produto incrível disponível! R${price} = BTC direto!"
            
            body = f"""
            <html>
            <body style="font-family: Arial; background: #000; color: #00ff00;">
                <h2>🛍️ DROPSHIP AUTOMÁTICO - CONVERSÃO BTC</h2>
                <p>{template.format(name=name)}</p>
                
                <div style="background: #111; padding: 20px; margin: 20px 0; border: 2px solid #00ff00;">
                    <h3>🔥 PRODUTO DESTAQUE:</h3>
                    <h4>{product_name}</h4>
                    <p><strong>💰 Preço: R${price}</strong></p>
                    <p><strong>⚡ Conversão: 100% para Bitcoin</strong></p>
                    <p><strong>🚚 Frete: GRÁTIS para todo Brasil</strong></p>
                    <p><strong>⏰ Entrega: 7-15 dias úteis</strong></p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/dropship?product={product_name}&price={price}" 
                       style="background: #00ff00; color: #000; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px;">
                        🛒 COMPRAR AGORA - R${price}
                    </a>
                </div>
                
                <p style="color: #ff0000;">⚠️ Estoque limitado! Últimas unidades disponíveis!</p>
            </body>
            </html>
            """
            
            self._send_email(email, subject, body)
            
            if DEBUG:
                print(f"🛍️ Email dropship enviado para {email} - {product_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no bot dropship: {e}")
            return False
    
    def send_follow_up_email(self, email, name, days_since_payment=1):
        """Envia email de follow-up"""
        try:
            template = random.choice(self.email_templates['follow_up'])
            subject = f"⏰ {name}, última chance! Oferta expirando em {24-days_since_payment}h!"
            
            body = f"""
            <html>
            <body style="font-family: Arial; background: #000; color: #ff0000;">
                <h2>⏰ FOLLOW-UP AUTOMÁTICO - URGENTE!</h2>
                <p>{template.format(name=name)}</p>
                
                <div style="background: #111; padding: 20px; margin: 20px 0; border: 2px solid #ff0000;">
                    <h3>🔥 OFERTA RELÂMPAGO:</h3>
                    <ul>
                        <li>✅ Bitcoin subindo +15% hoje</li>
                        <li>✅ Produtos dropship com 50% OFF</li>
                        <li>✅ Upgrade premium por R$25 (era R$50)</li>
                        <li>✅ Frete grátis para todo Brasil</li>
                        <li>✅ Conversão garantida em 24h</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/urgent?email={email}" 
                       style="background: #ff0000; color: #fff; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px;">
                        ⚡ APROVEITAR AGORA - 50% OFF
                    </a>
                </div>
                
                <p style="color: #ff0000; font-size: 18px; font-weight: bold;">
                    ⚠️ OFERTA EXPIRA EM {24-days_since_payment} HORAS!
                </p>
            </body>
            </html>
            """
            
            self._send_email(email, subject, body)
            
            if DEBUG:
                print(f"⏰ Follow-up enviado para {email} - dia {days_since_payment}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no follow-up: {e}")
            return False
    
    def _send_email(self, to_email, subject, body):
        """Envia email usando SMTP configurado"""
        try:
            # Seleciona SMTP aleatório para anonimato
            smtp_config = random.choice(self.smtp_configs)
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = 'hacker@bitcoinpayments.com'
            msg['To'] = to_email
            
            # Adiciona headers para evitar spam
            msg['X-Priority'] = '1'
            msg['X-MSMail-Priority'] = 'High'
            msg['X-Mailer'] = 'Bitcoin Payment System v2.0'
            
            html_part = MIMEText(body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Em produção, use credenciais reais
            if DEBUG:
                print(f"📧 Simulando envio para {to_email}")
                print(f"📧 Assunto: {subject}")
            else:
                # Código real para envio (configure suas credenciais)
                server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
                server.starttls()
                # server.login('seu_email', 'sua_senha')
                # server.send_message(msg)
                server.quit()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro SMTP: {e}")
            return False
    
    def schedule_follow_ups(self, email, name, amount):
        """Agenda follow-ups automáticos"""
        try:
            # Simula agendamento (em produção, use celery ou similar)
            follow_up_times = [1, 3, 7, 14, 30]  # dias após pagamento
            
            for days in follow_up_times:
                # Em produção, agende com delay
                if DEBUG:
                    print(f"📅 Follow-up agendado para {email} em {days} dias")
                
            return True
            
        except Exception as e:
            print(f"❌ Erro no agendamento: {e}")
            return False

# Instância global do bot
marketing_bot = MarketingBot()

# Funções de conveniência
def send_upsell_email(email, name, amount, product_suggestion='Produto Dropship Premium'):
    """Função de conveniência para upsell"""
    return marketing_bot.send_upsell_email(email, name, amount, product_suggestion)

def send_dropship_email(email, name, product_name, price):
    """Função de conveniência para dropship"""
    return marketing_bot.send_dropship_email(email, name, product_name, price)

def send_follow_up_email(email, name, days_since_payment=1):
    """Função de conveniência para follow-up"""
    return marketing_bot.send_follow_up_email(email, name, days_since_payment)

def schedule_follow_ups(email, name, amount):
    """Função de conveniência para agendamento"""
    return marketing_bot.schedule_follow_ups(email, name, amount)

