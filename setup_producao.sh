#!/bin/bash

# 🚀 Script de Configuração para Produção Real
# Bitcoin Payment System - Teste com Dinheiro Real

echo "🚀 Configurando sistema para teste REAL com dinheiro!"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header " CONFIGURAÇÃO PARA TESTE REAL"

# 1. Verifica se está no diretório correto
if [ ! -f "app.py" ]; then
    print_error "Execute este script no diretório raiz do projeto!"
    exit 1
fi

# 2. Cria arquivo .env de produção
print_status "Criando arquivo .env para produção..."
cat > .env << 'EOF'
# ========================================
# CONFIGURAÇÃO PARA TESTE REAL
# ========================================

# Stripe (OBRIGATÓRIO - Teste Real)
STRIPE_SECRET_KEY=sk_live_SUA_CHAVE_SECRETA_AQUI
STRIPE_PUBLISHABLE_KEY=pk_live_SUA_CHAVE_PUBLICA_AQUI

# BitPay (OBRIGATÓRIO - Teste Real)
BITPAY_API_TOKEN=seu_token_bitpay_real
BITPAY_PRIVATE_KEY_HEX=sua_chave_privada_hex_real
BITPAY_PUBLIC_KEY_HEX=sua_chave_publica_hex_real

# Bitcoin Wallet (OBRIGATÓRIO - Sua Wallet Real)
BITCOIN_WALLET_ADDRESS=sua_wallet_btc_real

# Binance (OPCIONAL - Para taxas menores)
BINANCE_API_KEY=sua_chave_binance_real
BINANCE_SECRET_KEY=sua_chave_secreta_real

# OneSignal (OPCIONAL - Para notificações push)
ONESIGNAL_APP_ID=seu_app_id_real
ONESIGNAL_API_KEY=sua_api_key_real

# Google Analytics (OPCIONAL - Para analytics)
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

# Mixpanel (OPCIONAL - Para eventos)
MIXPANEL_TOKEN=seu_mixpanel_token_real

# 2FA Configuration
TWO_FACTOR_ISSUER=Bitcoin Payment System
TWO_FACTOR_APP_NAME=Admin Dashboard

# Database (Produção)
SQLALCHEMY_DATABASE_URI=sqlite:///bitcoin_payment_prod.db

# App Configuration
DEBUG=False
APP_SECRET_KEY=sua_chave_secreta_super_segura_aqui
EOF

print_success "Arquivo .env criado!"

# 3. Instala dependências
print_status "Instalando dependências..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Cria diretórios necessários
print_status "Criando diretórios..."
mkdir -p logs
mkdir -p uploads
mkdir -p static/uploads
mkdir -p translations

# 5. Inicializa banco de dados
print_status "Inicializando banco de dados..."
python -c "
from src.models.database import init_database
from app import app
with app.app_context():
    init_database(app)
    print('✅ Banco de dados inicializado!')
"

print_header " CONFIGURAÇÃO CONCLUÍDA!"

print_warning "⚠️  PRÓXIMOS PASSOS OBRIGATÓRIOS:"
echo ""
echo "1. 🔑 CONFIGURE SUAS CHAVES REAIS:"
echo "   - Edite o arquivo .env"
echo "   - Substitua TODAS as chaves de exemplo"
echo "   - Use chaves LIVE do Stripe e BitPay"
echo ""
echo "2. CONFIGURE SUA WALLET BITCOIN:"
echo "   - Coloque sua wallet real no .env"
echo "   - Teste se está funcionando"
echo ""
echo "3. 🧪 TESTE COM VALORES PEQUENOS:"
echo "   - Comece com R$ 1,00"
echo "   - Teste a conversão para BTC"
echo "   - Verifique se chegou na sua wallet"
echo ""
echo "4. MONITORE TUDO:"
echo "   - Acesse http://localhost:5000/dashboard"
echo "   - Verifique logs em tempo real"
echo "   - Monitore conversões"
echo ""

print_success "Sistema pronto para teste REAL!"
print_success "Configure as chaves e vamos faturar! 💰🚀"
