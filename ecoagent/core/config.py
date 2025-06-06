"""
EcoAgent Framework - Configuration centralisée
Gestion des coûts, limites et paramètres globaux
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict, field
from .resource_manager import resource_manager

@dataclass
class CostLimits:
    """Limites de coût configurables"""
    daily_limit_euros: float = 5.0
    per_request_limit_euros: float = 0.50
    warning_threshold_euros: float = 3.0
    require_confirmation_above_euros: float = 1.0

@dataclass  
class EcoAgentConfig:
    """Configuration principale d'EcoAgent"""
    
    # Informations de base
    version: str = "1.0.0"
    language: str = "fr"  # fr ou en
    debug_mode: bool = False
    
    # Gestion des coûts - utilisation de field() pour les objets mutables
    cost_limits: CostLimits = field(default_factory=CostLimits)
    
    # Configuration des modèles (auto-détectée)
    model_config: Optional[Dict[str, Any]] = None
    
    # Chemins
    workspace_dir: str = "./workspace"
    logs_dir: str = "./logs"
    cache_dir: str = "./cache"
    
    # API Keys (optionnelles)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Fonctionnalités
    auto_git_commit: bool = True
    generate_documentation: bool = True
    run_tests_automatically: bool = True
    
    def __post_init__(self):
        """Initialisation après création"""
        if self.model_config is None:
            self.model_config = resource_manager.get_optimal_model_config()
            
        # Charger les clés API depuis l'environnement
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    
    @classmethod
    def from_file(cls, config_path: str) -> 'EcoAgentConfig':
        """Charge la configuration depuis un fichier JSON"""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        except FileNotFoundError:
            return cls()  # Configuration par défaut
    
    def save_to_file(self, config_path: str) -> None:
        """Sauvegarde la configuration dans un fichier JSON"""
        import json
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Conversion en dictionnaire avec gestion des objets complexes
        config_dict = {}
        for key, value in asdict(self).items():
            if key == 'cost_limits':
                config_dict[key] = asdict(value) if hasattr(value, '__dict__') else value
            else:
                config_dict[key] = value
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    def get_display_summary(self) -> str:
        """Résumé lisible de la configuration"""
        return f"""
🔧 EcoAgent Framework v{self.version}
🌍 Langue: {self.language.upper()}
💰 Limite quotidienne: {self.cost_limits.daily_limit_euros}€
⚡ Modèle principal: {self.model_config.get('primary_model', 'N/A') if self.model_config else 'N/A'}
📁 Espace de travail: {self.workspace_dir}
🔑 OpenAI API: {'✅' if self.openai_api_key else '❌'}
🔑 Anthropic API: {'✅' if self.anthropic_api_key else '❌'}
        """.strip()

# Configuration globale par défaut
config = EcoAgentConfig()
