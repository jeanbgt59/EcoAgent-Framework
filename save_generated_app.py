#!/usr/bin/env python3
"""
Script pour sauvegarder une application générée sur le disque
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecoagent.agents.analysis_agent import analysis_agent
from ecoagent.agents.architect_agent import architect_agent
from ecoagent.agents.coder_agent import coder_agent

async def generate_and_save_app():
    print("🏗️  Génération et sauvegarde d'une application complète")
    print("=" * 60)
    
    # Description du projet
    project_description = "Application web FastAPI pour gérer une bibliothèque avec gestion des livres, des auteurs, authentification JWT, base de données PostgreSQL et API REST complète"
    
    # Pipeline complet
    print("📋 Étape 1: Analyse...")
    analysis_task = {
        'id': 'save_app_test',
        'type': 'analysis',
        'description': project_description
    }
    analysis_result = await analysis_agent.start_task(analysis_task)
    
    print("🏗️  Étape 2: Architecture...")
    architect_task = {
        'id': 'save_app_test',
        'type': 'architect',
        'description': project_description,
        'context': {'analysis': analysis_result}
    }
    architect_result = await architect_agent.start_task(architect_task)
    
    print("💻 Étape 3: Génération du code...")
    coder_task = {
        'id': 'save_app_test',
        'type': 'coder',
        'description': project_description,
        'context': {
            'analysis': analysis_result,
            'architect': architect_result
        }
    }
    coder_result = await coder_agent.start_task(coder_task)
    
    if coder_result['success']:
        # Créer le dossier de destination
        output_dir = "generated_library_app"
        os.makedirs(output_dir, exist_ok=True)
        
        # Sauvegarder tous les fichiers
        generated_files = coder_result['generated_files']
        
        print(f"\n💾 Sauvegarde de {len(generated_files)} fichiers dans '{output_dir}'...")
        
        for file_path, content in generated_files.items():
            # Créer les dossiers nécessaires
            full_path = os.path.join(output_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Sauvegarder le fichier
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ {file_path}")
        
        print(f"\n🎉 Application sauvegardée dans le dossier '{output_dir}'!")
        print(f"📁 Fichiers créés: {len(generated_files)}")
        
        # Afficher les fichiers clés
        key_files = ['main.py', 'requirements.txt', 'Dockerfile', 'docker-compose.yml']
        print(f"\n📋 Fichiers clés pour Docker:")
        for key_file in key_files:
            if key_file in generated_files:
                print(f"   ✅ {key_file}")
                # Afficher le début du contenu
                content_preview = generated_files[key_file][:200] + "..." if len(generated_files[key_file]) > 200 else generated_files[key_file]
                print(f"      Aperçu: {content_preview.split(chr(10))[0]}")
        
        return output_dir, generated_files
    else:
        print(f"❌ Erreur: {coder_result['error']}")
        return None, None

if __name__ == "__main__":
    asyncio.run(generate_and_save_app())
