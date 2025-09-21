"""
Bot de IA para Geração de Leads - Scrap Automático
Sistema hacker para prospecção de clientes
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse
from src.config.settings import DEBUG
from src.models.database import MarketingCampaign, db

class LeadScraper:
    """Bot hacker para extração de leads"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Lista de proxies para anonimato (configure seus proxies)
        self.proxies = [
            # {'http': 'http://proxy1:port', 'https': 'https://proxy1:port'},
            # {'http': 'http://proxy2:port', 'https': 'https://proxy2:port'},
        ]
        
        # Sites para scrap (exemplos)
        self.target_sites = [
            'https://example-forum.com',
            'https://business-directory.com',
            'https://social-network.com',
        ]
        
        # Padrões de email
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Palavras-chave para identificar leads qualificados
        self.qualifying_keywords = [
            'bitcoin', 'crypto', 'investimento', 'trading', 'finanças',
            'empreendedor', 'negócio', 'startup', 'vendas', 'marketing',
            'e-commerce', 'dropshipping', 'afiliado', 'renda passiva'
        ]
    
    def get_random_proxy(self):
        """Retorna proxy aleatório para anonimato"""
        if self.proxies:
            return random.choice(self.proxies)
        return None
    
    def scrape_emails_from_url(self, url, max_emails=10):
        """Extrai emails de uma URL específica"""
        try:
            proxy = self.get_random_proxy()
            response = requests.get(url, headers=self.headers, proxies=proxy, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            emails = []
            
            # Busca emails em links mailto
            mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
            for link in mailto_links:
                email = link['href'].replace('mailto:', '').strip()
                if self.is_valid_email(email):
                    emails.append(email)
            
            # Busca emails no texto da página
            text_content = soup.get_text()
            found_emails = self.email_pattern.findall(text_content)
            for email in found_emails:
                if self.is_valid_email(email):
                    emails.append(email)
            
            # Remove duplicatas e limita quantidade
            unique_emails = list(set(emails))[:max_emails]
            
            if DEBUG:
                print(f"📧 Encontrados {len(unique_emails)} emails em {url}")
            
            return unique_emails
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao fazer scrap de {url}: {e}")
            return []
    
    def is_valid_email(self, email):
        """Valida se email é válido"""
        if not email or len(email) < 5:
            return False
        
        # Filtra emails genéricos
        generic_emails = [
            'noreply@', 'no-reply@', 'admin@', 'info@', 'contact@',
            'support@', 'help@', 'test@', 'example@', 'sample@'
        ]
        
        for generic in generic_emails:
            if generic in email.lower():
                return False
        
        return True
    
    def analyze_lead_quality(self, email, context=""):
        """Analisa qualidade do lead baseado no contexto"""
        score = 0
        
        # Verifica palavras-chave no contexto
        context_lower = context.lower()
        for keyword in self.qualifying_keywords:
            if keyword in context_lower:
                score += 1
        
        # Verifica domínio do email
        domain = email.split('@')[1].lower()
        business_domains = [
            'gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com',
            'empresa.com', 'business.com', 'startup.com'
        ]
        
        if domain in business_domains:
            score += 1
        
        return score
    
    def scrape_multiple_sites(self, max_emails_per_site=5):
        """Faz scrap de múltiplos sites"""
        all_emails = []
        
        for site in self.target_sites:
            try:
                emails = self.scrape_emails_from_url(site, max_emails_per_site)
                all_emails.extend(emails)
                
                # Delay entre requests para evitar bloqueio
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                if DEBUG:
                    print(f"❌ Erro no site {site}: {e}")
                continue
        
        return list(set(all_emails))  # Remove duplicatas
    
    def generate_lead_context(self, email, source_url=""):
        """Gera contexto para o lead"""
        return {
            'email': email,
            'source_url': source_url,
            'scraped_at': time.time(),
            'quality_score': self.analyze_lead_quality(email, source_url),
            'status': 'new'
        }
    
    def save_leads_to_database(self, leads):
        """Salva leads no banco de dados"""
        try:
            for lead in leads:
                # Cria campanha de marketing para o lead
                campaign = MarketingCampaign(
                    campaign_name=f"Lead Scrap - {lead['email']}",
                    campaign_type='upsell',
                    target_email=lead['email'],
                    target_name=lead['email'].split('@')[0],
                    amount=100.0,  # Valor padrão para upsell
                    status='pending'
                )
                
                db.session.add(campaign)
            
            db.session.commit()
            
            if DEBUG:
                print(f"💾 {len(leads)} leads salvos no banco de dados")
            
            return True
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao salvar leads: {e}")
            return False
    
    def run_lead_generation(self, max_total_emails=50):
        """Executa geração de leads completa"""
        try:
            if DEBUG:
                print("🤖 Iniciando geração de leads...")
            
            # Faz scrap de múltiplos sites
            emails = self.scrape_multiple_sites(max_emails_per_site=10)
            
            if not emails:
                if DEBUG:
                    print("❌ Nenhum email encontrado")
                return []
            
            # Gera contexto para cada lead
            leads = []
            for email in emails[:max_total_emails]:
                lead = self.generate_lead_context(email)
                leads.append(lead)
            
            # Salva no banco de dados
            self.save_leads_to_database(leads)
            
            if DEBUG:
                print(f"✅ Geração de leads concluída: {len(leads)} leads encontrados")
            
            return leads
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na geração de leads: {e}")
            return []
    
    def get_lead_statistics(self):
        """Retorna estatísticas de leads"""
        try:
            total_leads = MarketingCampaign.query.filter_by(campaign_type='upsell').count()
            new_leads = MarketingCampaign.query.filter_by(campaign_type='upsell', status='pending').count()
            converted_leads = MarketingCampaign.query.filter_by(campaign_type='upsell', status='converted').count()
            
            return {
                'total_leads': total_leads,
                'new_leads': new_leads,
                'converted_leads': converted_leads,
                'conversion_rate': (converted_leads / total_leads * 100) if total_leads > 0 else 0
            }
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao obter estatísticas: {e}")
            return {
                'total_leads': 0,
                'new_leads': 0,
                'converted_leads': 0,
                'conversion_rate': 0
            }

# Instância global do scraper
lead_scraper = LeadScraper()

# Funções de conveniência
def run_lead_generation(max_total_emails=50):
    """Executa geração de leads"""
    return lead_scraper.run_lead_generation(max_total_emails)

def get_lead_statistics():
    """Retorna estatísticas de leads"""
    return lead_scraper.get_lead_statistics()

def scrape_emails_from_url(url, max_emails=10):
    """Extrai emails de uma URL específica"""
    return lead_scraper.scrape_emails_from_url(url, max_emails)
