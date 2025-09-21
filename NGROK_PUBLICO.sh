#!/bin/bash

echo "🌍 CONFIGURANDO IP PÚBLICO COM NGROK 🌍"
echo ""

# Seu IP público atual
echo "📍 SEU IP PÚBLICO: 179.97.24.22"
echo "📍 SEU IP LOCAL: 192.168.1.18"
echo ""

# Instalar ngrok
echo "📦 Instalando Ngrok..."
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
rm ngrok-v3-stable-linux-amd64.tgz

echo "✅ Ngrok instalado!"
echo ""

# Configurar ngrok
echo "🔧 Configurando Ngrok..."
echo "1. Vá para: https://dashboard.ngrok.com/signup"
echo "2. Crie uma conta gratuita"
echo "3. Copie seu authtoken"
echo "4. Execute: ngrok config add-authtoken SEU_TOKEN"
echo ""

# Iniciar ngrok
echo "🚀 Iniciando servidor público..."
echo "Executando: ngrok http 5000"
echo ""

# Iniciar o sistema
echo "🔥 Iniciando sistema Bitcoin Payment..."
cd "/home/jocker/Área de trabalho/pagamento com cartão"
source venv/bin/activate
python run.py &

# Aguardar um pouco
sleep 3

# Iniciar ngrok
echo "🌍 Expondo para o mundo..."
ngrok http 5000

echo ""
echo "🎉 SISTEMA PÚBLICO ATIVO! 🎉"
echo "Acesse a URL pública que aparecerá acima!"
echo "Use essa URL no BitPay para webhooks!"


