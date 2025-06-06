#!/usr/bin/env python3
"""
Test de l'agent d'analyse
"""

import asyncio
import sys
import os

# Ajout du chemin du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecoagent.agents.analysis_agent import analysis_agent

async def test_analysis():
    print("🧪 Test de l'Agent d'Analyse")
    print("=" * 40)
    
    # Test 1: Application web complexe
    task1 = {
        'id': 'test_1',
        'type': 'analysis',
        'description': 'Créer une application web FastAPI pour gérer une liste de tâches avec base de données PostgreSQL, authentification utilisateur et API REST'
    }
    
    print("📋 Test 1: Application web complexe")
    result1 = await analysis_agent.start_task(task1)
    
    if result1['success']:
        print(f"✅ Type de projet: {result1['project_type']}")
        print(f"🎯 Complexité: {result1['complexity']}")
        print(f"⚡ Workflow recommandé: {result1['recommended_workflow']}")
        print(f"⏱️  Estimation: {result1['resource_estimate']['time_hours']}h")
        print(f"💰 Coût: {result1['resource_estimate']['cost_euros']}€")
        print(f"📝 Étapes: {len(result1['action_plan'])}")
        
        # Affichage des suggestions
        if result1['suggestions']:
            print(f"💡 Suggestions: {len(result1['suggestions'])}")
            for suggestion in result1['suggestions'][:2]:  # 2 premières
                print(f"   • {suggestion}")
    else:
        print(f"❌ Erreur: {result1['error']}")
    
    print("\n" + "-" * 40)
    
    # Test 2: Script simple
    task2 = {
        'id': 'test_2', 
        'type': 'analysis',
        'description': 'Script Python simple pour convertir des fichiers CSV en JSON'
    }
    
    print("📋 Test 2: Script simple")
    result2 = await analysis_agent.start_task(task2)
    
    if result2['success']:
        print(f"✅ Type de projet: {result2['project_type']}")
        print(f"🎯 Complexité: {result2['complexity']}")
        print(f"⚡ Workflow recommandé: {result2['recommended_workflow']}")
        print(f"⏱️  Estimation: {result2['resource_estimate']['time_hours']}h")
        print(f"💰 Coût: {result2['resource_estimate']['cost_euros']}€")
    
    print("\n📊 Performance de l'agent:")
    perf = analysis_agent.get_performance_summary()
    print(f"Tâches réalisées: {perf['total_tasks']}")
    print(f"Taux de succès: {perf['success_rate_percent']}%")
    print(f"Coût total: {perf['total_cost_euros']}€")

if __name__ == "__main__":
    asyncio.run(test_analysis())
