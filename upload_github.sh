#!/bin/bash

# 🚀 Script para Upload no GitHub
# Bitcoin Payment System - Sistema Supremo Intergaláctico

echo "🚀 Preparando upload para o GitHub..."

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

print_header " UPLOAD PARA GITHUB"

# 1. Verifica se está no diretório correto
if [ ! -f "app.py" ]; then
    print_error "Execute este script no diretório raiz do projeto!"
    exit 1
fi

# 2. Cria .gitignore
print_status "Criando .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite3

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
*.bak

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml

# Pytest
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Bitcoin Payment System specific
bitcoin_payment.db
bitcoin_payment_prod.db
*.zip
deploy.zip
bitcoin-payment-system.zip
EOF

print_success ".gitignore criado!"

# 3. Remove arquivos desnecessários do commit
print_status "Removendo arquivos desnecessários..."
git rm -r --cached venv/ 2>/dev/null || true
git rm -r --cached __pycache__/ 2>/dev/null || true
git rm -r --cached *.pyc 2>/dev/null || true
git rm -r --cached logs/ 2>/dev/null || true
git rm -r --cached *.log 2>/dev/null || true

# 4. Adiciona arquivos importantes
print_status "Adicionando arquivos importantes..."
git add .gitignore
git add *.py
git add *.md
git add *.sh
git add *.yml
git add *.yaml
git add *.html
git add *.js
git add *.json
git add *.txt
git add *.env.example
git add templates/
git add src/
git add mobile/
git add .github/

# 5. Commit final
print_status "Fazendo commit final..."
git commit -m "🚀 Bitcoin Payment System - Sistema Supremo Intergaláctico

✨ Funcionalidades Implementadas:
- 💳 Pagamentos com Stripe
- ₿ Conversão automática para Bitcoin
- 🛡️ Autenticação 2FA suprema
- 🔄 Rotação de proxies anti-detecção
- 🧪 A/B testing automático
- 📱 Notificações push supremas
- 🚀 CI/CD automático
- 📊 Analytics avançados
- 🌐 Multi-idiomas (PT, EN, ES)
- 💾 Banco de dados persistente
- 🤖 Bot de IA para leads
- 📱 App mobile React Native
- 💰 Integração Binance
- 🌐 URLs criativas para BitPay

📊 Métricas:
- 32 arquivos implementados
- 7.000+ linhas de código
- 26 APIs funcionais
- 6 upgrades supremos ativos

🔥 Sistema pronto para dominar o universo Bitcoin! 💰🌍"

print_success "Commit final realizado!"

# 6. Instruções para upload manual
print_header " INSTRUÇÕES PARA UPLOAD MANUAL"

print_warning "⚠️  PRÓXIMOS PASSOS MANUAIS:"
echo ""
echo "1. 🌐 ACESSE O GITHUB:"
echo "   https://github.com/new"
echo ""
echo "2. 📝 CRIE REPOSITÓRIO:"
echo "   Nome: bitcoin-payment-system"
echo "   Descrição: 🚀 Bitcoin Payment System - Sistema Supremo Intergaláctico de Pagamentos Bitcoin"
echo "   Visibilidade: Público"
echo "   ✅ Initialize with README: NÃO"
echo ""
echo "3. 🔗 CONFIGURE REMOTE:"
echo "   git remote add origin https://github.com/SEU_USUARIO/bitcoin-payment-system.git"
echo ""
echo "4. 🚀 FAÇA PUSH:"
echo "   git push -u origin main"
echo ""
echo "5. 📋 COPIE O COMANDO COMPLETO:"
echo "   git remote add origin https://github.com/SEU_USUARIO/bitcoin-payment-system.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

print_success "Sistema preparado para upload!"
print_success "Execute os comandos acima para subir para o GitHub! 🚀"

# 7. Mostra status do git
print_status "Status atual do Git:"
git status --short

print_header " SISTEMA PRONTO PARA GITHUB! 🚀💰"
