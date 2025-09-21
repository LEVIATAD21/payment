// Sistema de Pagamentos Bitcoin - JavaScript Hacker-Style
let isLoading = false;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadBitcoinPrice();
    setupEventListeners();
});

// Event listeners
function setupEventListeners() {
    // Preview da conversão quando valor muda
    document.getElementById('amount').addEventListener('input', function() {
        const amount = parseFloat(this.value);
        if (amount >= 10) {
            showConversionPreview(amount);
        } else {
            hideConversionPreview();
        }
    });
    
    // Submit do formulário
    document.getElementById('payment-form').addEventListener('submit', handleFormSubmit);
}

// Carrega preço do Bitcoin
async function loadBitcoinPrice() {
    try {
        const response = await fetch('/api/bitcoin_price?currency=brl');
        const data = await response.json();
        
        if (data.success) {
            const priceElement = document.getElementById('btc-price');
            priceElement.textContent = `R$ ${data.price.toLocaleString('pt-BR', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}`;
        }
    } catch (error) {
        console.error('Erro ao carregar preço:', error);
        document.getElementById('btc-price').textContent = 'Erro ao carregar';
    }
}

// Mostra preview da conversão
async function showConversionPreview(amount) {
    try {
        const response = await fetch('/api/preview_conversion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: amount, currency: 'brl' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('preview-details').innerHTML = `
                <div class="row">
                    <div class="col-6"><strong>Valor Original:</strong></div>
                    <div class="col-6">R$ ${data.original_amount.toLocaleString('pt-BR', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })}</div>
                </div>
                <div class="row">
                    <div class="col-6"><strong>Taxa (1%):</strong></div>
                    <div class="col-6">R$ ${data.fee_amount.toLocaleString('pt-BR', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })}</div>
                </div>
                <div class="row">
                    <div class="col-6"><strong>Valor Líquido:</strong></div>
                    <div class="col-6">R$ ${data.amount_after_fee.toLocaleString('pt-BR', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })}</div>
                </div>
                <div class="row">
                    <div class="col-6"><strong>Bitcoin Recebido:</strong></div>
                    <div class="col-6 text-success fw-bold">${data.btc_amount.toFixed(8)} BTC</div>
                </div>
                <div class="row">
                    <div class="col-6"><strong>Preço BTC:</strong></div>
                    <div class="col-6">R$ ${data.btc_price.toLocaleString('pt-BR', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })}</div>
                </div>
            `;
            document.getElementById('preview').style.display = 'block';
        }
    } catch (error) {
        console.error('Erro ao calcular conversão:', error);
    }
}

// Esconde preview
function hideConversionPreview() {
    document.getElementById('preview').style.display = 'none';
}

// Manipula submit do formulário
async function handleFormSubmit(event) {
    event.preventDefault();
    
    if (isLoading) return;
    
    const formData = {
        email: document.getElementById('email').value,
        name: document.getElementById('name').value,
        amount: parseFloat(document.getElementById('amount').value),
        type: document.querySelector('input[name="type"]:checked').value,
        currency: 'brl',
        card_number: document.getElementById('card-number').value,
        exp_month: parseInt(document.getElementById('exp-month').value),
        exp_year: parseInt(document.getElementById('exp-year').value),
        cvc: document.getElementById('cvc').value
    };
    
    // Validação hacker-proof
    if (!formData.email || !formData.name || !formData.amount) {
        showError('Preencha todos os campos obrigatórios!');
        return;
    }
    
    if (formData.amount < 10 || formData.amount > 10000) {
        showError('Valor deve estar entre R$ 10,00 e R$ 10.000,00!');
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch('/api/create_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            document.getElementById('payment-form').reset();
            hideConversionPreview();
        } else {
            showError(data.error);
        }
        
    } catch (error) {
        showError('Erro ao processar pagamento: ' + error.message);
    } finally {
        setLoading(false);
    }
}

// Mostra erro
function showError(message) {
    const errorDiv = document.getElementById('errors');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Mostra sucesso
function showSuccess(message) {
    alert('✅ ' + message);
}

// Define estado de loading
function setLoading(loading) {
    isLoading = loading;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const spinner = document.getElementById('spinner');
    
    if (loading) {
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        spinner.style.display = 'inline-block';
    } else {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

// Atualiza preço do Bitcoin a cada 5 minutos
setInterval(loadBitcoinPrice, 300000);

// HACK: Funções de Dropship
function showDropshipProducts() {
    fetch('/api/dropship_products')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const container = document.getElementById('dropship-products');
                container.style.display = 'block';
                
                let html = '<h6>Produtos Dropship Disponíveis:</h6><div class="row">';
                data.products.forEach(product => {
                    html += `
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <h6>${product.name}</h6>
                                    <p class="text-muted">${product.category}</p>
                                    <p><strong>R$ ${product.price}</strong></p>
                                    <p><small>Lucro: ${(product.profit_margin * 100).toFixed(0)}%</small></p>
                                    <button onclick="buyDropshipProduct('${product.id}', '${product.name}', ${product.price})" 
                                            class="btn btn-sm btn-warning">
                                        Comprar e Converter BTC
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                });
                html += '</div>';
                container.innerHTML = html;
            }
        })
        .catch(error => {
            console.error('Erro ao carregar produtos:', error);
            document.getElementById('dropship-products').innerHTML = '<div class="alert alert-danger">Erro ao carregar produtos</div>';
        });
}

function buyDropshipProduct(productId, productName, price) {
    const email = document.getElementById('email').value || 'cliente@email.com';
    const name = document.getElementById('name').value || 'Cliente';
    
    fetch('/api/dropship_order', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            email: email,
            name: name,
            product_name: productName,
            amount: price
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`🛍️ Produto comprado! R$ ${price} convertido para ${data.btc_amount.toFixed(8)} BTC`);
        } else {
            alert('Erro: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao processar compra');
    });
}

function dropshipUpsell() {
    const email = document.getElementById('email').value || 'cliente@email.com';
    const name = document.getElementById('name').value || 'Cliente';
    const amount = document.getElementById('amount').value || 100;
    
    fetch('/api/upsell', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            email: email,
            name: name,
            amount: parseFloat(amount)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('marketing-results').innerHTML = 
                '<div class="alert alert-success">✅ Upsell enviado com sucesso!</div>';
        } else {
            document.getElementById('marketing-results').innerHTML = 
                '<div class="alert alert-danger">❌ Erro: ' + data.error + '</div>';
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('marketing-results').innerHTML = 
            '<div class="alert alert-danger">❌ Erro ao enviar upsell</div>';
    });
}

// HACK: Funções de Marketing
function testUpsell() {
    const email = document.getElementById('email').value || 'teste@email.com';
    const name = document.getElementById('name').value || 'Cliente Teste';
    const amount = document.getElementById('amount').value || 100;
    
    fetch('/api/upsell', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            email: email,
            name: name,
            amount: parseFloat(amount)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('marketing-results').innerHTML = 
                '<div class="alert alert-success">🔥 Email de upsell enviado! Marketing automático ativado!</div>';
        } else {
            document.getElementById('marketing-results').innerHTML = 
                '<div class="alert alert-danger">❌ Erro: ' + data.error + '</div>';
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('marketing-results').innerHTML = 
            '<div class="alert alert-danger">❌ Erro no marketing</div>';
    });
}

function showFeeOptimization() {
    const amount = document.getElementById('amount').value || 100;
    
    fetch(`/api/fee_optimization?amount=${amount}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const feeInfo = data.fee_info;
                const bypassStats = data.bypass_stats;
                
                document.getElementById('marketing-results').innerHTML = `
                    <div class="alert alert-info">
                        <h6>💰 Otimização de Taxas</h6>
                        <p><strong>Valor:</strong> R$ ${amount}</p>
                        <p><strong>Taxa Otimizada:</strong> ${feeInfo.fee_percent.toFixed(2)}% (R$ ${feeInfo.fee_amount.toFixed(2)})</p>
                        <p><strong>Economia:</strong> R$ ${feeInfo.savings.toFixed(2)}</p>
                        <p><strong>Chaves Usadas:</strong> ${bypassStats.keys_used}</p>
                        <p><strong>Total Economizado:</strong> R$ ${bypassStats.total_savings.toFixed(2)}</p>
                    </div>
                `;
            } else {
                document.getElementById('marketing-results').innerHTML = 
                    '<div class="alert alert-danger">❌ Erro: ' + data.error + '</div>';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            document.getElementById('marketing-results').innerHTML = 
                '<div class="alert alert-danger">❌ Erro na otimização</div>';
        });
}