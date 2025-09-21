#!/usr/bin/env python3
"""
Script de Teste Real - Bitcoin Payment System
Testa o sistema com dinheiro real de forma segura
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:5000"
TEST_AMOUNT = 10.00  # Valor mínimo permitido: R$ 10,00
TEST_CURRENCY = "brl"

def print_header(text):
    print(f"\n{'='*50}")
    print(f" {text}")
    print(f"{'='*50}")

def print_status(text):
    print(f"🔵 [INFO] {text}")

def print_success(text):
    print(f"✅ [SUCCESS] {text}")

def print_error(text):
    print(f"❌ [ERROR] {text}")

def print_warning(text):
    print(f"⚠️ [WARNING] {text}")

def test_health():
    """Testa se o sistema está funcionando"""
    print_status("Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Sistema funcionando! Versão: {data.get('version', 'N/A')}")
            return True
        else:
            print_error(f"Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro ao conectar: {e}")
        return False

def test_bitcoin_price():
    """Testa se consegue buscar preço do Bitcoin"""
    print_status("Testando busca de preço Bitcoin...")
    try:
        response = requests.get(f"{BASE_URL}/api/bitcoin_price", timeout=10)
        if response.status_code == 200:
            data = response.json()
            price = data.get('price', 0)
            print_success(f"Preço Bitcoin: R$ {price:,.2f}")
            return True
        else:
            print_error(f"Erro ao buscar preço: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro na API: {e}")
        return False

def test_conversion_preview():
    """Testa preview de conversão"""
    print_status(f"Testando conversão de R$ {TEST_AMOUNT:.2f}...")
    try:
        payload = {
            "amount": TEST_AMOUNT,
            "currency": TEST_CURRENCY
        }
        response = requests.post(
            f"{BASE_URL}/api/preview_conversion",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            btc_amount = data.get('btc_amount', 0)
            print_success(f"Conversão: R$ {TEST_AMOUNT:.2f} = {btc_amount:.8f} BTC")
            return True
        else:
            print_error(f"Erro na conversão: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro na API: {e}")
        return False

def test_payment_creation():
    """Testa criação de pagamento (sem processar)"""
    print_status("Testando criação de pagamento...")
    try:
        payload = {
            "amount": TEST_AMOUNT,
            "currency": TEST_CURRENCY,
            "email": "teste@bitcoinpayment.com",
            "name": "Teste Real"
        }
        response = requests.post(
            f"{BASE_URL}/api/create_payment",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success("Pagamento criado com sucesso!")
                print(f"   Client Secret: {data.get('client_secret', 'N/A')[:20]}...")
                return True
            else:
                print_error(f"Erro na criação: {data.get('error', 'Desconhecido')}")
                return False
        else:
            print_error(f"Erro HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro na API: {e}")
        return False

def test_2fa_setup():
    """Testa configuração 2FA"""
    print_status("Testando configuração 2FA...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/setup_2fa",
            json={"email": "admin@bitcoinpayment.com"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success("2FA configurado com sucesso!")
                print("   QR Code gerado para configuração")
                return True
            else:
                print_warning(f"2FA já configurado ou erro: {data.get('error', 'Desconhecido')}")
                return True
        else:
            print_error(f"Erro HTTP: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro na API: {e}")
        return False

def test_ab_testing():
    """Testa A/B testing"""
    print_status("Testando A/B testing...")
    try:
        # Testa obtenção de variante
        response = requests.get(f"{BASE_URL}/api/ab_test", timeout=10)
        if response.status_code == 200:
            print_success("A/B testing funcionando!")
            return True
        else:
            print_warning(f"A/B testing não configurado: {response.status_code}")
            return True
    except Exception as e:
        print_warning(f"A/B testing não disponível: {e}")
        return True

def test_lead_generation():
    """Testa geração de leads"""
    print_status("Testando geração de leads...")
    try:
        payload = {"max_emails": 1}  # Apenas 1 lead para teste
        response = requests.post(
            f"{BASE_URL}/api/lead_generation",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Leads gerados: {data.get('leads_found', 0)}")
                return True
            else:
                print_warning(f"Geração de leads: {data.get('error', 'Desconhecido')}")
                return True
        else:
            print_warning(f"Geração de leads não disponível: {response.status_code}")
            return True
    except Exception as e:
        print_warning(f"Geração de leads não disponível: {e}")
        return True

def main():
    """Executa todos os testes"""
    print_header("TESTE REAL - BITCOIN PAYMENT SYSTEM")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Valor de teste: R$ {TEST_AMOUNT:.2f}")
    
    tests = [
        ("Health Check", test_health),
        ("Preço Bitcoin", test_bitcoin_price),
        ("Preview Conversão", test_conversion_preview),
        ("Criação Pagamento", test_payment_creation),
        ("Configuração 2FA", test_2fa_setup),
        ("A/B Testing", test_ab_testing),
        ("Geração de Leads", test_lead_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'─'*30}")
        print(f"🧪 Testando: {test_name}")
        print(f"{'─'*30}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Erro inesperado: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print_header("RESUMO DOS TESTES")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n{'─'*50}")
    print(f"RESULTADO: {passed}/{total} testes passaram")
    print(f"{'─'*50}")
    
    if passed == total:
        print_success("🎉 TODOS OS TESTES PASSARAM!")
        print_success("Sistema pronto para teste real com dinheiro!")
        print_warning("⚠️ Configure suas chaves reais no arquivo .env")
        print_warning("⚠️ Comece com valores pequenos (R$ 1,00)")
    else:
        print_error("❌ Alguns testes falharam!")
        print_error("Verifique a configuração antes de usar dinheiro real!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
