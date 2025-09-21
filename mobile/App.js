/**
 * App Mobile React Native - Sistema de Pagamentos Bitcoin
 * Interface mobile para pagamentos com conversão automática
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  ActivityIndicator,
  Switch,
  Picker
} from 'react-native';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Configure para sua URL

export default function App() {
  // Estados do formulário
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [amount, setAmount] = useState('');
  const [currency, setCurrency] = useState('BRL');
  const [paymentType, setPaymentType] = useState('unique');
  const [isLoading, setIsLoading] = useState(false);
  
  // Estados do sistema
  const [btcPrice, setBtcPrice] = useState(0);
  const [conversionPreview, setConversionPreview] = useState(null);
  const [language, setLanguage] = useState('pt');
  
  // Dados do cartão (em produção, use Stripe Elements)
  const [cardNumber, setCardNumber] = useState('4242424242424242');
  const [expMonth, setExpMonth] = useState('12');
  const [expYear, setExpYear] = useState('2025');
  const [cvc, setCvc] = useState('123');

  // Textos multi-idiomas
  const texts = {
    pt: {
      title: 'Pagamento Bitcoin',
      subtitle: 'Pague com cartão, receba em Bitcoin',
      email: 'Email',
      name: 'Nome',
      amount: 'Valor (R$)',
      currency: 'Moeda',
      paymentType: 'Tipo de Pagamento',
      unique: 'Pagamento Único',
      subscription: 'Assinatura Mensal',
      pay: 'Pagar e Converter',
      loading: 'Processando...',
      success: 'Pagamento realizado com sucesso!',
      error: 'Erro no pagamento',
      btcPrice: 'Preço Bitcoin',
      conversion: 'Conversão',
      dropship: 'Dropship',
      marketing: 'Marketing'
    },
    en: {
      title: 'Bitcoin Payment',
      subtitle: 'Pay with card, receive in Bitcoin',
      email: 'Email',
      name: 'Name',
      amount: 'Amount ($)',
      currency: 'Currency',
      paymentType: 'Payment Type',
      unique: 'One-time Payment',
      subscription: 'Monthly Subscription',
      pay: 'Pay and Convert',
      loading: 'Processing...',
      success: 'Payment successful!',
      error: 'Payment error',
      btcPrice: 'Bitcoin Price',
      conversion: 'Conversion',
      dropship: 'Dropship',
      marketing: 'Marketing'
    },
    es: {
      title: 'Pago Bitcoin',
      subtitle: 'Paga con tarjeta, recibe en Bitcoin',
      email: 'Email',
      name: 'Nombre',
      amount: 'Cantidad ($)',
      currency: 'Moneda',
      paymentType: 'Tipo de Pago',
      unique: 'Pago Único',
      subscription: 'Suscripción Mensual',
      pay: 'Pagar y Convertir',
      loading: 'Procesando...',
      success: '¡Pago exitoso!',
      error: 'Error en el pago',
      btcPrice: 'Precio Bitcoin',
      conversion: 'Conversión',
      dropship: 'Dropship',
      marketing: 'Marketing'
    }
  };

  const t = texts[language];

  useEffect(() => {
    loadBitcoinPrice();
  }, []);

  useEffect(() => {
    if (amount && parseFloat(amount) >= 10) {
      loadConversionPreview();
    }
  }, [amount, currency]);

  const loadBitcoinPrice = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/bitcoin_price?currency=${currency.toLowerCase()}`);
      if (response.data.success) {
        setBtcPrice(response.data.price);
      }
    } catch (error) {
      console.error('Erro ao carregar preço:', error);
    }
  };

  const loadConversionPreview = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/preview_conversion`, {
        amount: parseFloat(amount),
        currency: currency.toLowerCase()
      });
      
      if (response.data.success) {
        setConversionPreview(response.data);
      }
    } catch (error) {
      console.error('Erro ao carregar preview:', error);
    }
  };

  const handlePayment = async () => {
    if (!email || !name || !amount) {
      Alert.alert(t.error, 'Preencha todos os campos');
      return;
    }

    if (parseFloat(amount) < 10 || parseFloat(amount) > 10000) {
      Alert.alert(t.error, 'Valor deve estar entre R$ 10 e R$ 10.000');
      return;
    }

    setIsLoading(true);

    try {
      const paymentData = {
        email,
        name,
        amount: parseFloat(amount),
        currency: currency.toLowerCase(),
        type: paymentType,
        card_number: cardNumber,
        exp_month: parseInt(expMonth),
        exp_year: parseInt(expYear),
        cvc,
        language
      };

      const response = await axios.post(`${API_BASE_URL}/api/create_payment`, paymentData);
      
      if (response.data.success) {
        Alert.alert(t.success, response.data.message);
        // Limpa formulário
        setEmail('');
        setName('');
        setAmount('');
      } else {
        Alert.alert(t.error, response.data.error);
      }
    } catch (error) {
      console.error('Erro no pagamento:', error);
      Alert.alert(t.error, 'Erro ao processar pagamento');
    } finally {
      setIsLoading(false);
    }
  };

  const testDropship = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/dropship_order`, {
        email: email || 'teste@email.com',
        name: name || 'Cliente Teste',
        product_name: 'Produto Teste',
        amount: 100
      });
      
      if (response.data.success) {
        Alert.alert('Dropship', 'Produto comprado e convertido para Bitcoin!');
      }
    } catch (error) {
      console.error('Erro dropship:', error);
    }
  };

  const testMarketing = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/upsell`, {
        email: email || 'teste@email.com',
        name: name || 'Cliente Teste',
        amount: parseFloat(amount) || 100
      });
      
      if (response.data.success) {
        Alert.alert('Marketing', 'Upsell enviado com sucesso!');
      }
    } catch (error) {
      console.error('Erro marketing:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{t.title}</Text>
        <Text style={styles.subtitle}>{t.subtitle}</Text>
        
        {/* Seletor de idioma */}
        <View style={styles.languageSelector}>
          <Text>Idioma: </Text>
          <Picker
            selectedValue={language}
            style={styles.picker}
            onValueChange={setLanguage}
          >
            <Picker.Item label="Português" value="pt" />
            <Picker.Item label="English" value="en" />
            <Picker.Item label="Español" value="es" />
          </Picker>
        </View>
      </View>

      {/* Preço Bitcoin */}
      <View style={styles.priceCard}>
        <Text style={styles.priceLabel}>{t.btcPrice}</Text>
        <Text style={styles.priceValue}>
          {currency} {btcPrice.toLocaleString()}
        </Text>
      </View>

      {/* Formulário */}
      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder={t.email}
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        
        <TextInput
          style={styles.input}
          placeholder={t.name}
          value={name}
          onChangeText={setName}
        />
        
        <TextInput
          style={styles.input}
          placeholder={t.amount}
          value={amount}
          onChangeText={setAmount}
          keyboardType="numeric"
        />
        
        <View style={styles.row}>
          <View style={styles.halfWidth}>
            <Text style={styles.label}>{t.currency}</Text>
            <Picker
              selectedValue={currency}
              style={styles.picker}
              onValueChange={setCurrency}
            >
              <Picker.Item label="BRL" value="BRL" />
              <Picker.Item label="USD" value="USD" />
            </Picker>
          </View>
          
          <View style={styles.halfWidth}>
            <Text style={styles.label}>{t.paymentType}</Text>
            <Picker
              selectedValue={paymentType}
              style={styles.picker}
              onValueChange={setPaymentType}
            >
              <Picker.Item label={t.unique} value="unique" />
              <Picker.Item label={t.subscription} value="subscription" />
            </Picker>
          </View>
        </View>
      </View>

      {/* Preview da conversão */}
      {conversionPreview && (
        <View style={styles.previewCard}>
          <Text style={styles.previewTitle}>{t.conversion}</Text>
          <Text>Valor: {currency} {conversionPreview.original_amount.toLocaleString()}</Text>
          <Text>Taxa: {currency} {conversionPreview.fee_amount.toLocaleString()}</Text>
          <Text>Bitcoin: {conversionPreview.btc_amount.toFixed(8)} BTC</Text>
        </View>
      )}

      {/* Botão de pagamento */}
      <TouchableOpacity
        style={[styles.payButton, isLoading && styles.payButtonDisabled]}
        onPress={handlePayment}
        disabled={isLoading}
      >
        {isLoading ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text style={styles.payButtonText}>{t.pay}</Text>
        )}
      </TouchableOpacity>

      {/* Botões de teste */}
      <View style={styles.testButtons}>
        <TouchableOpacity style={styles.testButton} onPress={testDropship}>
          <Text style={styles.testButtonText}>{t.dropship}</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.testButton} onPress={testMarketing}>
          <Text style={styles.testButtonText}>{t.marketing}</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#2c3e50',
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#ecf0f1',
    marginBottom: 15,
  },
  languageSelector: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  picker: {
    height: 50,
    width: 120,
    backgroundColor: 'white',
  },
  priceCard: {
    backgroundColor: '#27ae60',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  priceLabel: {
    color: 'white',
    fontSize: 16,
    marginBottom: 5,
  },
  priceValue: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
  },
  form: {
    backgroundColor: 'white',
    margin: 15,
    padding: 20,
    borderRadius: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    padding: 15,
    marginBottom: 15,
    fontSize: 16,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  halfWidth: {
    width: '48%',
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
    fontWeight: '500',
  },
  previewCard: {
    backgroundColor: '#3498db',
    margin: 15,
    padding: 20,
    borderRadius: 10,
  },
  previewTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  payButton: {
    backgroundColor: '#e74c3c',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  payButtonDisabled: {
    backgroundColor: '#bdc3c7',
  },
  payButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  testButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    margin: 15,
  },
  testButton: {
    backgroundColor: '#f39c12',
    padding: 15,
    borderRadius: 10,
    flex: 0.45,
    alignItems: 'center',
  },
  testButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
});
