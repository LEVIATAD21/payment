"""
Autenticação 2FA - Segurança Suprema
Sistema de dois fatores para proteção total
"""

import pyotp
import qrcode
import io
import base64
from flask import session, request
from src.config.settings import APP_SECRET_KEY, DEBUG
import secrets

class TwoFactorAuth:
    """Sistema de autenticação de dois fatores"""
    
    def __init__(self):
        self.issuer_name = "Bitcoin Payment System"
        self.app_name = "Admin Dashboard"
    
    def generate_secret(self):
        """Gera chave secreta para 2FA"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, secret, email="admin@bitcoinpayment.com"):
        """Gera QR code para configuração do 2FA"""
        try:
            totp = pyotp.TOTP(secret)
            provisioning_uri = totp.provisioning_uri(
                name=email,
                issuer_name=self.issuer_name
            )
            
            # Gera QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converte para base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao gerar QR code: {e}")
            return None
    
    def verify_code(self, secret, code):
        """Verifica código 2FA"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=1)  # Tolerância de 1 período
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na verificação 2FA: {e}")
            return False
    
    def generate_backup_codes(self, count=10):
        """Gera códigos de backup"""
        return [secrets.token_hex(4).upper() for _ in range(count)]
    
    def setup_2fa(self, email="admin@bitcoinpayment.com"):
        """Configura 2FA para um usuário"""
        try:
            secret = self.generate_secret()
            qr_code = self.generate_qr_code(secret, email)
            backup_codes = self.generate_backup_codes()
            
            # Salva na sessão temporariamente
            session['2fa_setup'] = {
                'secret': secret,
                'email': email,
                'backup_codes': backup_codes,
                'verified': False
            }
            
            return {
                'success': True,
                'secret': secret,
                'qr_code': qr_code,
                'backup_codes': backup_codes,
                'manual_key': secret
            }
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro no setup 2FA: {e}")
            return {'success': False, 'error': str(e)}
    
    def verify_2fa_setup(self, code):
        """Verifica código durante setup do 2FA"""
        try:
            setup_data = session.get('2fa_setup')
            if not setup_data:
                return {'success': False, 'error': 'Setup não encontrado'}
            
            secret = setup_data['secret']
            if self.verify_code(secret, code):
                # Marca como verificado
                session['2fa_setup']['verified'] = True
                session['2fa_secret'] = secret
                session['2fa_enabled'] = True
                
                return {
                    'success': True,
                    'message': '2FA configurado com sucesso!',
                    'backup_codes': setup_data['backup_codes']
                }
            else:
                return {'success': False, 'error': 'Código inválido'}
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na verificação setup: {e}")
            return {'success': False, 'error': str(e)}
    
    def login_with_2fa(self, code):
        """Login com código 2FA"""
        try:
            secret = session.get('2fa_secret')
            if not secret:
                return {'success': False, 'error': '2FA não configurado'}
            
            if self.verify_code(secret, code):
                session['2fa_verified'] = True
                session['2fa_login_time'] = pyotp.time.time()
                return {'success': True, 'message': 'Login realizado com sucesso!'}
            else:
                return {'success': False, 'error': 'Código 2FA inválido'}
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro no login 2FA: {e}")
            return {'success': False, 'error': str(e)}
    
    def is_2fa_verified(self):
        """Verifica se 2FA está verificado"""
        return session.get('2fa_verified', False)
    
    def logout_2fa(self):
        """Logout do 2FA"""
        session.pop('2fa_verified', None)
        session.pop('2fa_login_time', None)
    
    def get_remaining_time(self):
        """Retorna tempo restante do código atual"""
        try:
            totp = pyotp.TOTP(session.get('2fa_secret', ''))
            return totp.interval - (pyotp.time.time() % totp.interval)
        except:
            return 30

# Instância global
two_factor_auth = TwoFactorAuth()

# Funções de conveniência
def setup_2fa(email="admin@bitcoinpayment.com"):
    """Configura 2FA"""
    return two_factor_auth.setup_2fa(email)

def verify_2fa_setup(code):
    """Verifica setup do 2FA"""
    return two_factor_auth.verify_2fa_setup(code)

def login_with_2fa(code):
    """Login com 2FA"""
    return two_factor_auth.login_with_2fa(code)

def is_2fa_verified():
    """Verifica se 2FA está ativo"""
    return two_factor_auth.is_2fa_verified()

def logout_2fa():
    """Logout do 2FA"""
    two_factor_auth.logout_2fa()

def get_remaining_time():
    """Tempo restante do código"""
    return two_factor_auth.get_remaining_time()
