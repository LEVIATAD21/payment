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
