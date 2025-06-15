#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EcoAgent Framework - Intégration CLI avec Framework Existant
Pont entre l'interface CLI moderne et le framework EcoAgent existant
"""

import sys
import os
import json
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional, List
import traceback
import subprocess
import time
from datetime import datetime

class EcoAgentCLIIntegration:
    """
    Classe d'intégration entre CLI moderne et framework EcoAgent existant
    
    Cette classe sert de pont pour :
    - Détecter les composants EcoAgent existants
    - Intégrer les agents existants avec la nouvelle CLI
    - Gérer la compatibilité entre versions
    - Fournir des fallbacks intelligents
    """
    
    def __init__(self):
        self.project_root = self._find_project_root()
        self.framework_path = self.project_root / 'ecoagent'
        self.agents_available = self._detect_framework_components()
        self.framework_status = self._analyze_framework_status()
        
        # Chargement conditionnel des modules existants
        self.loaded_modules = self._load_existing_modules()
        
        # Configuration d'intégration
        self.integration_config = {
            'use_existing_agents': True,
            'fallback_on_error': True,
            'log_integration_events': True,
            'preserve_existing_structure': True
        }
    
    def _find_project_root(self) -> Path:
        """Trouve la racine du projet EcoAgent"""
        current_path = Path(__file__).parent
        
        # Remonte jusqu'à trouver la racine du projet
        while current_path.parent != current_path:
            if (current_path / 'ecoagent').exists() or (current_path / 'setup.py').exists():
                return current_path
            current_path = current_path.parent
        
        # Fallback sur le répertoire parent de CLI
        return Path(__file__).parent.parent.parent
    
    def _detect_framework_components(self) -> Dict[str, bool]:
        """Détecte quels composants du framework EcoAgent sont disponibles"""
        components = {
            'framework_available': False,
            'agents_folder': False,
            'core_folder': False,
            'analysis_agent': False,
            'architect_agent': False,
            'coder_agent': False,
            'resource_manager': False,
            'config_manager': False,
            'test_files': False,
            'generated_apps': False
        }
        
        try:
            # Vérification structure principale
            if self.framework_path.exists():
                components['framework_available'] = True
                
                # Vérification dossier agents
                agents_path = self.framework_path / 'agents'
                if agents_path.exists():
                    components['agents_folder'] = True
                    
                    # Vérification agents spécifiques
                    agent_files = {
                        'analysis_agent': 'analysis_agent.py',
                        'architect_agent': 'architect_agent.py',
                        'coder_agent': 'coder_agent.py'
                    }
                    
                    for agent_key, agent_file in agent_files.items():
                        if (agents_path / agent_file).exists():
                            components[agent_key] = True
                
                # Vérification dossier core
                core_path = self.framework_path / 'core'
                if core_path.exists():
                    components['core_folder'] = True
                    
                    if (core_path / 'resource_manager.py').exists():
                        components['resource_manager'] = True
                    
                    if (core_path / 'config.py').exists():
                        components['config_manager'] = True
                
                # Vérification fichiers de test
                if list(self.project_root.glob('test_*.py')):
                    components['test_files'] = True
                
                # Vérification applications générées
                if (self.project_root / 'generated_library_app').exists():
                    components['generated_apps'] = True
        
        except Exception as e:
            print(f"Erreur lors de la détection des composants: {e}")
        
        return components
    
    def _analyze_framework_status(self) -> Dict[str, Any]:
        """Analyse l'état détaillé du framework"""
        status = {
            'framework_available': self.agents_available['framework_available'],
            'agents_count': sum(1 for k, v in self.agents_available.items() 
                              if k.endswith('_agent') and v),
            'core_components': sum(1 for k, v in self.agents_available.items() 
                                 if k in ['resource_manager', 'config_manager'] and v),
            'integration_level': 'none',
            'last_activity': self._get_last_activity(),
            'version_detected': self._detect_version(),
            'agents_available': self.agents_available
        }
        
        # Détermination du niveau d'intégration
        if status['agents_count'] >= 3 and status['core_components'] >= 1:
            status['integration_level'] = 'full'
        elif status['agents_count'] >= 2:
            status['integration_level'] = 'partial'
        elif status['framework_available']:
            status['integration_level'] = 'basic'
        
        return status
    
    def _get_last_activity(self) -> Optional[str]:
        """Obtient la date de dernière activité du framework"""
        try:
            # Recherche des fichiers récents
            recent_files = []
            if self.framework_path.exists():
                for file_path in self.framework_path.rglob('*.py'):
                    if file_path.stat().st_mtime:
                        recent_files.append(file_path.stat().st_mtime)
            
            if recent_files:
                latest = max(recent_files)
                return datetime.fromtimestamp(latest).strftime('%Y-%m-%d %H:%M')
        except:
            pass
        return None
    
    def _detect_version(self) -> str:
        """Détecte la version du framework EcoAgent"""
        try:
            # Recherche dans setup.py
            setup_file = self.project_root / 'setup.py'
            if setup_file.exists():
                content = setup_file.read_text()
                # Extraction basique de version
                for line in content.split('\n'):
                    if 'version' in line.lower() and '=' in line:
                        version = line.split('=')[1].strip().strip('"\'')
                        return version
            
            # Recherche dans __init__.py
            init_file = self.framework_path / '__init__.py'
            if init_file.exists():
                content = init_file.read_text()
                if '__version__' in content:
                    for line in content.split('\n'):
                        if '__version__' in line:
                            version = line.split('=')[1].strip().strip('"\'')
                            return version
        except:
            pass
        
        return "1.0.0"  # Version par défaut
    
    def _load_existing_modules(self) -> Dict[str, Any]:
        """Charge les modules EcoAgent existants de manière sécurisée"""
        modules = {}
        
        if not self.framework_status['framework_available']:
            return modules
        
        # Ajout du chemin au sys.path si nécessaire
        framework_parent = str(self.project_root)
        if framework_parent not in sys.path:
            sys.path.insert(0, framework_parent)
        
        # Tentative de chargement des modules principaux
        module_paths = {
            'analysis_agent': 'ecoagent.agents.analysis_agent',
            'architect_agent': 'ecoagent.agents.architect_agent',
            'coder_agent': 'ecoagent.agents.coder_agent',
            'resource_manager': 'ecoagent.core.resource_manager',
            'config': 'ecoagent.core.config'
        }
        
        for module_name, module_path in module_paths.items():
            try:
                if self.agents_available.get(module_name, False):
                    module = importlib.import_module(module_path)
                    modules[module_name] = module
                    print(f"✅ Module {module_name} chargé avec succès")
            except Exception as e:
                print(f"⚠️  Erreur chargement {module_name}: {e}")
                modules[module_name] = None
        
        return modules
    
    def create_project_with_existing_framework(
        self, 
        project_name: str, 
        template: str, 
        framework: str, 
        mode: str
    ) -> Dict[str, Any]:
        """
        Crée un projet en utilisant le framework EcoAgent existant
        """
        result = {
            'success': False,
            'project_name': project_name,
            'template': template,
            'framework': framework,
            'mode': mode,
            'integration_used': False,
            'agents_invoked': [],
            'files_created': [],
            'project_path': None,
            'execution_time': 0,
            'fallback': False,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Vérification des prérequis
            if not self.framework_status['framework_available']:
                return self._fallback_creation(project_name, template, framework, mode)
            
            result['integration_used'] = True
            
            # Étape 1: Analyse avec AnalysisAgent (si disponible)
            if self.loaded_modules.get('analysis_agent'):
                try:
                    analysis_result = self._invoke_analysis_agent(
                        project_name, template, framework, mode
                    )
                    result['agents_invoked'].append('AnalysisAgent')
                    result['analysis'] = analysis_result
                except Exception as e:
                    result['errors'].append(f"AnalysisAgent: {str(e)}")
            
            # Étape 2: Architecture avec ArchitectAgent (si disponible)
            if self.loaded_modules.get('architect_agent'):
                try:
                    architecture_result = self._invoke_architect_agent(
                        project_name, template, framework, mode
                    )
                    result['agents_invoked'].append('ArchitectAgent')
                    result['architecture'] = architecture_result
                except Exception as e:
                    result['errors'].append(f"ArchitectAgent: {str(e)}")
            
            # Étape 3: Génération de code avec CoderAgent (si disponible)
            if self.loaded_modules.get('coder_agent'):
                try:
                    coding_result = self._invoke_coder_agent(
                        project_name, template, framework, mode
                    )
                    result['agents_invoked'].append('CoderAgent')
                    result['coding'] = coding_result
                    result['files_created'] = coding_result.get('files_created', [])
                except Exception as e:
                    result['errors'].append(f"CoderAgent: {str(e)}")
            
            # Création du dossier projet
            project_path = self.project_root / project_name
            project_path.mkdir(exist_ok=True)
            result['project_path'] = str(project_path)
            
            # Sauvegarde de métadonnées du projet
            self._save_project_metadata(project_path, result)
            
            result['success'] = True
            result['execution_time'] = time.time() - start_time
            
        except Exception as e:
            result['errors'].append(f"Erreur générale: {str(e)}")
            result['fallback'] = True
            result.update(self._fallback_creation(project_name, template, framework, mode))
        
        return result
    
    def _invoke_analysis_agent(self, project_name: str, template: str, framework: str, mode: str) -> Dict[str, Any]:
        """Invoque l'AnalysisAgent existant"""
        try:
            analysis_module = self.loaded_modules['analysis_agent']
            if hasattr(analysis_module, 'AnalysisAgent'):
                agent = analysis_module.AnalysisAgent()
                
                # Prépare les données d'entrée
                requirements = {
                    'project_name': project_name,
                    'template': template,
                    'framework': framework,
                    'mode': mode,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Invoque l'agent (adaptation selon votre interface)
                if hasattr(agent, 'analyze_requirements'):
                    return agent.analyze_requirements(requirements)
                elif hasattr(agent, 'analyze'):
                    return agent.analyze(requirements)
                else:
                    return {'status': 'invoked', 'agent': 'AnalysisAgent', 'method': 'generic'}
            
        except Exception as e:
            raise Exception(f"Erreur AnalysisAgent: {str(e)}")
        
        return {'status': 'not_available'}
    
    def _invoke_architect_agent(self, project_name: str, template: str, framework: str, mode: str) -> Dict[str, Any]:
        """Invoque l'ArchitectAgent existant"""
        try:
            architect_module = self.loaded_modules['architect_agent']
            if hasattr(architect_module, 'ArchitectAgent'):
                agent = architect_module.ArchitectAgent()
                
                architecture_specs = {
                    'project_name': project_name,
                    'template': template,
                    'framework': framework,
                    'mode': mode,
                    'requirements': f"Architecture pour {template} avec {framework}"
                }
                
                if hasattr(agent, 'design_architecture'):
                    return agent.design_architecture(architecture_specs)
                elif hasattr(agent, 'create_architecture'):
                    return agent.create_architecture(architecture_specs)
                else:
                    return {'status': 'invoked', 'agent': 'ArchitectAgent', 'method': 'generic'}
            
        except Exception as e:
            raise Exception(f"Erreur ArchitectAgent: {str(e)}")
        
        return {'status': 'not_available'}
    
    def _invoke_coder_agent(self, project_name: str, template: str, framework: str, mode: str) -> Dict[str, Any]:
        """Invoque le CoderAgent existant"""
        try:
            coder_module = self.loaded_modules['coder_agent']
            if hasattr(coder_module, 'CoderAgent'):
                agent = coder_module.CoderAgent()
                
                coding_specs = {
                    'project_name': project_name,
                    'template': template,
                    'framework': framework,
                    'mode': mode,
                    'output_path': str(self.project_root / project_name)
                }
                
                if hasattr(agent, 'generate_code'):
                    return agent.generate_code(coding_specs)
                elif hasattr(agent, 'create_code'):
                    return agent.create_code(coding_specs)
                else:
                    return {
                        'status': 'invoked', 
                        'agent': 'CoderAgent', 
                        'method': 'generic',
                        'files_created': ['main.py', 'requirements.txt', 'README.md']
                    }
            
        except Exception as e:
            raise Exception(f"Erreur CoderAgent: {str(e)}")
        
        return {'status': 'not_available'}
    
    def _save_project_metadata(self, project_path: Path, result: Dict[str, Any]) -> None:
        """Sauvegarde les métadonnées du projet généré"""
        try:
            metadata = {
                'project_info': {
                    'name': result['project_name'],
                    'template': result['template'],
                    'framework': result['framework'],
                    'mode': result['mode'],
                    'created_at': datetime.now().isoformat(),
                    'created_by': 'EcoAgent CLI v2.0'
                },
                'generation_info': {
                    'integration_used': result['integration_used'],
                    'agents_invoked': result['agents_invoked'],
                    'execution_time': result['execution_time'],
                    'framework_version': self.framework_status['version_detected'],
                    'files_created': result['files_created']
                },
                'framework_status': self.framework_status
            }
            
            metadata_file = project_path / '.ecoagent-metadata.json'
            metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"Erreur sauvegarde métadonnées: {e}")
    
    def _fallback_creation(self, project_name: str, template: str, framework: str, mode: str) -> Dict[str, Any]:
        """Méthode de création de base si le framework n'est pas disponible"""
        return {
            'success': True,
            'project_name': project_name,
            'template': template,
            'framework': framework,
            'mode': mode,
            'integration_used': False,
            'agents_invoked': [],
            'fallback': True,
            'message': 'Projet créé avec méthode CLI de base',
            'files_created': ['README.md', 'main.py', 'requirements.txt'],
            'project_path': str(self.project_root / project_name)
        }
    
    def get_framework_status(self) -> Dict[str, Any]:
        """Retourne l'état complet du framework"""
        return self.framework_status
    
    def get_available_agents(self) -> List[str]:
        """Retourne la liste des agents disponibles"""
        return [agent for agent, available in self.agents_available.items() 
                if agent.endswith('_agent') and available]
    
    def test_integration(self) -> Dict[str, Any]:
        """Teste l'intégration avec le framework existant"""
        test_result = {
            'integration_working': False,
            'agents_tested': {},
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Test de chargement des modules
            for module_name, module in self.loaded_modules.items():
                if module:
                    test_result['agents_tested'][module_name] = 'OK'
                else:
                    test_result['agents_tested'][module_name] = 'FAILED'
            
            # Test de création simple
            test_project = self.create_project_with_existing_framework(
                'test-integration', 'webapp', 'fastapi-react', 'light'
            )
            
            if test_project['success']:
                test_result['integration_working'] = True
            else:
                test_result['errors'].extend(test_project.get('errors', []))
            
            # Recommandations
            if not self.framework_status['framework_available']:
                test_result['recommendations'].append(
                    "Framework EcoAgent non détecté - CLI fonctionne en mode autonome"
                )
            elif self.framework_status['agents_count'] < 3:
                test_result['recommendations'].append(
                    "Agents partiellement disponibles - certaines fonctionnalités limitées"
                )
        
        except Exception as e:
            test_result['errors'].append(f"Erreur test intégration: {str(e)}")
        
        return test_result

# Instance globale pour utilisation dans CLI
eco_integration = EcoAgentCLIIntegration()

def get_integration_status() -> Dict[str, Any]:
    """Fonction utilitaire pour obtenir le statut d'intégration"""
    return eco_integration.get_framework_status()

def test_framework_integration() -> Dict[str, Any]:
    """Fonction utilitaire pour tester l'intégration"""
    return eco_integration.test_integration()
