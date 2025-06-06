"""
EcoAgent Framework - Estimateur de coûts
Votre différenciateur clé : transparence totale des coûts
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

class ModelProvider(Enum):
    """Fournisseurs de modèles supportés"""
    OLLAMA = "ollama"
    OPENAI = "openai" 
    ANTHROPIC = "anthropic"

@dataclass
class CostEstimate:
    """Estimation détaillée des coûts"""
    provider: ModelProvider
    model_name: str
    estimated_tokens: int
    cost_euros: float
    confidence_level: float  # 0.0 à 1.0
    reasoning: str

class CostEstimator:
    """Estimateur intelligent des coûts d'utilisation"""
    
    # Tarifs à jour (janvier 2025)
    PRICING = {
        ModelProvider.OPENAI: {
            'gpt-4o': {'input': 0.0000025, 'output': 0.00001},     # €/token
            'gpt-4o-mini': {'input': 0.00000015, 'output': 0.0000006},
            'gpt-3.5-turbo': {'input': 0.0000005, 'output': 0.0000015}
        },
        ModelProvider.ANTHROPIC: {
            'claude-3-5-sonnet': {'input': 0.000003, 'output': 0.000015},
            'claude-3-haiku': {'input': 0.00000025, 'output': 0.00000125}
        },
        ModelProvider.OLLAMA: {
            # Ollama = 0€ mais coût en électricité/temps
            'default': {'input': 0.0, 'output': 0.0}
        }
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.usage_history: List[Dict] = []
        
    def estimate_task_cost(self, 
                          task_description: str,
                          expected_agents: int = 3,
                          complexity: str = "medium") -> List[CostEstimate]:
        """Estime le coût d'une tâche complète"""
        
        # Estimation des tokens basée sur la complexité
        token_estimates = {
            "simple": {"input": 500, "output": 1000},    # Correction simple
            "medium": {"input": 1500, "output": 3000},   # Développement moyen
            "complex": {"input": 5000, "output": 8000}   # Projet complet
        }
        
        base_tokens = token_estimates.get(complexity, token_estimates["medium"])
        total_tokens = {
            "input": base_tokens["input"] * expected_agents,
            "output": base_tokens["output"] * expected_agents
        }
        
        estimates = []
        
        # Option 1: Ollama (gratuit)
        estimates.append(CostEstimate(
            provider=ModelProvider.OLLAMA,
            model_name="mistral:7b + codellama:7b",
            estimated_tokens=total_tokens["input"] + total_tokens["output"],
            cost_euros=0.0,
            confidence_level=0.95,
            reasoning="Modèles locaux - Aucun coût API mais utilise ressources système"
        ))
        
        # Option 2: OpenAI (si nécessaire)
        if self._should_suggest_api_option(complexity):
            gpt_cost = self._calculate_cost(
                ModelProvider.OPENAI, 
                'gpt-4o-mini',
                total_tokens["input"],
                total_tokens["output"]
            )
            
            estimates.append(CostEstimate(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4o-mini",
                estimated_tokens=total_tokens["input"] + total_tokens["output"],
                cost_euros=gpt_cost,
                confidence_level=0.85,
                reasoning=f"Recommandé si Ollama insuffisant pour '{complexity}'"
            ))
        
        return estimates
    
    def _calculate_cost(self, 
                       provider: ModelProvider,
                       model: str, 
                       input_tokens: int,
                       output_tokens: int) -> float:
        """Calcule le coût exact pour un modèle"""
        
        pricing = self.PRICING.get(provider, {}).get(model)
        if not pricing:
            return 0.0
            
        cost = (input_tokens * pricing['input']) + (output_tokens * pricing['output'])
        return round(cost, 4)
    
    def _should_suggest_api_option(self, complexity: str) -> bool:
        """Détermine s'il faut suggérer une option API payante"""
        # Plus la tâche est complexe, plus on suggère l'API
        return complexity in ["complex", "enterprise"]
    
    def get_cost_breakdown_display(self, estimates: List[CostEstimate]) -> str:
        """Affichage lisible des estimations de coût"""
        
        display = "\n💰 **ESTIMATION DES COÛTS** 💰\n"
        display += "=" * 40 + "\n"
        
        for i, estimate in enumerate(estimates, 1):
            confidence_bar = "🟢" * int(estimate.confidence_level * 5)
            confidence_bar += "⚪" * (5 - int(estimate.confidence_level * 5))
            
            display += f"\n**Option {i}: {estimate.provider.value.upper()}**\n"
            display += f"📱 Modèle: {estimate.model_name}\n"
            display += f"💵 Coût estimé: {estimate.cost_euros:.4f}€\n"
            display += f"🎯 Confiance: {confidence_bar} ({estimate.confidence_level:.0%})\n"
            display += f"💭 Justification: {estimate.reasoning}\n"
            display += "-" * 30 + "\n"
        
        # Recommandation
        recommended = min(estimates, key=lambda x: x.cost_euros)
        display += f"\n🏆 **RECOMMANDATION**: {recommended.provider.value.upper()}\n"
        display += f"Coût total estimé: **{recommended.cost_euros:.4f}€**\n"
        
        return display
    
    def confirm_cost_with_user(self, estimates: List[CostEstimate]) -> Tuple[bool, Optional[CostEstimate]]:
        """Interface de confirmation utilisateur (sera intégrée au CLI)"""
        print(self.get_cost_breakdown_display(estimates))
        
        # Pour l'instant, retourne automatiquement l'option la moins chère
        recommended = min(estimates, key=lambda x: x.cost_euros)
        
        # TODO: Implémenter vraie interface utilisateur
        return True, recommended
    
    def track_actual_usage(self, 
                          provider: ModelProvider,
                          model: str,
                          input_tokens: int,
                          output_tokens: int,
                          actual_cost: float = 0.0):
        """Enregistre l'utilisation réelle pour affiner les estimations"""
        
        usage_record = {
            'timestamp': time.time(),
            'provider': provider.value,
            'model': model,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'actual_cost': actual_cost
        }
        
        self.usage_history.append(usage_record)
        
        # Limite l'historique à 1000 entrées
        if len(self.usage_history) > 1000:
            self.usage_history = self.usage_history[-1000:]
    
    def get_daily_usage_summary(self) -> Dict:
        """Résumé de l'utilisation quotidienne"""
        today_start = time.time() - (24 * 3600)  # 24 heures
        
        today_usage = [
            record for record in self.usage_history 
            if record['timestamp'] >= today_start
        ]
        
        total_cost = sum(record['actual_cost'] for record in today_usage)
        total_requests = len(today_usage)
        
        return {
            'total_cost_euros': round(total_cost, 4),
            'total_requests': total_requests,
            'average_cost_per_request': round(total_cost / max(1, total_requests), 4),
            'ollama_requests': len([r for r in today_usage if r['provider'] == 'ollama']),
            'api_requests': len([r for r in today_usage if r['provider'] != 'ollama'])
        }

# Instance globale
cost_estimator = CostEstimator()
