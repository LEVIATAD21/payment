#!/bin/bash

echo "🚀 INICIANDO SISTEMA BITCOIN PAYMENT v2.0 COM DESIGN MODERNO"
echo "============================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🎯 $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "app_v2.py" ]; then
    print_error "Execute este script no diretório raiz do projeto!"
    exit 1
fi

print_header "VERIFICANDO DEPENDÊNCIAS..."

# Verificar Python
if command -v python3 &> /dev/null; then
    print_status "Python3 encontrado"
else
    print_error "Python3 não encontrado!"
    exit 1
fi

# Verificar Node.js
if command -v node &> /dev/null; then
    print_status "Node.js encontrado"
else
    print_error "Node.js não encontrado!"
    exit 1
fi

# Verificar npm
if command -v npm &> /dev/null; then
    print_status "npm encontrado"
else
    print_error "npm não encontrado!"
    exit 1
fi

print_header "PREPARANDO AMBIENTE..."

# Ativar ambiente virtual Python
if [ -d "venv" ]; then
    print_info "Ativando ambiente virtual Python..."
    source venv/bin/activate
    print_status "Ambiente virtual ativado"
else
    print_warning "Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    print_status "Ambiente virtual criado e dependências instaladas"
fi

# Verificar dependências do frontend
if [ -d "frontend/node_modules" ]; then
    print_status "Dependências do frontend encontradas"
else
    print_info "Instalando dependências do frontend..."
    cd frontend
    npm install
    cd ..
    print_status "Dependências do frontend instaladas"
fi

print_header "INICIANDO SISTEMA..."

# Função para limpar processos ao sair
cleanup() {
    print_info "Parando processos..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    print_status "Sistema parado com sucesso!"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Iniciar Backend
print_info "Iniciando Backend v2.0..."
python app_v2.py &
BACKEND_PID=$!
print_status "Backend iniciado com PID: $BACKEND_PID"

# Aguardar backend inicializar
sleep 3

# Verificar se backend está rodando
if curl -s http://localhost:5000/api/health > /dev/null; then
    print_status "Backend funcionando em http://localhost:5000"
else
    print_warning "Backend pode não estar funcionando corretamente"
fi

# Iniciar Frontend
print_info "Iniciando Frontend v2.0 com design moderno..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..
print_status "Frontend iniciado com PID: $FRONTEND_PID"

# Aguardar frontend inicializar
sleep 5

print_header "🎉 SISTEMA INICIADO COM SUCESSO!"
echo ""
echo -e "${CYAN}🌐 URLs Disponíveis:${NC}"
echo -e "   ${GREEN}Frontend (Design Moderno):${NC} http://localhost:5173"
echo -e "   ${GREEN}Backend API:${NC} http://localhost:5000"
echo -e "   ${GREEN}Health Check:${NC} http://localhost:5000/api/health"
echo -e "   ${GREEN}Dashboard:${NC} http://localhost:5173/dashboard"
echo ""
echo -e "${CYAN}🎨 Recursos do Design:${NC}"
echo -e "   ${GREEN}• Landing Page moderna${NC} com gradientes e animações"
echo -e "   ${GREEN}• Navegação responsiva${NC} com menu mobile"
echo -e "   ${GREEN}• Contadores animados${NC} para estatísticas"
echo -e "   ${GREEN}• Cards interativos${NC} com hover effects"
echo -e "   ${GREEN}• Seção de preços${NC} com planos detalhados"
echo -e "   ${GREEN}• Depoimentos${NC} com avaliações"
echo -e "   ${GREEN}• Footer completo${NC} com links organizados"
echo ""
echo -e "${CYAN}💳 Funcionalidades:${NC}"
echo -e "   ${GREEN}• 3 métodos de pagamento${NC} (Stripe, Crypto, BitPay)"
echo -e "   ${GREEN}• Dashboard completo${NC} com analytics"
echo -e "   ${GREEN}• Sistema 2FA${NC} para segurança"
echo -e "   ${GREEN}• A/B Testing${NC} integrado"
echo -e "   ${GREEN}• Notificações push${NC}"
echo ""
echo -e "${YELLOW}Pressione Ctrl+C para parar o sistema${NC}"
echo ""

# Manter script rodando
while true; do
    sleep 1
done
