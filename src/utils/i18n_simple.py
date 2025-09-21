"""
Sistema de Internacionalização Simples - Multi-Idiomas
Suporte para PT, EN, ES para escalar globalmente
"""

from flask import request, session

def init_babel(app):
    """Inicializa o sistema de internacionalização (versão simples)"""
    # Configuração de idiomas suportados
    app.config['LANGUAGES'] = {
        'pt': 'Português',
        'en': 'English', 
        'es': 'Español'
    }
    
    # Idioma padrão
    app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'America/Sao_Paulo'
    
    return None

def set_language(language):
    """Define idioma na sessão"""
    if language in ['pt', 'en', 'es']:
        session['language'] = language
        return True
    return False

def get_available_languages():
    """Retorna idiomas disponíveis"""
    return {
        'pt': 'Português',
        'en': 'English',
        'es': 'Español'
    }

def get_language_name(code):
    """Retorna nome do idioma pelo código"""
    languages = get_available_languages()
    return languages.get(code, 'Português')

# Funções de conveniência para tradução
def t(text, **kwargs):
    """Função de conveniência para tradução (versão simples)"""
    return text

def format_currency(amount, currency='BRL', locale=None):
    """Formata moeda baseado no idioma"""
    if locale == 'en':
        if currency == 'BRL':
            return f"R$ {amount:,.2f}"
        elif currency == 'USD':
            return f"${amount:,.2f}"
    elif locale == 'es':
        if currency == 'BRL':
            return f"R$ {amount:,.2f}"
        elif currency == 'USD':
            return f"${amount:,.2f}"
    else:  # pt (padrão)
        if currency == 'BRL':
            return f"R$ {amount:,.2f}"
        elif currency == 'USD':
            return f"US$ {amount:,.2f}"
    
    return f"{amount:,.2f} {currency}"

def get_currency_symbol(currency, locale=None):
    """Retorna símbolo da moeda baseado no idioma"""
    if locale == 'en':
        return {'BRL': 'R$', 'USD': '$'}.get(currency, currency)
    elif locale == 'es':
        return {'BRL': 'R$', 'USD': '$'}.get(currency, currency)
    else:  # pt
        return {'BRL': 'R$', 'USD': 'US$'}.get(currency, currency)

def get_date_format(locale=None):
    """Retorna formato de data baseado no idioma"""
    if locale == 'en':
        return '%m/%d/%Y'
    elif locale == 'es':
        return '%d/%m/%Y'
    else:  # pt
        return '%d/%m/%Y'

def get_time_format(locale=None):
    """Retorna formato de hora baseado no idioma"""
    if locale == 'en':
        return '%I:%M %p'
    elif locale == 'es':
        return '%H:%M'
    else:  # pt
        return '%H:%M'
