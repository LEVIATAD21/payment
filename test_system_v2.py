#!/usr/bin/env python3
"""
🧪 Teste Completo do Sistema Bitcoin Payment v2.0
Testa todas as funcionalidades do sistema integrado
"""

import requests
import json
import time
from datetime import datetime

# Configurações
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:5173"

def test_backend_health():
    """Testa health check do backend"""
    print("🔍 Testando health check do backend...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend saudável: {data['status']}")
            print(f"   Versão: {data['version']}")
            print(f"   Serviços: {data['services']}")
            return True
        else:
            print(f"❌ Backend com problemas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar backend: {e}")
        return False

def test_bitcoin_price():
    """Testa API de preço do Bitcoin"""
    print("\n₿ Testando API de preço do Bitcoin...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/bitcoin/price", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Preço Bitcoin obtido:")
            print(f"   CoinGecko: ${data['prices']['coingecko']:,.2f}")
            print(f"   Binance: ${data['prices']['binance']:,.2f}")
            return True
        else:
            print(f"❌ Erro ao obter preço: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar preço Bitcoin: {e}")
        return False

def test_conversion_preview():
    """Testa preview de conversão"""
    print("\n💱 Testando preview de conversão...")
    try:
        data = {
            "amount": 100.00,
            "currency": "brl"
        }
        response = requests.post(f"{BACKEND_URL}/api/convert/preview", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Preview de conversão:")
            print(f"   Valor: R$ {data['amount']}")
            print(f"   Bitcoin: {result['preview']['btc_amount']:.8f} BTC")
            print(f"   Taxa: {result['preview']['conversion_rate']:.2f}%")
            return True
        else:
            print(f"❌ Erro no preview: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar preview: {e}")
        return False

def test_payment_creation():
    """Testa criação de pagamento"""
    print("\n💳 Testando criação de pagamento...")
    try:
        # Teste Stripe Cartão
        data = {
            "email": "teste@exemplo.com",
            "name": "João Silva",
            "amount": 50.00,
            "currency": "brl",
            "method": "stripe"
        }
        response = requests.post(f"{BACKEND_URL}/api/payments/create", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pagamento Stripe criado:")
            print(f"   ID: {result['payment_id']}")
            print(f"   Método: {data['method']}")
            return True
        else:
            print(f"❌ Erro ao criar pagamento: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar pagamento: {e}")
        return False

def test_crypto_payment():
    """Testa pagamento em cripto"""
    print("\n🪙 Testando pagamento em cripto...")
    try:
        data = {
            "email": "teste@exemplo.com",
            "name": "João Silva",
            "amount": 50.00,
            "currency": "usd",
            "method": "stripe_crypto",
            "crypto_currency": "usdc"
        }
        response = requests.post(f"{BACKEND_URL}/api/payments/create", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pagamento crypto criado:")
            print(f"   ID: {result['payment_id']}")
            print(f"   Crypto: {data['crypto_currency']}")
            return True
        else:
            print(f"❌ Erro ao criar pagamento crypto: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar pagamento crypto: {e}")
        return False

def test_bitpay_payment():
    """Testa pagamento BitPay"""
    print("\n₿ Testando pagamento BitPay...")
    try:
        data = {
            "email": "teste@exemplo.com",
            "name": "João Silva",
            "amount": 50.00,
            "currency": "brl",
            "method": "bitpay"
        }
        response = requests.post(f"{BACKEND_URL}/api/payments/create", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pagamento BitPay criado:")
            print(f"   ID: {result['payment_id']}")
            print(f"   Invoice ID: {result['bitpay_invoice_id']}")
            return True
        else:
            print(f"❌ Erro ao criar pagamento BitPay: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar pagamento BitPay: {e}")
        return False

def test_analytics():
    """Testa analytics"""
    print("\n📊 Testando analytics...")
    try:
        # Teste tracking de evento
        event_data = {
            "event": "test_event",
            "properties": {
                "test": True,
                "timestamp": datetime.now().isoformat()
            }
        }
        response = requests.post(f"{BACKEND_URL}/api/analytics/track", 
                               json=event_data, timeout=10)
        if response.status_code == 200:
            print("✅ Evento trackeado com sucesso")
        else:
            print(f"❌ Erro ao trackear evento: {response.status_code}")
        
        # Teste estatísticas
        response = requests.get(f"{BACKEND_URL}/api/analytics/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas obtidas:")
            print(f"   Total de eventos: {stats['stats']['analytics']['total_events']}")
            return True
        else:
            print(f"❌ Erro ao obter stats: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar analytics: {e}")
        return False

def test_2fa():
    """Testa 2FA"""
    print("\n🔐 Testando 2FA...")
    try:
        # Setup 2FA
        response = requests.post(f"{BACKEND_URL}/api/auth/2fa/setup", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 2FA setup criado:")
            print(f"   QR Code: {result['qr_code'][:50]}...")
            print(f"   Backup codes: {len(result['backup_codes'])} códigos")
            return True
        else:
            print(f"❌ Erro no setup 2FA: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar 2FA: {e}")
        return False

def test_ab_testing():
    """Testa A/B Testing"""
    print("\n🧪 Testando A/B Testing...")
    try:
        # Obter variante
        response = requests.get(f"{BACKEND_URL}/api/ab-test/variant?experiment=payment_page&user_id=test_user", 
                              timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Variante A/B obtida:")
            print(f"   Experimento: {result['experiment']}")
            print(f"   Variante: {result['variant']}")
            
            # Tracking de conversão
            conversion_data = {
                "experiment": "payment_page",
                "variant": result['variant'],
                "user_id": "test_user"
            }
            response = requests.post(f"{BACKEND_URL}/api/ab-test/conversion", 
                                   json=conversion_data, timeout=10)
            if response.status_code == 200:
                print("✅ Conversão A/B trackeada")
                return True
            else:
                print(f"❌ Erro ao trackear conversão: {response.status_code}")
                return False
        else:
            print(f"❌ Erro ao obter variante: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar A/B: {e}")
        return False

def test_notifications():
    """Testa notificações"""
    print("\n🔔 Testando notificações...")
    try:
        data = {
            "user_id": "test_user",
            "message": "Teste de notificação",
            "type": "payment"
        }
        response = requests.post(f"{BACKEND_URL}/api/notifications/send", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Notificação enviada:")
            print(f"   Status: {result['notification_sent']}")
            return True
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar notificações: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA BITCOIN PAYMENT v2.0")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_backend_health),
        ("Preço Bitcoin", test_bitcoin_price),
        ("Preview Conversão", test_conversion_preview),
        ("Pagamento Stripe", test_payment_creation),
        ("Pagamento Crypto", test_crypto_payment),
        ("Pagamento BitPay", test_bitpay_payment),
        ("Analytics", test_analytics),
        ("2FA", test_2fa),
        ("A/B Testing", test_ab_testing),
        ("Notificações", test_notifications)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro crítico no teste {test_name}: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Pausa entre testes
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"Total: {passed}/{total} testes passaram")
    print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema funcionando perfeitamente!")
    elif passed >= total * 0.8:
        print("\n⚠️  Maioria dos testes passou. Sistema funcional com pequenos problemas.")
    else:
        print("\n❌ Muitos testes falharam. Sistema precisa de correções.")
    
    print("\n🚀 Sistema Bitcoin Payment v2.0 testado com sucesso!")

if __name__ == "__main__":
    main()
