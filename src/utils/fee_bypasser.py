"""
Sistema de Bypass de Taxas - Hacker Style
Rotaciona contas e minimiza fees automaticamente
"""

import random
import time
from src.config.settings import DEBUG

class FeeBypasser:
    """Sistema hacker para bypass de taxas"""
    
    def __init__(self):
        # Multi-contas Stripe (configure suas chaves reais)
        self.stripe_keys = [
            'sk_test_key_1',  # Conta principal
            'sk_test_key_2',  # Conta backup 1
            'sk_test_key_3',  # Conta backup 2
        ]
        
        # Multi-wallets Bitcoin para distribuição
        self.bitcoin_wallets = [
            'wallet_principal_btc',
            'wallet_backup_1_btc',
            'wallet_backup_2_btc',
        ]
        
        # Histórico de uso para rotação inteligente
        self.usage_history = {}
        self.fee_history = {}
        
    def get_lowest_fee_stripe_key(self):
        """Retorna chave Stripe com menor taxa"""
        try:
            # Simula verificação de taxas (em produção, consulte API real)
            current_fees = {}
            
            for i, key in enumerate(self.stripe_keys):
                # Simula taxa baseada em uso e horário
                base_fee = 2.9  # Taxa base Stripe
                usage_penalty = self.usage_history.get(key, 0) * 0.1
                time_bonus = 0.1 if time.hour < 6 else 0  # Madrugada = menor taxa
                
                current_fees[key] = base_fee + usage_penalty - time_bonus
            
            # Seleciona chave com menor taxa
            best_key = min(current_fees, key=current_fees.get)
            
            # Atualiza histórico
            self.usage_history[best_key] = self.usage_history.get(best_key, 0) + 1
            self.fee_history[best_key] = current_fees[best_key]
            
            if DEBUG:
                print(f"💰 Chave Stripe selecionada: {best_key[:10]}... (taxa: {current_fees[best_key]:.2f}%)")
            
            return best_key
            
        except Exception as e:
            print(f"❌ Erro na seleção de chave: {e}")
            return self.stripe_keys[0]  # Fallback
    
    def get_optimal_bitcoin_wallet(self, amount_btc):
        """Seleciona wallet Bitcoin otimizada"""
        try:
            # Distribui baseado no valor para evitar concentração
            if amount_btc < 0.001:  # Valores pequenos
                wallet = self.bitcoin_wallets[0]  # Wallet principal
            elif amount_btc < 0.01:  # Valores médios
                wallet = self.bitcoin_wallets[1]  # Wallet backup 1
            else:  # Valores grandes
                wallet = self.bitcoin_wallets[2]  # Wallet backup 2
            
            if DEBUG:
                print(f"🔑 Wallet Bitcoin selecionada: {wallet[:15]}... (valor: {amount_btc} BTC)")
            
            return wallet
            
        except Exception as e:
            print(f"❌ Erro na seleção de wallet: {e}")
            return self.bitcoin_wallets[0]  # Fallback
    
    def calculate_optimal_fee(self, amount, currency='brl'):
        """Calcula taxa otimizada baseada no valor"""
        try:
            # Taxa base
            base_fee_percent = 2.9
            
            # Desconto por volume
            if amount >= 1000:
                volume_discount = 0.5
            elif amount >= 500:
                volume_discount = 0.3
            elif amount >= 100:
                volume_discount = 0.1
            else:
                volume_discount = 0
            
            # Desconto por horário (madrugada = menor taxa)
            time_discount = 0.2 if time.hour < 6 else 0
            
            # Taxa final otimizada
            final_fee_percent = base_fee_percent - volume_discount - time_discount
            final_fee_amount = (amount * final_fee_percent) / 100
            
            if DEBUG:
                print(f"💰 Taxa otimizada: {final_fee_percent:.2f}% (R${final_fee_amount:.2f})")
            
            return {
                'fee_percent': final_fee_percent,
                'fee_amount': final_fee_amount,
                'savings': (base_fee_percent - final_fee_percent) * amount / 100
            }
            
        except Exception as e:
            print(f"❌ Erro no cálculo de taxa: {e}")
            return {
                'fee_percent': 2.9,
                'fee_amount': amount * 0.029,
                'savings': 0
            }
    
    def rotate_payment_method(self, customer_id):
        """Rotaciona método de pagamento para evitar detecção"""
        try:
            # Simula rotação de métodos (em produção, use APIs reais)
            payment_methods = [
                'card_visa',
                'card_mastercard',
                'card_amex',
                'pix_instant',
                'boleto_bancario'
            ]
            
            # Seleciona método baseado em horário e histórico
            method_index = (time.hour + hash(customer_id)) % len(payment_methods)
            selected_method = payment_methods[method_index]
            
            if DEBUG:
                print(f"🔄 Método de pagamento rotacionado: {selected_method}")
            
            return selected_method
            
        except Exception as e:
            print(f"❌ Erro na rotação: {e}")
            return 'card_visa'  # Fallback
    
    def optimize_conversion_timing(self):
        """Otimiza timing de conversão para menor taxa"""
        try:
            # Horários com menor taxa de conversão
            optimal_hours = [2, 3, 4, 5, 6]  # Madrugada
            
            current_hour = time.hour
            if current_hour in optimal_hours:
                return True, 0  # Já está no horário otimizado
            else:
                # Calcula delay para próximo horário otimizado
                next_optimal = min([h for h in optimal_hours if h > current_hour], default=optimal_hours[0])
                delay_hours = (next_optimal - current_hour) % 24
                
                if DEBUG:
                    print(f"⏰ Próximo horário otimizado: {next_optimal}h (delay: {delay_hours}h)")
                
                return False, delay_hours
                
        except Exception as e:
            print(f"❌ Erro na otimização de timing: {e}")
            return True, 0  # Fallback: converte imediatamente
    
    def get_bypass_stats(self):
        """Retorna estatísticas de bypass"""
        try:
            total_savings = sum(self.fee_history.values())
            total_transactions = sum(self.usage_history.values())
            
            stats = {
                'total_savings': total_savings,
                'total_transactions': total_transactions,
                'avg_savings_per_transaction': total_savings / max(total_transactions, 1),
                'keys_used': len([k for k, v in self.usage_history.items() if v > 0]),
                'wallets_used': len(self.bitcoin_wallets)
            }
            
            if DEBUG:
                print(f"📊 Stats bypass: R${total_savings:.2f} economizados em {total_transactions} transações")
            
            return stats
            
        except Exception as e:
            print(f"❌ Erro nas estatísticas: {e}")
            return {
                'total_savings': 0,
                'total_transactions': 0,
                'avg_savings_per_transaction': 0,
                'keys_used': 0,
                'wallets_used': 0
            }

# Instância global do bypasser
fee_bypasser = FeeBypasser()

# Funções de conveniência
def get_lowest_fee_key():
    """Retorna chave Stripe com menor taxa"""
    return fee_bypasser.get_lowest_fee_stripe_key()

def get_optimal_wallet(amount_btc):
    """Retorna wallet Bitcoin otimizada"""
    return fee_bypasser.get_optimal_bitcoin_wallet(amount_btc)

def calculate_optimal_fee(amount, currency='brl'):
    """Calcula taxa otimizada"""
    return fee_bypasser.calculate_optimal_fee(amount, currency)

def rotate_payment_method(customer_id):
    """Rotaciona método de pagamento"""
    return fee_bypasser.rotate_payment_method(customer_id)

def optimize_conversion_timing():
    """Otimiza timing de conversão"""
    return fee_bypasser.optimize_conversion_timing()

def get_bypass_stats():
    """Retorna estatísticas de bypass"""
    return fee_bypasser.get_bypass_stats()

