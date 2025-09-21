"""
Proxy Rotator - Anti-Detecção Suprema
Sistema de rotação de proxies para anonimato total
"""

import requests
import random
import time
from src.config.settings import DEBUG

class ProxyRotator:
    """Sistema de rotação de proxies para anonimato"""
    
    def __init__(self):
        # Lista de proxies (configure seus proxies reais)
        self.proxies_list = [
            # Exemplos - substitua por proxies reais
            {'http': 'http://proxy1.example.com:8080', 'https': 'https://proxy1.example.com:8080'},
            {'http': 'http://proxy2.example.com:8080', 'https': 'https://proxy2.example.com:8080'},
            {'http': 'http://proxy3.example.com:8080', 'https': 'https://proxy3.example.com:8080'},
            # Adicione mais proxies conforme necessário
        ]
        
        # Proxies gratuitos (menos confiáveis, mas funcionais)
        self.free_proxies = [
            {'http': 'http://8.8.8.8:8080', 'https': 'https://8.8.8.8:8080'},
            {'http': 'http://1.1.1.1:8080', 'https': 'https://1.1.1.1:8080'},
        ]
        
        # Headers para anonimato
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        
        # Estatísticas de uso
        self.proxy_stats = {}
        self.failed_proxies = set()
        
    def get_random_proxy(self, use_free=False):
        """Retorna proxy aleatório"""
        try:
            if use_free:
                proxy_list = self.free_proxies
            else:
                proxy_list = self.proxies_list
            
            # Filtra proxies que falharam recentemente
            available_proxies = [p for p in proxy_list if str(p) not in self.failed_proxies]
            
            if not available_proxies:
                if DEBUG:
                    print("⚠️ Todos os proxies falharam, usando proxy padrão")
                return None
            
            proxy = random.choice(available_proxies)
            
            # Registra uso
            proxy_key = str(proxy)
            self.proxy_stats[proxy_key] = self.proxy_stats.get(proxy_key, 0) + 1
            
            if DEBUG:
                print(f"🔄 Usando proxy: {proxy_key}")
            
            return proxy
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao selecionar proxy: {e}")
            return None
    
    def get_random_headers(self):
        """Retorna headers aleatórios para anonimato"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
    
    def test_proxy(self, proxy, timeout=10):
        """Testa se proxy está funcionando"""
        try:
            test_url = 'https://httpbin.org/ip'
            response = requests.get(
                test_url,
                proxies=proxy,
                headers=self.get_random_headers(),
                timeout=timeout
            )
            
            if response.status_code == 200:
                if DEBUG:
                    print(f"✅ Proxy funcionando: {proxy}")
                return True
            else:
                if DEBUG:
                    print(f"❌ Proxy falhou: {proxy} - Status: {response.status_code}")
                return False
                
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro ao testar proxy {proxy}: {e}")
            return False
    
    def get_working_proxy(self, max_attempts=3):
        """Retorna um proxy que está funcionando"""
        for attempt in range(max_attempts):
            proxy = self.get_random_proxy()
            if proxy and self.test_proxy(proxy):
                return proxy
            else:
                if proxy:
                    self.failed_proxies.add(str(proxy))
                time.sleep(1)  # Delay entre tentativas
        
        # Se todos falharam, tenta proxies gratuitos
        if DEBUG:
            print("⚠️ Tentando proxies gratuitos...")
        
        for attempt in range(max_attempts):
            proxy = self.get_random_proxy(use_free=True)
            if proxy and self.test_proxy(proxy):
                return proxy
            time.sleep(1)
        
        if DEBUG:
            print("❌ Nenhum proxy funcionando")
        return None
    
    def make_request(self, method, url, **kwargs):
        """Faz requisição com proxy rotativo"""
        try:
            proxy = self.get_working_proxy()
            headers = self.get_random_headers()
            
            # Adiciona proxy e headers se disponíveis
            if proxy:
                kwargs['proxies'] = proxy
            
            kwargs['headers'] = {**headers, **kwargs.get('headers', {})}
            kwargs['timeout'] = kwargs.get('timeout', 30)
            
            response = requests.request(method, url, **kwargs)
            
            if DEBUG:
                print(f"🌐 Requisição via proxy: {method} {url} - Status: {response.status_code}")
            
            return response
            
        except Exception as e:
            if DEBUG:
                print(f"❌ Erro na requisição com proxy: {e}")
            
            # Fallback: requisição sem proxy
            try:
                kwargs.pop('proxies', None)
                kwargs['headers'] = self.get_random_headers()
                return requests.request(method, url, **kwargs)
            except Exception as fallback_error:
                if DEBUG:
                    print(f"❌ Erro no fallback: {fallback_error}")
                raise fallback_error
    
    def get_proxy_stats(self):
        """Retorna estatísticas de uso dos proxies"""
        return {
            'total_proxies': len(self.proxies_list),
            'failed_proxies': len(self.failed_proxies),
            'working_proxies': len(self.proxies_list) - len(self.failed_proxies),
            'usage_stats': self.proxy_stats
        }
    
    def reset_failed_proxies(self):
        """Reseta lista de proxies que falharam"""
        self.failed_proxies.clear()
        if DEBUG:
            print("🔄 Lista de proxies falhados resetada")

# Instância global
proxy_rotator = ProxyRotator()

# Funções de conveniência
def get_rotated_proxy():
    """Retorna proxy rotativo"""
    return proxy_rotator.get_working_proxy()

def make_proxy_request(method, url, **kwargs):
    """Faz requisição com proxy"""
    return proxy_rotator.make_request(method, url, **kwargs)

def get_proxy_stats():
    """Estatísticas de proxies"""
    return proxy_rotator.get_proxy_stats()

def reset_proxy_failures():
    """Reseta falhas de proxy"""
    proxy_rotator.reset_failed_proxies()
