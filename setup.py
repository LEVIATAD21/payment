#!/usr/bin/env python3
"""
Setup Automático - Sistema Bitcoin Hacker-Style
"""

import os
import subprocess
import sys
import shutil

def print_banner():
    print("=" * 60)
    print("🚀 SISTEMA DE PAGAMENTOS BITCOIN - HACKER STYLE")
    print("=" * 60)
    print("Setup automático iniciando...")
    print()

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ necessário")
        print(f"   Atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instala dependências"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
        return False

def setup_environment():
    """Configura .env"""
    print("⚙️ Configurando .env...")
    
    if not os.path.exists('.env'):
        if os.path.exists('config.env.example'):
            shutil.copy('config.env.example', '.env')
            print("✅ .env criado")
            print("📝 Configure suas chaves no .env")
        else:
            print("❌ config.env.example não encontrado")
            return False
    else:
        print("ℹ️ .env já existe")
    
    return True

def create_directories():
    """Cria diretórios"""
    print("📁 Criando diretórios...")
    
    dirs = ['logs', 'data', 'backups']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"   ✅ {d}/")
        else:
            print(f"   ℹ️ {d}/ existe")
    
    return True

def show_next_steps():
    """Próximos passos"""
    print("\n" + "=" * 60)
    print("🎉 SETUP CONCLUÍDO!")
    print("=" * 60)
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print()
    print("1. 🔑 Configure .env com suas chaves:")
    print("   - STRIPE_SECRET_KEY (Stripe Dashboard)")
    print("   - BITPAY_API_TOKEN (BitPay)")
    print("   - BITCOIN_WALLET_ADDRESS (Sua wallet)")
    print()
    print("2. 🚀 Execute:")
    print("   python run.py")
    print()
    print("3. 🌐 Acesse:")
    print("   - http://localhost:5000 (Cliente)")
    print("   - http://localhost:5000/dashboard (Admin)")
    print()
    print("4. 🧪 Teste com cartões Stripe:")
    print("   - 4242424242424242 (OK)")
    print("   - 4000000000000002 (Falha)")
    print()
    print("💥 SISTEMA PRONTO PARA HACKEAR!")
    print("=" * 60)

def main():
    """Função principal"""
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not setup_environment():
        sys.exit(1)
    
    if not create_directories():
        sys.exit(1)
    
    show_next_steps()

if __name__ == '__main__':
    main()