#!/usr/bin/env python3
"""
Test de l'agent architecte
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecoagent.agents.analysis_agent import analysis_agent
from ecoagent.agents.architect_agent import architect_agent

async def test_architect_with_analysis():
    print("🏗️  Test de l'Agent Architecte")
    print("=" * 50)
    
    # Étape 1: Analyse
    analysis_task = {
        'id': 'architect_test',
        'type': 'analysis', 
        'description': 'Application web de gestion de tâches avec utilisateurs, authentification JWT, base de données PostgreSQL et API REST'
    }
    
    print("📋 Étape 1: Analyse du projet")
    analysis_result = await analysis_agent.start_task(analysis_task)
    
    if not analysis_result['success']:
        print(f"❌ Échec de l'analyse: {analysis_result['error']}")
        return
    
    print(f"✅ Analyse terminée: {analysis_result['project_type']} ({analysis_result['complexity']})")
    
    # Étape 2: Architecture
    architect_task = {
        'id': 'architect_test',
        'type': 'architect',
        'description': analysis_task['description'],
        'context': {'analysis': analysis_result}
    }
    
    print("\n🏗️  Étape 2: Conception de l'architecture")
    architect_result = await architect_agent.start_task(architect_task)
    
    if architect_result['success']:
        print("✅ Architecture conçue avec succès!")
        
        # Affichage des résultats
        tech_stack = architect_result['technology_stack']
        print(f"\n🔧 Stack technologique:")
        for tech, value in tech_stack.items():
            print(f"   • {tech}: {value}")
        
        structure = architect_result['project_structure']
        print(f"\n🏗️  Structure: {structure['pattern']}")
        print(f"   Couches: {', '.join(structure['layers'])}")
        
        api_design = architect_result['api_design']
        if api_design.get('type') != 'none':
            print(f"\n🌐 API: {api_design['style']} - {len(api_design['endpoints'])} endpoints")
            for endpoint in api_design['endpoints'][:3]:  # 3 premiers
                print(f"   • {endpoint['method']} {endpoint['path']}")
        
        deployment = architect_result['deployment_strategy']
        print(f"\n🚀 Déploiement: {deployment['strategy']}")
        print(f"   Plateforme: {deployment['platform']}")
        
        dependencies = architect_result['dependencies']
        print(f"\n📦 Dépendances principales:")
        for category, deps in dependencies.items():
            print(f"   • {category}: {len(deps)} packages")
    
    else:
        print(f"❌ Erreur architecture: {architect_result['error']}")
    
    # Performance
    print(f"\n📊 Performance Architecte:")
    perf = architect_agent.get_performance_summary()
    print(f"   Tâches: {perf['total_tasks']} | Succès: {perf['success_rate_percent']}% | Coût: {perf['total_cost_euros']}€")

if __name__ == "__main__":
    asyncio.run(test_architect_with_analysis())
