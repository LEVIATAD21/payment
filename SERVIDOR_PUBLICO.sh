#!/bin/bash

echo "🌍 CONFIGURANDO SERVIDOR PÚBLICO SEM NGROK 🌍"
echo ""

# Seu IP público atual
echo "📍 SEU IP PÚBLICO: 179.97.24.22"
echo "📍 SEU IP LOCAL: 192.168.1.18"
echo ""

# Configurar firewall para permitir porta 5000
echo "🔥 Configurando firewall..."
sudo ufw allow 5000
sudo ufw allow 80
sudo ufw allow 443

echo "✅ Firewall configurado!"
echo ""

# Iniciar o sistema na porta 5000 com IP público
echo "🚀 Iniciando sistema Bitcoin Payment..."
cd "/home/jocker/Área de trabalho/pagamento com cartão"
source venv/bin/activate

# Configurar Flask para rodar em todas as interfaces
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000

echo "🌍 Sistema rodando em:"
echo "   - Local: http://localhost:5000"
echo "   - Rede Local: http://192.168.1.18:5000"
echo "   - Público: http://179.97.24.22:5000"
echo ""

# Iniciar o sistema
python run.py

echo ""
echo "🎉 SISTEMA PÚBLICO ATIVO! 🎉"
echo "Acesse: http://179.97.24.22:5000"
echo "Use essa URL no BitPay para webhooks!"


