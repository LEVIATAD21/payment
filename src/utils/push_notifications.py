"""
Push Notifications - Engajamento Supremo
Sistema de notificações push para manter clientes ativos
"""

import requests
import json
from src.config.settings import DEBUG

class PushNotificationService:
    """Serviço de notificações push"""
    
    def __init__(self):
        # Configure suas chaves OneSignal no .env
        self.app_id = None  # Será carregado do .env
        self.api_key = None  # Será carregado do .env
        self.base_url = 'https://onesignal.com/api/v1'
        
        # Templates de notificações
        self.templates = {
            'payment_success': {
                'title': '💰 Pagamento Convertido!',
                'message': 'Seu pagamento de R${amount} foi convertido para {btc_amount} BTC!',
                'icon': 'https://bitcoin.org/img/icons/opengraph.png',
                'url': 'https://bitcoin.org'
            },
            'upsell_offer': {
                'title': '🚀 Oferta Especial!',
                'message': 'Aproveite nossa oferta exclusiva e maximize seus ganhos em Bitcoin!',
                'icon': 'https://bitcoin.org/img/icons/opengraph.png',
                'url': 'https://bitcoin.org'
            },
            'dropship_ready': {
                'title': '📦 Produto Enviado!',
                'message': 'Seu produto dropship foi enviado e o valor convertido para Bitcoin!',
                'icon': 'https://bitcoin.org/img/icons/opengraph.png',
                'url': 'https://bitcoin.org'
            },
            'price_alert': {
                'title': '📈 Alerta de Preço!',
                'message': 'Bitcoin subiu {percentage}%! Aproveite para converter mais!',
                'icon': 'https://bitcoin.org/img/icons/opengraph.png',
                'url': 'https://bitcoin.org'
            }
        }
    
    def load_credentials(self):
        """Carrega credenciais do .env"""
        try:
            from src.config.settings import ONESIGNAL_APP_ID, ONESIGNAL_API_KEY
            self.app_id = ONESIGNAL_APP_ID
            self.api_key = ONESIGNAL_API_KEY
            
            if not self.app_id or not self.api_key:
                if DEBUG:
                    print("⚠️ Chaves OneSignal não configuradas - usando modo simulação")
                return False
            
            return True
            
        except ImportError:
            if DEBUG:
                print("⚠️ Chaves OneSignal não encontradas no .env")
            return False
    
    def send_notification(self, player_ids, template_name, data=None, segments=None):
        """Envia notificação push"""
        try:
            if not self.load_credentials():
                return self._simulate_notification(template_name, data)
            
            template = self.templates.get(template_name, {})
            if not template:
                if DEBUG:
                    print(f"❌ Template {template_name} não encontrado")
                return False
            
            # Prepara dados da notificação
            notification_data = {
                'app_id': self.app_id,
                'contents': {'en': self._format_message(template['message'], data or {})},
                'headings': {'en': template['title']},
                'url': template.get('url', ''),
                'chrome_web_icon': template.get('icon', ''),
                'chrome_web_badge': template.get('icon', ''),
                'data': data or {}
            }
            
            # Adiciona destinatários
            if player_ids:
                notification_data['include_player_ids'] = player_ids
            elif segments:
                notification_data['included_segments'] = segments
            else:
                notification_data['included_segments'] = ['All']
            
            # Headers de autenticação
            headers = {
                'Authorization': f'Basic {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Envia notificação
            response = requests.post(
                f'{self.base_url}/notifications',
                json=notification_data,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if DEBUG:
                print(f"📱 Notificação enviada: {template_name} - ID: {result.get('id')}")
            
            return {
                'success': True,
                'notification_id': result.get('id'),
                'recipients': result.get('recipients', 0)
            }
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao enviar notificação: {e}")
            return {'success': False, 'error': str(e)}
    
    def _format_message(self, message, data):
        """Formata mensagem com dados"""
        try:
            return message.format(**data)
        except KeyError as e:
            if DEBUG:
                print(f"⚠️ Dados faltando na mensagem: {e}")
            return message
    
    def _simulate_notification(self, template_name, data):
        """Simula notificação para desenvolvimento"""
        if DEBUG:
            print(f"📱 [SIMULAÇÃO] Notificação {template_name}: {data}")
        return {'success': True, 'simulated': True}
    
    def send_payment_success(self, player_id, amount, btc_amount):
        """Envia notificação de pagamento bem-sucedido"""
        data = {
            'amount': f"{amount:.2f}",
            'btc_amount': f"{btc_amount:.8f}"
        }
        return self.send_notification([player_id], 'payment_success', data)
    
    def send_upsell_offer(self, player_ids):
        """Envia oferta de upsell"""
        return self.send_notification(player_ids, 'upsell_offer')
    
    def send_dropship_ready(self, player_id, product_name):
        """Envia notificação de produto dropship pronto"""
        data = {'product_name': product_name}
        return self.send_notification([player_id], 'dropship_ready', data)
    
    def send_price_alert(self, percentage_change):
        """Envia alerta de preço"""
        data = {'percentage': f"{percentage_change:.2f}"}
        return self.send_notification(None, 'price_alert', data, ['All'])
    
    def get_notification_stats(self):
        """Retorna estatísticas de notificações"""
        try:
            if not self.load_credentials():
                return {'simulated': True}
            
            headers = {'Authorization': f'Basic {self.api_key}'}
            response = requests.get(f'{self.base_url}/apps/{self.app_id}', headers=headers)
            response.raise_for_status()
            
            app_data = response.json()
            
            return {
                'app_id': app_data.get('id'),
                'name': app_data.get('name'),
                'players': app_data.get('players', 0),
                'created_at': app_data.get('created_at')
            }
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao obter estatísticas: {e}")
            return {'error': str(e)}

# Instância global
push_service = PushNotificationService()

# Funções de conveniência
def send_payment_notification(player_id, amount, btc_amount):
    """Envia notificação de pagamento"""
    return push_service.send_payment_success(player_id, amount, btc_amount)

def send_upsell_notification(player_ids):
    """Envia notificação de upsell"""
    return push_service.send_upsell_offer(player_ids)

def send_dropship_notification(player_id, product_name):
    """Envia notificação de dropship"""
    return push_service.send_dropship_ready(player_id, product_name)

def send_price_alert_notification(percentage_change):
    """Envia alerta de preço"""
    return push_service.send_price_alert(percentage_change)

def get_push_stats():
    """Retorna estatísticas de push"""
    return push_service.get_notification_stats()
