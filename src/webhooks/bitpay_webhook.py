"""
🔗 BitPay Webhook Handler
Processa webhooks do BitPay para atualizar status de pagamentos
"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def handle_bitpay_webhook(payload: bytes) -> Dict[str, Any]:
    """
    Processa webhook do BitPay
    
    Args:
        payload: Dados do webhook em bytes
    
    Returns:
        Dict com resultado do processamento
    """
    try:
        # Decodificar payload
        data = json.loads(payload.decode('utf-8'))
        
        # Verificar tipo de evento
        event_type = data.get('type')
        invoice_data = data.get('data', {})
        
        logger.info(f"BitPay webhook recebido: {event_type}")
        
        if event_type == 'invoice_confirmed':
            return _handle_invoice_confirmed(invoice_data)
        elif event_type == 'invoice_paidInFull':
            return _handle_invoice_paid(invoice_data)
        elif event_type == 'invoice_failedToConfirm':
            return _handle_invoice_failed(invoice_data)
        else:
            logger.warning(f"Tipo de evento não reconhecido: {event_type}")
            return {'success': True, 'message': 'Evento ignorado'}
            
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON do webhook: {e}")
        return {'success': False, 'error': 'JSON inválido'}
    except Exception as e:
        logger.error(f"Erro ao processar webhook BitPay: {e}")
        return {'success': False, 'error': str(e)}

def _handle_invoice_confirmed(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """Processa invoice confirmada"""
    try:
        invoice_id = invoice_data.get('id')
        amount = invoice_data.get('price')
        currency = invoice_data.get('currency')
        
        logger.info(f"Invoice confirmada: {invoice_id} - {amount} {currency}")
        
        # Atualizar status no banco de dados
        # TODO: Implementar atualização no banco
        
        # Enviar notificação
        # TODO: Implementar notificação
        
        return {
            'success': True,
            'message': 'Invoice confirmada processada',
            'invoice_id': invoice_id
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar invoice confirmada: {e}")
        return {'success': False, 'error': str(e)}

def _handle_invoice_paid(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """Processa invoice paga"""
    try:
        invoice_id = invoice_data.get('id')
        amount = invoice_data.get('price')
        currency = invoice_data.get('currency')
        bitcoin_amount = invoice_data.get('btcPaid')
        
        logger.info(f"Invoice paga: {invoice_id} - {amount} {currency} = {bitcoin_amount} BTC")
        
        # Atualizar status no banco de dados
        # TODO: Implementar atualização no banco
        
        # Processar conversão para Bitcoin
        # TODO: Implementar conversão
        
        # Enviar notificação de sucesso
        # TODO: Implementar notificação
        
        return {
            'success': True,
            'message': 'Invoice paga processada',
            'invoice_id': invoice_id,
            'bitcoin_amount': bitcoin_amount
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar invoice paga: {e}")
        return {'success': False, 'error': str(e)}

def _handle_invoice_failed(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """Processa invoice falhada"""
    try:
        invoice_id = invoice_data.get('id')
        reason = invoice_data.get('exceptionStatus')
        
        logger.warning(f"Invoice falhada: {invoice_id} - {reason}")
        
        # Atualizar status no banco de dados
        # TODO: Implementar atualização no banco
        
        # Enviar notificação de falha
        # TODO: Implementar notificação
        
        return {
            'success': True,
            'message': 'Invoice falhada processada',
            'invoice_id': invoice_id,
            'reason': reason
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar invoice falhada: {e}")
        return {'success': False, 'error': str(e)}
