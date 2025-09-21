#!/usr/bin/env python3
"""
Configuração Criativa do BitPay
URLs criativas para o sistema Bitcoin Payment
"""

import requests
import json
import time
from datetime import datetime

# URLs criativas para o sistema
CREATIVE_URLS = {
    "main": "https://bitcoin-payment-hacker.ngrok.io",
    "callback": "https://bitcoin-payment-hacker.ngrok.io/webhook/bitpay",
    "redirect": "https://bitcoin-payment-hacker.ngrok.io/success",
    "dashboard": "https://bitcoin-payment-hacker.ngrok.io/dashboard",
    "health": "https://bitcoin-payment-hacker.ngrok.io/api/health"
}

# Configurações do BitPay
BITPAY_CONFIG = {
    "notificationURL": CREATIVE_URLS["callback"],
    "redirectURL": CREATIVE_URLS["redirect"],
    "orderID": f"bitcoin-payment-{int(time.time())}",
    "itemDesc": "Pagamento Mensal com Conversão para Bitcoin",
    "itemCode": "BTC-PAYMENT-001",
    "posData": json.dumps({
        "system": "Bitcoin Payment System",
        "version": "2.0.0",
        "features": ["2fa", "ab_testing", "push_notifications", "proxy_rotation"],
        "hacker_mode": True,
        "intergalactic": True
    })
}

def print_creative_header():
    """Imprime header criativo"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🚀 BITCOIN PAYMENT SYSTEM - CONFIGURAÇÃO CRIATIVA 🚀       ║
    ║                                                              ║
    ║  💰 Sistema Supremo Intergaláctico de Pagamentos Bitcoin    ║
    ║  🔥 URLs Criativas para Dominar o Universo                  ║
    ║  🌍 Pronto para Faturar Globalmente                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def generate_creative_urls():
    """Gera URLs criativas para o sistema"""
    print("🌐 GERANDO URLs CRIATIVAS...")
    print("")
    
    for name, url in CREATIVE_URLS.items():
        print(f"🔗 {name.upper()}: {url}")
    
    print("")
    print("✅ URLs criativas geradas com sucesso!")
    return CREATIVE_URLS

def create_bitpay_invoice_config():
    """Cria configuração para invoice do BitPay"""
    print("")
    print("🔧 CONFIGURAÇÃO DO BITPAY:")
    print("")
    
    config = {
        "price": 10.00,  # Valor de teste
        "currency": "BRL",
        "notificationURL": CREATIVE_URLS["callback"],
        "redirectURL": CREATIVE_URLS["redirect"],
        "orderID": BITPAY_CONFIG["orderID"],
        "itemDesc": BITPAY_CONFIG["itemDesc"],
        "itemCode": BITPAY_CONFIG["itemCode"],
        "posData": BITPAY_CONFIG["posData"],
        "buyer": {
            "name": "Bitcoin Payment Hacker",
            "email": "hacker@bitcoinpayment.com",
            "address1": "Rua do Bitcoin, 123",
            "city": "São Paulo",
            "state": "SP",
            "zip": "01234-567",
            "country": "BR"
        }
    }
    
    print("📋 Configuração do Invoice:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    return config

def test_creative_urls():
    """Testa se as URLs estão funcionando"""
    print("")
    print("🧪 TESTANDO URLs CRIATIVAS...")
    print("")
    
    for name, url in CREATIVE_URLS.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name.upper()}: Funcionando ({response.status_code})")
            else:
                print(f"⚠️ {name.upper()}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name.upper()}: Erro - {e}")
    
    print("")
    print("✅ Teste de URLs concluído!")

def generate_ngrok_command():
    """Gera comando ngrok criativo"""
    print("")
    print("🚀 COMANDO NGROK CRIATIVO:")
    print("")
    print("ngrok http 5000 --subdomain=bitcoin-payment-hacker")
    print("")
    print("🌐 URLs que serão geradas:")
    print("   https://bitcoin-payment-hacker.ngrok.io")
    print("   https://bitcoin-payment-hacker.ngrok.io/dashboard")
    print("   https://bitcoin-payment-hacker.ngrok.io/webhook/bitpay")
    print("")

def create_bitpay_webhook_handler():
    """Cria handler para webhook do BitPay"""
    print("")
    print("🔧 CRIANDO HANDLER DO WEBHOOK BITPAY...")
    print("")
    
    webhook_code = '''
@app.route('/webhook/bitpay', methods=['POST'])
def bitpay_webhook():
    """Webhook para processar pagamentos do BitPay"""
    try:
        data = request.get_json()
        
        # Log do webhook
        print(f"🔔 Webhook BitPay recebido: {data}")
        
        # Processa pagamento
        if data.get('status') == 'paid':
            # Pagamento confirmado
            amount = data.get('price', 0)
            btc_amount = convert_fiat_to_btc(amount, 'BRL')
            
            # Envia para wallet Bitcoin
            send_to_bitcoin_wallet(btc_amount)
            
            # Registra no histórico
            payments_history.append({
                'id': data.get('id'),
                'amount': amount,
                'currency': 'BRL',
                'btc_amount': btc_amount,
                'status': 'paid',
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ Pagamento processado: R$ {amount:.2f} = {btc_amount:.8f} BTC")
            
        return jsonify({'success': True, 'message': 'Webhook processado'})
        
    except Exception as e:
        print(f"❌ Erro no webhook BitPay: {e}")
        return jsonify({'error': str(e)}), 500
'''
    
    print("📝 Código do webhook criado!")
    print(webhook_code)
    
    return webhook_code

def main():
    """Função principal"""
    print_creative_header()
    
    # Gera URLs criativas
    urls = generate_creative_urls()
    
    # Cria configuração do BitPay
    config = create_bitpay_invoice_config()
    
    # Testa URLs (se ngrok estiver rodando)
    test_creative_urls()
    
    # Gera comando ngrok
    generate_ngrok_command()
    
    # Cria handler do webhook
    webhook_code = create_bitpay_webhook_handler()
    
    print("")
    print("🎉 CONFIGURAÇÃO CRIATIVA CONCLUÍDA!")
    print("")
    print("💰 PRÓXIMOS PASSOS:")
    print("1. Execute: ./ngrok_setup.sh")
    print("2. Configure seu token ngrok")
    print("3. Execute: ./deploy_ngrok.sh")
    print("4. Use as URLs criativas no BitPay")
    print("5. Teste com R$ 10,00")
    print("6. Fature em Bitcoin! 🚀")
    print("")
    print("🔥 Sistema pronto para dominar o universo! 💰🌍")

if __name__ == "__main__":
    main()

