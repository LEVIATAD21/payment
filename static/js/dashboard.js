// Dashboard JavaScript - Sistema Bitcoin Hacker-Style
let conversionChart = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadDashboardData();
    setupEventListeners();
});

// Inicializa dashboard
function initializeDashboard() {
    // Inicializa gráfico de conversões
    const ctx = document.getElementById('conversionChart');
    if (ctx) {
        conversionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Valor Convertido (R$)',
                    data: [1000, 1500, 2000, 1800, 2500, 3000],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toLocaleString('pt-BR');
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Conversões Bitcoin - Últimos 6 Meses'
                    }
                }
            }
        });
    }
}

// Event listeners
function setupEventListeners() {
    // Atualiza dados a cada 30 segundos
    setInterval(loadDashboardData, 30000);
    
    // Event listeners para tabs
    const tabs = document.querySelectorAll('#dashboardTabs button[data-bs-toggle="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const target = event.target.getAttribute('data-bs-target');
            if (target === '#payments') {
                loadPayments();
            } else if (target === '#subscriptions') {
                loadSubscriptions();
            } else if (target === '#conversions') {
                loadConversions();
            }
        });
    });
}

// Carrega dados do dashboard
async function loadDashboardData() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            updateStats(data);
        }
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

// Atualiza estatísticas
function updateStats(data) {
    document.getElementById('total-converted').textContent = 
        'R$ ' + data.total_converted.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    
    document.getElementById('btc-received').textContent = 
        data.btc_received.toFixed(8) + ' BTC';
    
    document.getElementById('active-subscriptions').textContent = data.active_subs;
}

// Carrega pagamentos
async function loadPayments() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            // Atualiza tabela de pagamentos
            const tableBody = document.getElementById('payments-table');
            if (data.total_payments === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center text-muted">
                            Nenhum pagamento encontrado
                        </td>
                    </tr>
                `;
            }
        }
    } catch (error) {
        console.error('Erro ao carregar pagamentos:', error);
    }
}

// Carrega assinaturas
async function loadSubscriptions() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            // Atualiza tabela de assinaturas
            const tableBody = document.getElementById('subscriptions-table');
            if (data.active_subs === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            Nenhuma assinatura encontrada
                        </td>
                    </tr>
                `;
            }
        }
    } catch (error) {
        console.error('Erro ao carregar assinaturas:', error);
    }
}

// Carrega conversões
async function loadConversions() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            // Atualiza gráfico
            updateConversionChart(data);
        }
    } catch (error) {
        console.error('Erro ao carregar conversões:', error);
    }
}

// Atualiza gráfico de conversões
function updateConversionChart(data) {
    if (conversionChart) {
        // Dados simulados baseados nas estatísticas
        const labels = [];
        const values = [];
        
        for (let i = 5; i >= 0; i--) {
            const date = new Date();
            date.setMonth(date.getMonth() - i);
            labels.push(date.toLocaleDateString('pt-BR', {month: 'short'}));
            values.push(Math.random() * 1000 + 500); // Valores simulados
        }
        
        conversionChart.data.labels = labels;
        conversionChart.data.datasets[0].data = values;
        conversionChart.update();
    }
}

// Atualiza wallet
async function updateWallet() {
    const walletAddress = document.getElementById('wallet-address').value;
    
    if (!walletAddress) {
        alert('Por favor, insira um endereço de wallet válido.');
        return;
    }
    
    try {
        // Simula atualização da wallet
        alert('✅ Wallet atualizada com sucesso!');
        console.log('Nova wallet:', walletAddress);
    } catch (error) {
        alert('❌ Erro ao atualizar wallet: ' + error.message);
    }
}

// Cria nova assinatura
function createSubscription() {
    const email = prompt('Email do cliente:');
    const name = prompt('Nome do cliente:');
    const amount = prompt('Valor mensal (R$):');
    
    if (!email || !name || !amount) {
        alert('Todos os campos são obrigatórios!');
        return;
    }
    
    const amountNum = parseFloat(amount);
    if (isNaN(amountNum) || amountNum < 10 || amountNum > 10000) {
        alert('Valor inválido! Deve ser entre R$ 10,00 e R$ 10.000,00');
        return;
    }
    
    // Simula criação de assinatura
    alert(`✅ Assinatura criada!\nCliente: ${name}\nEmail: ${email}\nValor: R$ ${amountNum.toFixed(2)}`);
}

// Cancela assinatura
function cancelSubscription(subscriptionId) {
    if (!confirm('Tem certeza que deseja cancelar esta assinatura?')) {
        return;
    }
    
    // Simula cancelamento
    alert(`✅ Assinatura ${subscriptionId} cancelada com sucesso!`);
}

// Atualiza pagamentos
function refreshPayments() {
    loadPayments();
    alert('🔄 Pagamentos atualizados!');
}

// Atualiza assinaturas
function refreshSubscriptions() {
    loadSubscriptions();
    alert('🔄 Assinaturas atualizadas!');
}

// Atualiza conversões
function refreshConversions() {
    loadConversions();
    alert('🔄 Conversões atualizadas!');
}