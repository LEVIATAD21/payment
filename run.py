#!/usr/bin/env python3
"""
Sistema de Pagamentos Bitcoin - Script de Execução Hacker-Style
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Verifica se as variáveis de ambiente estão configuradas
    required_vars = [
        'STRIPE_SECRET_KEY',
        'BITPAY_API_TOKEN',
        'BITCOIN_WALLET_ADDRESS'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ ERRO: Variáveis de ambiente não configuradas:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Configure no arquivo .env:")
        print("   cp config.env.example .env")
        print("   # Edite .env com suas chaves")
        sys.exit(1)
    
    print("🚀 SISTEMA DE PAGAMENTOS BITCOIN INICIANDO...")
    print("=" * 50)
    print("📱 Página Principal: http://localhost:5000")
    print("📊 Dashboard Admin: http://localhost:5000/dashboard")
    print("🔧 API Endpoints: /api/*")
    print("🪝 Webhooks: /webhook/stripe")
    print("=" * 50)
    print("🛑 Para parar: Ctrl+C")
    print("=" * 50)
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar: {e}")
        sys.exit(1)
