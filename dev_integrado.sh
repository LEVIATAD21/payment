#!/bin/bash

# 🚀 Script para desenvolvimento integrado
# Executa backend e frontend simultaneamente

echo "🔥 Iniciando desenvolvimento integrado..."
echo "📁 Backend: Python/Flask (porta 5000)"
echo "📁 Frontend: React/TypeScript (porta 5173)"
echo ""

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo "🛑 Parando servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Verificar se as dependências estão instaladas
echo "🔍 Verificando dependências..."

# Backend
if [ ! -f "venv/bin/activate" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv venv
fi

echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

# Frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Instalando dependências Node.js..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "🚀 Iniciando servidores..."

# Iniciar backend em background
echo "🐍 Iniciando backend Flask..."
python app.py &
BACKEND_PID=$!

# Aguardar backend inicializar
sleep 3

# Iniciar frontend em background
echo "⚛️  Iniciando frontend React..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servidores iniciados com sucesso!"
echo ""
echo "🌐 URLs disponíveis:"
echo "   Backend:  http://localhost:5000"
echo "   Frontend: http://localhost:5173"
echo "   APIs:     http://localhost:5000/api/*"
echo ""
echo "💡 Pressione Ctrl+C para parar os servidores"
echo ""

# Aguardar processos
wait $BACKEND_PID $FRONTEND_PID
