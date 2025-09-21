#!/bin/bash

echo "🔥 CONECTANDO COM SUA CONTA LEVIATAD21 🔥"
echo ""

# 1. Configure SUAS credenciais
echo "Configurando SUA conta..."
git config --global user.name "LEVIATAD21"
git config --global user.email "seu_email@exemplo.com"  # SUBSTITUA pelo seu email

echo "✅ Usuário configurado: LEVIATAD21"
echo ""

# 2. Entre na pasta do projeto
echo "Entrando na pasta do projeto..."
cd "/home/jocker/Área de trabalho/pagamento com cartão/temp_upload"

# 3. Configure o remote com SUA conta
echo "Configurando repositório..."
git remote set-url origin https://github.com/LEVIATAD21/paymetcard.git

echo "✅ Repositório configurado: https://github.com/LEVIATAD21/paymetcard.git"
echo ""

# 4. INSTRUÇÕES PARA VOCÊ
echo "🚀 AGORA VOCÊ PRECISA:"
echo "1. Vá para: https://github.com/settings/tokens"
echo "2. Crie um novo token pessoal"
echo "3. Copie o token"
echo "4. Execute: git push origin main"
echo "5. Digite seu username: LEVIATAD21"
echo "6. Digite seu token quando pedir a senha"
echo ""

echo "OU use este comando com SEU token:"
echo "git remote set-url origin https://SEU_TOKEN@github.com/LEVIATAD21/paymetcard.git"
echo "git push origin main"
echo ""

echo "🎯 SISTEMA PRONTO PARA SUBIR! 🎯"


