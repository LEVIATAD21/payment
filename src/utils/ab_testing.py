"""
A/B Testing Automático - Otimização Suprema
Sistema de testes A/B para maximizar conversões
"""

import random
import json
import time
from flask import session, request
from src.config.settings import DEBUG
from src.models.database import SystemStats, db

class ABTesting:
    """Sistema de A/B testing para otimização"""
    
    def __init__(self):
        self.experiments = {
            'homepage_title': {
                'A': 'Pagamento Mensal com Conversão para Bitcoin',
                'B': 'Pague Agora e Ganhe Bitcoin!',
                'C': 'Sistema de Pagamentos Bitcoin - Conversão Automática'
            },
            'cta_button': {
                'A': 'Pagar e Converter',
                'B': 'Comprar Bitcoin Agora',
                'C': 'Converter para BTC'
            },
            'pricing_display': {
                'A': 'Valor (R$)',
                'B': 'Quantidade em Reais',
                'C': 'Valor para Conversão'
            },
            'upsell_message': {
                'A': 'Que tal turbinar seus ganhos?',
                'B': 'Escale seus lucros com Bitcoin!',
                'C': 'Maximize sua receita passiva!'
            }
        }
        
        # Configurações de tráfego
        self.traffic_split = {
            'A': 0.4,  # 40%
            'B': 0.3,  # 30%
            'C': 0.3   # 30%
        }
    
    def get_variant(self, experiment_name, user_id=None):
        """Retorna variante para um experimento"""
        try:
            # Usa user_id se disponível, senão gera baseado na sessão
            if not user_id:
                user_id = session.get('user_id', f"anon_{int(time.time())}")
            
            # Gera seed determinística baseada no user_id
            random.seed(hash(user_id + experiment_name))
            
            # Seleciona variante baseada no tráfego
            rand = random.random()
            cumulative = 0
            
            for variant, percentage in self.traffic_split.items():
                cumulative += percentage
                if rand <= cumulative:
                    selected_variant = variant
                    break
            else:
                selected_variant = 'A'  # Fallback
            
            # Salva na sessão
            if 'ab_tests' not in session:
                session['ab_tests'] = {}
            
            session['ab_tests'][experiment_name] = selected_variant
            
            if DEBUG:
                print(f"🧪 A/B Test: {experiment_name} = {selected_variant} (User: {user_id})")
            
            return selected_variant
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro no A/B testing: {e}")
            return 'A'  # Fallback para variante A
    
    def get_experiment_value(self, experiment_name, user_id=None):
        """Retorna valor da variante do experimento"""
        try:
            variant = self.get_variant(experiment_name, user_id)
            return self.experiments[experiment_name].get(variant, '')
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao obter valor do experimento: {e}")
            return ''
    
    def track_conversion(self, experiment_name, event_type, value=0, user_id=None):
        """Registra conversão de um experimento"""
        try:
            if not user_id:
                user_id = session.get('user_id', f"anon_{int(time.time())}")
            
            variant = session.get('ab_tests', {}).get(experiment_name, 'A')
            
            # Salva no banco de dados
            stat_name = f"ab_test_{experiment_name}_{variant}_{event_type}"
            
            # Busca estatística existente
            stat = SystemStats.query.filter_by(stat_name=stat_name).first()
            
            if stat:
                # Atualiza valor existente
                stat.stat_value += 1
                if value > 0:
                    stat.stat_data = stat.stat_data or {}
                    stat.stat_data['total_value'] = stat.stat_data.get('total_value', 0) + value
                    stat.stat_data['last_conversion'] = time.time()
            else:
                # Cria nova estatística
                stat = SystemStats(
                    stat_name=stat_name,
                    stat_value=1,
                    stat_data={
                        'experiment': experiment_name,
                        'variant': variant,
                        'event_type': event_type,
                        'total_value': value,
                        'first_conversion': time.time(),
                        'last_conversion': time.time()
                    }
                )
                db.session.add(stat)
            
            db.session.commit()
            
            if DEBUG:
                print(f"📊 Conversão registrada: {experiment_name} - {variant} - {event_type}")
            
            return True
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao registrar conversão: {e}")
            return False
    
    def get_experiment_results(self, experiment_name):
        """Retorna resultados de um experimento"""
        try:
            results = {}
            
            for variant in self.traffic_split.keys():
                stat_name = f"ab_test_{experiment_name}_{variant}_conversion"
                stat = SystemStats.query.filter_by(stat_name=stat_name).first()
                
                if stat:
                    results[variant] = {
                        'conversions': stat.stat_value,
                        'data': stat.stat_data or {}
                    }
                else:
                    results[variant] = {
                        'conversions': 0,
                        'data': {}
                    }
            
            return results
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao obter resultados: {e}")
            return {}
    
    def get_winning_variant(self, experiment_name):
        """Retorna variante vencedora de um experimento"""
        try:
            results = self.get_experiment_results(experiment_name)
            
            if not results:
                return 'A'
            
            # Encontra variante com mais conversões
            winning_variant = max(results.keys(), key=lambda k: results[k]['conversions'])
            
            if DEBUG:
                print(f"🏆 Variante vencedora {experiment_name}: {winning_variant}")
            
            return winning_variant
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao determinar vencedor: {e}")
            return 'A'
    
    def get_all_experiments(self):
        """Retorna todos os experimentos disponíveis"""
        return list(self.experiments.keys())
    
    def create_experiment(self, name, variants, traffic_split=None):
        """Cria novo experimento"""
        try:
            self.experiments[name] = variants
            
            if traffic_split:
                self.traffic_split = traffic_split
            
            if DEBUG:
                print(f"✅ Novo experimento criado: {name}")
            
            return True
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao criar experimento: {e}")
            return False

# Instância global
ab_testing = ABTesting()

# Funções de conveniência
def get_ab_variant(experiment_name, user_id=None):
    """Retorna variante A/B"""
    return ab_testing.get_variant(experiment_name, user_id)

def get_ab_value(experiment_name, user_id=None):
    """Retorna valor da variante A/B"""
    return ab_testing.get_experiment_value(experiment_name, user_id)

def track_ab_conversion(experiment_name, event_type, value=0, user_id=None):
    """Registra conversão A/B"""
    return ab_testing.track_conversion(experiment_name, event_type, value, user_id)

def get_ab_results(experiment_name):
    """Retorna resultados A/B"""
    return ab_testing.get_experiment_results(experiment_name)

def get_ab_winner(experiment_name):
    """Retorna vencedor A/B"""
    return ab_testing.get_winning_variant(experiment_name)
