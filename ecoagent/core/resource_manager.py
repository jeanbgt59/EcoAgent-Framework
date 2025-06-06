"""
EcoAgent Framework - Resource Manager
Détecte automatiquement les ressources système et optimise la configuration
"""

import psutil
import platform
import subprocess
from typing import Dict, Tuple, Optional
from enum import Enum
import logging

class ResourceTier(Enum):
    """Niveaux de ressources détectés"""
    MINIMAL = "minimal"      # < 8GB RAM
    STANDARD = "standard"    # 8-16GB RAM
    ENHANCED = "enhanced"    # 16-32GB RAM  
    PREMIUM = "premium"      # > 32GB RAM

class ResourceManager:
    """Gestionnaire intelligent des ressources système"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._system_info = self._detect_system()
        self._resource_tier = self._determine_tier()
        
    def _detect_system(self) -> Dict:
        """Détecte les spécifications du système"""
        try:
            return {
                'platform': platform.system(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'ram_gb': round(psutil.virtual_memory().total / (1024**3), 1),
                'cpu_cores': psutil.cpu_count(logical=True),
                'cpu_cores_physical': psutil.cpu_count(logical=False),
                'ollama_available': self._check_ollama_availability()
            }
        except Exception as e:
            self.logger.error(f"Erreur détection système: {e}")
            return self._get_fallback_config()
    
    def _check_ollama_availability(self) -> bool:
        """Vérifie si Ollama est installé et accessible"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _determine_tier(self) -> ResourceTier:
        """Détermine le niveau de ressources disponibles"""
        ram = self._system_info['ram_gb']
        
        if ram >= 32:
            return ResourceTier.PREMIUM
        elif ram >= 16:
            return ResourceTier.ENHANCED  # Votre MacBook Pro !
        elif ram >= 8:
            return ResourceTier.STANDARD
        else:
            return ResourceTier.MINIMAL
    
    def get_optimal_model_config(self) -> Dict:
        """Retourne la configuration optimale des modèles selon les ressources"""
        configs = {
            ResourceTier.MINIMAL: {
                'primary_model': 'tinyllama',
                'fallback_model': None,
                'max_concurrent_agents': 2,
                'use_api_threshold': 0.8,  # Utilise API si charge > 80%
                'context_window': 2048
            },
            ResourceTier.STANDARD: {
                'primary_model': 'gemma:2b',
                'fallback_model': 'tinyllama',
                'max_concurrent_agents': 4,
                'use_api_threshold': 0.85,
                'context_window': 4096
            },
            ResourceTier.ENHANCED: {  # Votre configuration optimale
                'primary_model': 'mistral:7b',
                'fallback_model': 'gemma:2b',
                'coding_model': 'codellama:7b',
                'max_concurrent_agents': 6,
                'use_api_threshold': 0.9,
                'context_window': 8192
            },
            ResourceTier.PREMIUM: {
                'primary_model': 'codellama:13b',
                'fallback_model': 'mistral:7b',
                'coding_model': 'codellama:13b',
                'max_concurrent_agents': 8,
                'use_api_threshold': 0.95,
                'context_window': 16384
            }
        }
        
        return configs[self._resource_tier]
    
    def can_run_concurrent_agents(self, requested_agents: int) -> bool:
        """Vérifie si le système peut gérer N agents simultanément"""
        max_agents = self.get_optimal_model_config()['max_concurrent_agents']
        current_load = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        
        # Logique de décision intelligente
        if current_load > 80 or memory_usage > 85:
            return requested_agents <= max(1, max_agents // 2)
        
        return requested_agents <= max_agents
    
    def get_system_summary(self) -> str:
        """Retourne un résumé lisible de la configuration"""
        info = self._system_info
        config = self.get_optimal_model_config()
        
        return f"""
🖥️  Système détecté: {info['platform']} ({info['machine']})
💾 RAM: {info['ram_gb']} GB
🔧 CPU: {info['cpu_cores']} cœurs ({info['cpu_cores_physical']} physiques)
🤖 Ollama: {'✅ Disponible' if info['ollama_available'] else '❌ Non détecté'}
⚡ Niveau: {self._resource_tier.value.upper()}
🎯 Modèle principal: {config['primary_model']}
👥 Agents simultanés max: {config['max_concurrent_agents']}
        """.strip()

    def _get_fallback_config(self) -> Dict:
        """Configuration de sécurité si la détection échoue"""
        return {
            'platform': 'Unknown',
            'machine': 'Unknown', 
            'processor': 'Unknown',
            'ram_gb': 8.0,  # Estimation conservatrice
            'cpu_cores': 4,
            'cpu_cores_physical': 2,
            'ollama_available': False
        }

# Instance globale pour usage dans le framework
resource_manager = ResourceManager()
