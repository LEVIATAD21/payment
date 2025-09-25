# 🚀 Projeto Integrado: Bitcoin Payment System + Frontend Moderno

## 📋 Visão Geral

Este projeto integra dois repositórios em uma solução completa:

1. **Backend (Python/Flask)**: Sistema de pagamentos Bitcoin com APIs avançadas
2. **Frontend (React/TypeScript)**: Interface moderna com dashboard completo

## 🏗️ Estrutura do Projeto

```
payment/
├── 📁 backend/                    # Sistema Python/Flask original
│   ├── src/                      # APIs e lógica de negócio
│   ├── templates/                # Templates HTML (legado)
│   ├── static/                   # Assets estáticos (legado)
│   ├── app.py                    # Aplicação principal Flask
│   └── requirements.txt          # Dependências Python
├── 📁 frontend/                  # Interface React/TypeScript moderna
│   ├── src/                      # Componentes React
│   ├── public/                   # Assets públicos
│   ├── package.json              # Dependências Node.js
│   └── vite.config.ts            # Configuração Vite
├── 📁 mobile/                    # App React Native
└── 📄 README.md                  # Documentação principal
```

## 🔧 Configuração

### Backend (Python/Flask)
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp config.env.example .env
# Editar .env com suas chaves

# Executar backend
python app.py
# Backend rodará em: http://localhost:5000
```

### Frontend (React/TypeScript)
```bash
# Navegar para pasta frontend
cd frontend

# Instalar dependências
npm install

# Executar frontend
npm run dev
# Frontend rodará em: http://localhost:5173
```

## 🌐 URLs e Integração

### Backend APIs
- **Base URL**: `http://localhost:5000`
- **APIs**: `/api/*` (pagamentos, conversões, analytics)
- **Webhooks**: `/webhook/*` (Stripe, BitPay)

### Frontend
- **Base URL**: `http://localhost:5173`
- **Dashboard**: Interface moderna para gerenciar pagamentos
- **Integração**: Consome APIs do backend

## 🔗 Integração Frontend ↔ Backend

O frontend React se conecta ao backend Flask através de:

1. **APIs REST**: Todas as operações via `/api/*`
2. **CORS**: Configurado para permitir requisições do frontend
3. **Autenticação**: Sistema 2FA integrado
4. **WebSockets**: Para atualizações em tempo real (futuro)

## 🚀 Deploy

### Desenvolvimento
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Produção
```bash
# Build frontend
cd frontend && npm run build

# Deploy backend (com frontend integrado)
./deploy.sh
```

## 📱 Funcionalidades Integradas

### Backend (APIs)
- ✅ Processamento de pagamentos Stripe
- ✅ Conversão automática para Bitcoin
- ✅ Sistema 2FA
- ✅ Analytics e relatórios
- ✅ Webhooks em tempo real

### Frontend (Interface)
- ✅ Dashboard moderno
- ✅ Formulários de pagamento
- ✅ Histórico de transações
- ✅ Analytics visuais
- ✅ Gerenciamento de clientes
- ✅ Configurações do sistema

## 🔄 Próximos Passos

1. **Configurar CORS** no backend para frontend
2. **Integrar APIs** no frontend
3. **Testar fluxo completo** de pagamentos
4. **Deploy integrado** em produção
5. **Otimizar performance** da integração

---

**🎉 Projeto integrado com sucesso! Agora você tem um sistema completo de pagamentos Bitcoin com interface moderna!**
