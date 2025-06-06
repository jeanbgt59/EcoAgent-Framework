#!/usr/bin/env python3
"""Test de la configuration initiale d'EcoAgent"""

from ecoagent.core.resource_manager import resource_manager
from ecoagent.core.config import config  
from ecoagent.core.cost_estimator import cost_estimator

def main():
    print("🚀 Test de configuration EcoAgent Framework")
    print("=" * 50)
    
    # Test du gestionnaire de ressources
    print(resource_manager.get_system_summary())
    print("\n" + "=" * 50)
    
    # Test de la configuration
    print(config.get_display_summary())
    print("\n" + "=" * 50)
    
    # Test de l'estimateur de coûts
    estimates = cost_estimator.estimate_task_cost(
        "Créer une application web simple avec FastAPI",
        expected_agents=3,
        complexity="medium"
    )
    
    print(cost_estimator.get_cost_breakdown_display(estimates))

if __name__ == "__main__":
    main()
