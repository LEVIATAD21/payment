"""
📊 Analytics e Tracking - Bitcoin Payment System
Sistema de analytics para tracking de eventos e estatísticas
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# Cache de eventos (em produção, usar banco de dados)
events_cache = []
analytics_cache = {}

def track_event(event_name: str, properties: Dict[str, Any] = None) -> bool:
    """
    Trackear evento para analytics
    
    Args:
        event_name: Nome do evento
        properties: Propriedades do evento
    
    Returns:
        bool: True se evento foi trackeado com sucesso
    """
    try:
        event = {
            'event': event_name,
            'properties': properties or {},
            'timestamp': datetime.now().isoformat(),
            'session_id': _generate_session_id(),
            'user_id': properties.get('user_id', 'anonymous') if properties else 'anonymous'
        }
        
        events_cache.append(event)
        
        # Atualizar cache de analytics
        _update_analytics_cache(event)
        
        logger.info(f"Evento trackeado: {event_name}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao trackear evento: {str(e)}")
        return False

def get_analytics_stats() -> Dict[str, Any]:
    """
    Obter estatísticas de analytics
    
    Returns:
        Dict com estatísticas
    """
    try:
        # Calcular estatísticas dos últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_events = [
            event for event in events_cache 
            if datetime.fromisoformat(event['timestamp']) >= thirty_days_ago
        ]
        
        # Contar eventos por tipo
        event_counts = {}
        for event in recent_events:
            event_name = event['event']
            event_counts[event_name] = event_counts.get(event_name, 0) + 1
        
        # Calcular conversões
        conversions = _calculate_conversions(recent_events)
        
        # Calcular funnels
        funnels = _calculate_funnels(recent_events)
        
        return {
            'total_events': len(recent_events),
            'event_counts': event_counts,
            'conversions': conversions,
            'funnels': funnels,
            'period': '30_days',
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter stats: {str(e)}")
        return {'error': str(e)}

def _generate_session_id() -> str:
    """Gerar ID de sessão único"""
    return f"session_{int(time.time())}_{hash(str(time.time()))}"

def _update_analytics_cache(event: Dict[str, Any]):
    """Atualizar cache de analytics"""
    event_name = event['event']
    
    if event_name not in analytics_cache:
        analytics_cache[event_name] = {
            'count': 0,
            'last_seen': None,
            'unique_users': set()
        }
    
    analytics_cache[event_name]['count'] += 1
    analytics_cache[event_name]['last_seen'] = event['timestamp']
    analytics_cache[event_name]['unique_users'].add(event['user_id'])

def _calculate_conversions(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcular taxas de conversão"""
    conversions = {
        'payment_conversion': 0,
        'subscription_conversion': 0,
        'crypto_conversion': 0,
        'overall_conversion': 0
    }
    
    try:
        # Contar eventos de interesse
        page_views = len([e for e in events if e['event'] == 'page_view'])
        payments = len([e for e in events if e['event'] == 'payment_created'])
        subscriptions = len([e for e in events if e['event'] == 'subscription_created'])
        crypto_payments = len([e for e in events if e['event'] == 'crypto_payment_created'])
        
        # Calcular conversões
        if page_views > 0:
            conversions['payment_conversion'] = (payments / page_views) * 100
            conversions['subscription_conversion'] = (subscriptions / page_views) * 100
            conversions['crypto_conversion'] = (crypto_payments / page_views) * 100
            conversions['overall_conversion'] = ((payments + subscriptions + crypto_payments) / page_views) * 100
        
        return conversions
        
    except Exception as e:
        logger.error(f"Erro ao calcular conversões: {str(e)}")
        return conversions

def _calculate_funnels(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcular funnels de conversão"""
    funnels = {
        'payment_funnel': {
            'page_view': 0,
            'payment_started': 0,
            'payment_completed': 0,
            'conversion_rate': 0
        },
        'crypto_funnel': {
            'page_view': 0,
            'crypto_selected': 0,
            'crypto_payment_completed': 0,
            'conversion_rate': 0
        }
    }
    
    try:
        # Payment funnel
        page_views = len([e for e in events if e['event'] == 'page_view'])
        payment_started = len([e for e in events if e['event'] == 'payment_started'])
        payment_completed = len([e for e in events if e['event'] == 'payment_completed'])
        
        funnels['payment_funnel']['page_view'] = page_views
        funnels['payment_funnel']['payment_started'] = payment_started
        funnels['payment_funnel']['payment_completed'] = payment_completed
        
        if page_views > 0:
            funnels['payment_funnel']['conversion_rate'] = (payment_completed / page_views) * 100
        
        # Crypto funnel
        crypto_selected = len([e for e in events if e['event'] == 'crypto_selected'])
        crypto_completed = len([e for e in events if e['event'] == 'crypto_payment_completed'])
        
        funnels['crypto_funnel']['page_view'] = page_views
        funnels['crypto_funnel']['crypto_selected'] = crypto_selected
        funnels['crypto_funnel']['crypto_payment_completed'] = crypto_completed
        
        if page_views > 0:
            funnels['crypto_funnel']['conversion_rate'] = (crypto_completed / page_views) * 100
        
        return funnels
        
    except Exception as e:
        logger.error(f"Erro ao calcular funnels: {str(e)}")
        return funnels

def get_event_history(event_name: str = None, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Obter histórico de eventos
    
    Args:
        event_name: Nome do evento (opcional)
        limit: Limite de eventos
    
    Returns:
        Lista de eventos
    """
    try:
        events = events_cache.copy()
        
        if event_name:
            events = [e for e in events if e['event'] == event_name]
        
        # Ordenar por timestamp (mais recentes primeiro)
        events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return events[:limit]
        
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {str(e)}")
        return []

def export_analytics_data() -> Dict[str, Any]:
    """
    Exportar dados de analytics
    
    Returns:
        Dict com todos os dados de analytics
    """
    try:
        return {
            'events': events_cache,
            'analytics_cache': analytics_cache,
            'stats': get_analytics_stats(),
            'exported_at': datetime.now().isoformat(),
            'total_events': len(events_cache)
        }
        
    except Exception as e:
        logger.error(f"Erro ao exportar dados: {str(e)}")
        return {'error': str(e)}

def clear_analytics_data():
    """Limpar dados de analytics (cuidado!)"""
    global events_cache, analytics_cache
    events_cache.clear()
    analytics_cache.clear()
    logger.warning("Dados de analytics limpos!")

# Eventos pré-definidos para tracking
TRACKING_EVENTS = {
    'PAGE_VIEW': 'page_view',
    'PAYMENT_STARTED': 'payment_started',
    'PAYMENT_COMPLETED': 'payment_completed',
    'PAYMENT_FAILED': 'payment_failed',
    'SUBSCRIPTION_CREATED': 'subscription_created',
    'CRYPTO_PAYMENT_CREATED': 'crypto_payment_created',
    'CRYPTO_PAYMENT_COMPLETED': 'crypto_payment_completed',
    '2FA_SETUP': '2fa_setup',
    '2FA_VERIFIED': '2fa_verified',
    'AB_TEST_VIEW': 'ab_test_view',
    'AB_TEST_CONVERSION': 'ab_test_conversion',
    'NOTIFICATION_SENT': 'notification_sent',
    'NOTIFICATION_CLICKED': 'notification_clicked'
}
