# Sistema de Pagamentos com Cartão Convertido para Bitcoin

Este sistema permite aceitar pagamentos mensais via cartão de crédito e converter automaticamente para Bitcoin, enviando os fundos para sua wallet Bitcoin.

## 🚀 Funcionalidades

- **Pagamentos Únicos**: Aceita pagamentos únicos via cartão de crédito/débito
- **Assinaturas Mensais**: Sistema de cobrança recorrente automática
- **Conversão Automática**: Converte pagamentos em fiat (R$) para Bitcoin automaticamente
- **Interface Web**: Dashboard completo para gerenciar pagamentos e assinaturas
- **Webhooks**: Processamento automático de pagamentos via webhooks do Stripe
- **Taxa de Conversão**: Aplica taxa de 1% na conversão (configurável)

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Pagamentos**: Stripe API
- **Conversão Bitcoin**: BitPay API + CoinGecko API
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Gráficos**: Chart.js

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Stripe (modo teste ou produção)
- Conta no BitPay (opcional, para conversão real)
- Wallet Bitcoin para receber os fundos

## 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd pagamento-com-cartao
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**:
```bash
cp config.env.example .env
```

Edite o arquivo `.env` com suas chaves:
```env
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# BitPay Configuration (opcional)
BITPAY_API_KEY=your_bitpay_api_key
BITPAY_MERCHANT_TOKEN=your_merchant_token
BITPAY_WALLET_ADDRESS=your_bitcoin_wallet_address

# Flask Configuration
SECRET_KEY=your_secret_key_here
```

4. **Execute a aplicação**:
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🔑 Configuração das APIs

### Stripe

1. Acesse [Stripe Dashboard](https://dashboard.stripe.com)
2. Obtenha suas chaves de API (modo teste)
3. Configure webhooks apontando para `/webhook/stripe`
4. Eventos necessários:
   - `payment_intent.succeeded`
   - `invoice.payment_succeeded`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`

### BitPay (Opcional)

1. Acesse [BitPay](https://bitpay.com)
2. Crie uma conta de merchant
3. Obtenha sua API key e merchant token
4. Configure o endereço da sua wallet Bitcoin

## 📱 Como Usar

### Para Clientes

1. Acesse a página principal
2. Preencha seus dados (email, nome, valor)
3. Escolha entre pagamento único ou assinatura mensal
4. Insira os dados do cartão
5. Confirme o pagamento

### Para Administradores

1. Acesse `/dashboard` para gerenciar o sistema
2. Visualize estatísticas de conversões
3. Gerencie assinaturas ativas
4. Monitore pagamentos processados

## 🔄 Fluxo de Funcionamento

1. **Cliente faz pagamento** com cartão via Stripe
2. **Webhook é disparado** quando pagamento é confirmado
3. **Sistema calcula conversão** de R$ para Bitcoin
4. **Bitcoin é enviado** para sua wallet configurada
5. **Confirmação é enviada** por email (implementar)

## 💰 Taxas e Limites

- **Taxa de Conversão**: 1% (configurável)
- **Valor Mínimo**: R$ 10,00
- **Valor Máximo**: R$ 10.000,00
- **Taxa Stripe**: ~2.9% + R$ 0,39 por transação
- **Taxa BitPay**: ~1% para conversão

## 🛡️ Segurança

- Todas as chaves de API são armazenadas em variáveis de ambiente
- Webhooks são verificados com assinatura do Stripe
- Validação de valores e dados de entrada
- Logs de todas as operações importantes

## 📊 Monitoramento

O dashboard fornece:
- Preço atual do Bitcoin em tempo real
- Histórico de pagamentos processados
- Estatísticas de conversões
- Gráficos de performance
- Gerenciamento de assinaturas

## 🚨 Modo de Desenvolvimento

Para testar o sistema:

1. Use cartões de teste do Stripe:
   - `4242424242424242` (Visa)
   - `4000000000000002` (Visa recusado)
   - `4000000000009995` (Saldo insuficiente)

2. Configure webhooks localmente usando ngrok:
```bash
ngrok http 5000
```

3. Use o URL do ngrok nos webhooks do Stripe

## 📝 Estrutura do Projeto

```
pagamento-com-cartao/
├── src/
│   ├── api/
│   │   ├── stripe_handler.py      # Integração com Stripe
│   │   └── bitpay_handler.py      # Integração com BitPay
│   ├── webhooks/
│   │   └── stripe_webhook.py      # Processamento de webhooks
│   ├── utils/
│   │   └── bitcoin_converter.py   # Conversão para Bitcoin
│   └── config/
│       └── settings.py            # Configurações
├── templates/
│   ├── index.html                 # Página principal
│   └── dashboard.html             # Dashboard admin
├── static/
│   ├── css/
│   │   ├── style.css              # Estilos principais
│   │   └── dashboard.css          # Estilos do dashboard
│   └── js/
│       ├── app.js                 # JavaScript principal
│       └── dashboard.js           # JavaScript do dashboard
├── app.py                         # Aplicação Flask principal
├── requirements.txt               # Dependências Python
├── config.env.example            # Exemplo de configuração
└── README.md                     # Este arquivo
```

## 🔧 Personalização

### Alterar Taxa de Conversão

Edite `src/config/settings.py`:
```python
CONVERSION_FEE_PERCENTAGE = 0.02  # 2% em vez de 1%
```

### Alterar Limites de Pagamento

```python
MINIMUM_PAYMENT_AMOUNT = 20  # R$ 20,00 mínimo
MAXIMUM_PAYMENT_AMOUNT = 50000  # R$ 50.000,00 máximo
```

### Adicionar Novas Moedas

Modifique `bitcoin_converter.py` para suportar outras moedas além do Real.

## 🐛 Solução de Problemas

### Erro de Chaves de API
- Verifique se as chaves estão corretas no arquivo `.env`
- Certifique-se de que está usando as chaves do modo correto (teste/produção)

### Webhooks não funcionam
- Verifique se o endpoint está acessível publicamente
- Confirme se a assinatura do webhook está correta
- Verifique os logs da aplicação

### Conversão não funciona
- Verifique se a API do CoinGecko está acessível
- Confirme se o endereço da wallet está correto
- Verifique os logs de erro

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs da aplicação
2. Consulte a documentação das APIs (Stripe, BitPay)
3. Abra uma issue no repositório

## ⚖️ Considerações Legais

- Declare os Bitcoin recebidos na Receita Federal
- Use exchanges reguladas se precisar converter para fiat
- Mantenha registros de todas as transações
- Consulte um advogado para questões específicas do seu país

## 🔄 Atualizações Futuras

- [ ] Integração com mais exchanges
- [ ] Suporte a outras criptomoedas
- [ ] Sistema de notificações por email
- [ ] API REST completa
- [ ] Banco de dados para persistência
- [ ] Sistema de relatórios avançado
- [ ] Integração com contabilidade

---

**⚠️ Aviso**: Este é um sistema de demonstração. Para uso em produção, implemente todas as medidas de segurança necessárias e consulte profissionais qualificados.
