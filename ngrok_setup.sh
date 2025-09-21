#!/bin/bash

# 🌐 Script para Configurar URL Pública com Ngrok
# Bitcoin Payment System - URL para BitPay

echo "🌐 Configurando URL pública para BitPay..."

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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header " CONFIGURAÇÃO DE URL PÚBLICA"

# 1. Verifica se ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    print_status "Instalando ngrok..."
    
    # Download ngrok
    wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar xvzf ngrok-v3-stable-linux-amd64.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    
    print_success "Ngrok instalado!"
else
    print_success "Ngrok já está instalado!"
fi

# 2. Cria arquivo de configuração ngrok
print_status "Criando configuração ngrok..."
cat > ngrok.yml << 'EOF'
version: "2"
authtoken: # Adicione seu token aqui
tunnels:
  bitcoin-payment:
    proto: http
    addr: 5000
    subdomain: bitcoin-payment-hacker
    inspect: false
    bind_tls: true
EOF

print_success "Configuração ngrok criada!"

# 3. Cria script de start
print_status "Criando script de start..."
cat > start_ngrok.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando ngrok para Bitcoin Payment System..."
echo "🌐 URL será: https://bitcoin-payment-hacker.ngrok.io"
echo "📱 Acesse: http://localhost:4040 para ver o dashboard ngrok"
echo ""
ngrok start bitcoin-payment
EOF

chmod +x start_ngrok.sh
print_success "Script de start criado!"

# 4. Cria script de deploy
print_status "Criando script de deploy..."
cat > deploy_ngrok.sh << 'EOF'
#!/bin/bash
echo "🚀 Deploy com ngrok - Bitcoin Payment System"
echo ""

# Inicia o sistema em background
echo "🔧 Iniciando sistema..."
source venv/bin/activate
python app.py &
APP_PID=$!

# Aguarda sistema iniciar
sleep 5

# Inicia ngrok
echo "🌐 Iniciando ngrok..."
ngrok start bitcoin-payment &
NGROK_PID=$!

# Aguarda ngrok iniciar
sleep 10

# Pega a URL pública
echo "🔍 Obtendo URL pública..."
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ "$NGROK_URL" != "null" ] && [ ! -z "$NGROK_URL" ]; then
    echo "✅ URL pública obtida: $NGROK_URL"
    echo ""
    echo "🌐 URLs do sistema:"
    echo "   Página principal: $NGROK_URL"
    echo "   Dashboard admin: $NGROK_URL/dashboard"
    echo "   Health check: $NGROK_URL/api/health"
    echo ""
    echo "📱 Dashboard ngrok: http://localhost:4040"
    echo ""
    echo "🔑 Configure no BitPay:"
    echo "   Callback URL: $NGROK_URL/webhook/bitpay"
    echo "   Redirect URL: $NGROK_URL/success"
    echo ""
    echo "💰 Sistema pronto para teste real!"
    echo "   Pressione Ctrl+C para parar"
    
    # Mantém rodando
    wait
else
    echo "❌ Erro ao obter URL do ngrok"
    kill $APP_PID 2>/dev/null
    kill $NGROK_PID 2>/dev/null
    exit 1
fi
EOF

chmod +x deploy_ngrok.sh
print_success "Script de deploy criado!"

# 5. Instala jq se não estiver instalado
if ! command -v jq &> /dev/null; then
    print_status "Instalando jq..."
    sudo apt update
    sudo apt install -y jq
    print_success "Jq instalado!"
fi

print_header " CONFIGURAÇÃO CONCLUÍDA!"

print_warning "⚠️  PRÓXIMOS PASSOS:"
echo ""
echo "1. 🔑 CONFIGURE SEU TOKEN NGROK:"
echo "   - Acesse: https://dashboard.ngrok.com/"
echo "   - Crie conta gratuita"
echo "   - Copie seu token"
echo "   - Cole no arquivo ngrok.yml"
echo ""
echo "2. 🚀 INICIE O SISTEMA:"
echo "   ./deploy_ngrok.sh"
echo ""
echo "3. 🔗 CONFIGURE NO BITPAY:"
echo "   - Use a URL que aparecerá"
echo "   - Callback: https://bitcoin-payment-hacker.ngrok.io/webhook/bitpay"
echo "   - Redirect: https://bitcoin-payment-hacker.ngrok.io/success"
echo ""

print_success "Sistema pronto para URL pública!"
print_success "Agora o BitPay vai funcionar perfeitamente! 🌐💰"

