#!/usr/bin/env python3
"""
Test de l'agent codeur avec pipeline complet Analyse → Architecture → Code
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecoagent.agents.analysis_agent import analysis_agent
from ecoagent.agents.architect_agent import architect_agent
from ecoagent.agents.coder_agent import CoderAgent

# Créez l'instance si l'import de coder_agent échoue
try:
    from ecoagent.agents.coder_agent import coder_agent
except ImportError:
    coder_agent = CoderAgent()

async def test_full_pipeline():
    print("💻 Test complet du Pipeline de Génération de Code")
    print("=" * 60)
    
    # Description du projet à créer
    project_description = "Application web FastAPI pour gérer une bibliothèque avec gestion des livres, des auteurs, authentification JWT, base de données PostgreSQL et API REST complète"
    
    # Étape 1: Analyse
    print("📋 Étape 1: Analyse du projet")
    analysis_task = {
        'id': 'full_pipeline_test',
        'type': 'analysis',
        'description': project_description
    }
    
    analysis_result = await analysis_agent.start_task(analysis_task)
    
    if not analysis_result['success']:
        print(f"❌ Échec de l'analyse: {analysis_result['error']}")
        return
    
    print(f"✅ Analyse terminée: {analysis_result['project_type']} ({analysis_result['complexity']})")
    print(f"   Workflow recommandé: {analysis_result['recommended_workflow']}")
    print(f"   Estimation: {analysis_result['resource_estimate']['time_hours']}h")
    
    # Étape 2: Architecture
    print("\n🏗️  Étape 2: Conception de l'architecture")
    architect_task = {
        'id': 'full_pipeline_test',
        'type': 'architect',
        'description': project_description,
        'context': {'analysis': analysis_result}
    }
    
    architect_result = await architect_agent.start_task(architect_task)
    
    if not architect_result['success']:
        print(f"❌ Échec de l'architecture: {architect_result['error']}")
        return
    
    print("✅ Architecture conçue avec succès!")
    tech_stack = architect_result['technology_stack']
    print(f"   Stack: {tech_stack.get('backend', 'N/A')} + {tech_stack.get('database', 'N/A')}")
    print(f"   API endpoints: {len(architect_result.get('api_design', {}).get('endpoints', []))}")
    
    # Étape 3: Génération de code
    print("\n💻 Étape 3: Génération du code source")
    coder_task = {
        'id': 'full_pipeline_test',
        'type': 'coder',
        'description': project_description,
        'context': {
            'analysis': analysis_result,
            'architect': architect_result
        }
    }
    
    coder_result = await coder_agent.start_task(coder_task)
    
    if coder_result['success']:
        print("✅ Code généré avec succès!")
        print(f"   Fichiers créés: {coder_result['file_count']}")
        print(f"   Point d'entrée: {coder_result['entry_point']}")
        print(f"   Technologies: {', '.join(coder_result['main_technologies'])}")
        
        # Affichage de quelques fichiers générés
        print("\n📁 Fichiers générés (échantillon):")
        generated_files = coder_result['generated_files']
        
        key_files = ['main.py', 'requirements.txt', 'README.md', 'app/config.py', 'app/models/user.py']
        for file_name in key_files:
            if file_name in generated_files:
                size = len(generated_files[file_name])
                print(f"   ✅ {file_name} ({size} caractères)")
        
        # Affichage des commandes d'installation
        print(f"\n🔧 Commandes d'installation:")
        for cmd in coder_result['installation_commands']:
            print(f"   • {cmd}")
        
        # Affichage des commandes de lancement
        print(f"\n🚀 Commandes de lancement:")
        for cmd in coder_result['run_commands']:
            print(f"   • {cmd}")
        
        # Vérification de la cohérence du code généré
        print("\n🔍 Vérification de la cohérence:")
        
        # Vérifiez que les fichiers essentiels sont présents
        essential_files = ['main.py', 'requirements.txt', 'README.md']
        missing_files = [f for f in essential_files if f not in generated_files]
        
        if not missing_files:
            print("   ✅ Tous les fichiers essentiels sont présents")
        else:
            print(f"   ⚠️  Fichiers manquants: {missing_files}")
        
        # Vérifiez que le main.py contient FastAPI
        main_py_content = generated_files.get('main.py', '')
        if 'FastAPI' in main_py_content and 'uvicorn' in main_py_content:
            print("   ✅ Structure FastAPI détectée dans main.py")
        else:
            print("   ⚠️  Structure FastAPI non détectée")
        
        # Vérifiez que les dépendances sont listées
        requirements_content = generated_files.get('requirements.txt', '')
        if 'fastapi' in requirements_content and 'uvicorn' in requirements_content:
            print("   ✅ Dépendances FastAPI présentes")
        else:
            print("   ⚠️  Dépendances FastAPI manquantes")
        
    else:
        print(f"❌ Erreur génération de code: {coder_result['error']}")
    
    # Statistiques finales
    print(f"\n📊 Statistiques du pipeline:")
    
    agents_stats = [
        ("Analyse", analysis_agent.get_performance_summary()),
        ("Architecture", architect_agent.get_performance_summary()), 
        ("Codeur", coder_agent.get_performance_summary())
    ]
    
    total_cost = 0.0
    total_time = 0.0
    
    for agent_name, stats in agents_stats:
        print(f"   {agent_name}: {stats['total_tasks']} tâches | {stats['success_rate_percent']}% succès | {stats['total_cost_euros']}€")
        total_cost += stats['total_cost_euros']
        if stats['total_tasks'] > 0:
            total_time += stats.get('average_duration_seconds', 0)
    
    print(f"\n🎯 RÉSULTAT FINAL:")
    print(f"   Coût total: {total_cost:.4f}€")
    print(f"   Temps moyen: {total_time:.2f}s")
    print(f"   Pipeline: {'✅ SUCCÈS' if coder_result.get('success', False) else '❌ ÉCHEC'}")

async def test_simple_script():
    print("\n" + "=" * 60)
    print("📜 Test Bonus: Génération d'un script simple")
    print("=" * 60)
    
    # Test d'un script simple
    script_description = "Script Python pour convertir des fichiers CSV en JSON avec validation des données"
    
    # Pipeline rapide pour script
    analysis_task = {
        'id': 'script_test',
        'type': 'analysis', 
        'description': script_description
    }
    
    analysis_result = await analysis_agent.start_task(analysis_task)
    
    architect_task = {
        'id': 'script_test',
        'type': 'architect',
        'description': script_description,
        'context': {'analysis': analysis_result}
    }
    
    architect_result = await architect_agent.start_task(architect_task)
    
    coder_task = {
        'id': 'script_test',
        'type': 'coder',
        'description': script_description,
        'context': {
            'analysis': analysis_result,
            'architect': architect_result
        }
    }
    
    coder_result = await coder_agent.start_task(coder_task)
    
    if coder_result['success']:
        print(f"✅ Script généré: {coder_result['file_count']} fichiers")
        
        # Vérifiez que le script principal existe
        if 'main.py' in coder_result['generated_files']:
            main_content = coder_result['generated_files']['main.py']
            if 'argparse' in main_content and 'csv' in main_content:
                print("   ✅ Structure de script CLI détectée")
        
        print(f"   Commandes: {coder_result['run_commands']}")
    else:
        print(f"❌ Erreur script: {coder_result['error']}")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
    asyncio.run(test_simple_script())
