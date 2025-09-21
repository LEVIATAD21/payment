#!/bin/bash

echo "🔥 CONFIGURANDO SUAS CREDENCIAIS GITHUB - LEVIATAD21 🔥"
echo ""

# 1. Configure suas credenciais
echo "Configurando usuário..."
git config --global user.name "LEVIATAD21"
git config --global user.email "leviatad21@github.com"

echo "✅ Usuário configurado: LEVIATAD21"
echo ""

# 2. Entre na pasta do projeto
echo "Entrando na pasta do projeto..."
cd "/home/jocker/Área de trabalho/pagamento com cartão/temp_upload"

# 3. Configure o remote
echo "Configurando repositório..."
git remote set-url origin https://github.com/LEVIATAD21/paymetcard.git

echo "✅ Repositório configurado: https://github.com/LEVIATAD21/paymetcard.git"
echo ""

# 4. Faça o push com token
echo "🚀 FAZENDO PUSH COM SEU TOKEN..."
echo "Use o token: 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"
echo ""

# Configure o token no URL
git remote set-url origin https://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@github.com/LEVIATAD21/paymetcard.git

echo "Fazendo push..."
git push origin main

echo ""
echo "🎉 SISTEMA ENVIADO PARA SEU GITHUB! 🎉"
echo "Acesse: https://github.com/LEVIATAD21/paymetcard"


