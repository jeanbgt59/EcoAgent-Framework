"""
EcoAgent Framework - Agent d'Analyse
Premier agent du workflow : analyse les besoins et définit la stratégie
"""

import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class AnalysisAgent(BaseAgent):
    """
    Agent d'analyse des besoins
    Point d'entrée de tous les workflows de développement
    """
    
    def __init__(self):
        super().__init__(
            name="analysis",
            description="Analyse les besoins, définit les exigences et planifie la stratégie de développement",
            model_preference="local"
        )
        
        # Spécialisation pour l'analyse
        self.specialized_model = "primary_model"  # Utilise le meilleur modèle disponible
        
        # Templates d'analyse
        self.analysis_templates = {
            'web_app': self._web_app_analysis_template(),
            'bug_fix': self._bug_fix_analysis_template(),
            'refactoring': self._refactoring_analysis_template(),
            'documentation': self._documentation_analysis_template(),
            'simple_task': self._simple_task_analysis_template()
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse une demande de développement et produit un plan détaillé
        """
        description = task.get('description', '')
        task_type = task.get('type', 'analysis')
        context = task.get('context', {})
        
        self.logger.info(f"Analyse de la demande: {description[:100]}...")
        
        # Analyse de la complexité
        complexity = self._assess_complexity(description)
        
        # Détection du type de projet
        project_type = self._detect_project_type(description)
        
        # Extraction des exigences
        requirements = self._extract_requirements(description)
        
        # Génération du plan d'action
        action_plan = self._generate_action_plan(project_type, complexity, requirements)
        
        # Estimation des ressources
        resource_estimate = self._estimate_resources(project_type, complexity)
        
        # Suggestions d'amélioration
        suggestions = self._generate_suggestions(description, project_type)
        
        analysis_result = {
            'success': True,
            'project_type': project_type,
            'complexity': complexity,
            'requirements': requirements,
            'action_plan': action_plan,
            'resource_estimate': resource_estimate,
            'suggestions': suggestions,
            'recommended_workflow': self._recommend_workflow(project_type, complexity),
            'technical_stack': self._suggest_tech_stack(project_type, requirements),
            'risk_assessment': self._assess_risks(project_type, complexity)
        }
        
        return analysis_result
    
    def _assess_complexity(self, description: str) -> str:
        """Évalue la complexité du projet"""
        description_lower = description.lower()
        
        # Indicateurs de complexité élevée
        high_complexity_indicators = [
            'base de données', 'database', 'api rest', 'microservices',
            'authentification', 'authentication', 'paiement', 'payment',
            'temps réel', 'real-time', 'machine learning', 'ia', 'ai',
            'distributed', 'kubernetes', 'docker', 'cloud'
        ]
        
        # Indicateurs de complexité moyenne
        medium_complexity_indicators = [
            'web', 'api', 'backend', 'frontend', 'crud',
            'formulaire', 'form', 'validation', 'fichier', 'file'
        ]
        
        # Indicateurs de simplicité
        simple_indicators = [
            'simple', 'basic', 'petit', 'small', 'script',
            'utilitaire', 'utility', 'converter', 'calculatrice'
        ]
        
        high_score = sum(1 for indicator in high_complexity_indicators if indicator in description_lower)
        medium_score = sum(1 for indicator in medium_complexity_indicators if indicator in description_lower)
        simple_score = sum(1 for indicator in simple_indicators if indicator in description_lower)
        
        if high_score >= 2:
            return 'complex'
        elif high_score >= 1 or medium_score >= 2:
            return 'medium'
        elif simple_score >= 1:
            return 'simple'
        else:
            # Par défaut, basé sur la longueur de la description
            return 'medium' if len(description) > 200 else 'simple'
    
    def _detect_project_type(self, description: str) -> str:
        """Détecte le type de projet basé sur la description"""
        description_lower = description.lower()
        
        type_indicators = {
            'web_application': ['web app', 'site web', 'application web', 'webapp', 'website'],
            'api': ['api', 'rest', 'endpoint', 'microservice'],
            'mobile_app': ['mobile', 'app mobile', 'android', 'ios', 'smartphone'],
            'desktop_app': ['desktop', 'application bureau', 'gui', 'interface graphique'],
            'script': ['script', 'automation', 'batch', 'utilitaire'],
            'library': ['bibliothèque', 'library', 'package', 'module'],
            'data_analysis': ['analyse de données', 'data analysis', 'statistiques', 'dashboard'],
            'game': ['jeu', 'game', 'gaming'],
            'documentation': ['documentation', 'doc', 'readme', 'guide']
        }
        
        for project_type, indicators in type_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                return project_type
        
        return 'general_application'
    
    def _extract_requirements(self, description: str) -> Dict[str, List[str]]:
        """Extrait les exigences fonctionnelles et techniques"""
        
        # Exigences fonctionnelles (ce que doit faire l'application)
        functional_requirements = []
        
        # Patterns pour détecter les fonctionnalités
        functionality_patterns = [
            r'(?:doit|devra|permettre de|capable de)\s+([^.!?]+)',
            r'(?:créer|afficher|gérer|envoyer|recevoir|calculer|traiter)\s+([^.!?]+)',
            r'(?:l\'utilisateur peut|on peut|il faut pouvoir)\s+([^.!?]+)'
        ]
        
        for pattern in functionality_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            functional_requirements.extend(matches)
        
        # Exigences techniques (technologies, contraintes)
        technical_requirements = []
        
        tech_keywords = [
            'python', 'javascript', 'react', 'vue', 'angular', 'django', 'flask',
            'fastapi', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker',
            'kubernetes', 'aws', 'azure', 'gcp', 'rest api', 'graphql'
        ]
        
        description_lower = description.lower()
        for keyword in tech_keywords:
            if keyword in description_lower:
                technical_requirements.append(keyword)
        
        # Exigences de performance
        performance_requirements = []
        performance_keywords = ['rapide', 'performant', 'temps réel', 'scalable', 'responsive']
        
        for keyword in performance_keywords:
            if keyword in description_lower:
                performance_requirements.append(keyword)
        
        return {
            'functional': functional_requirements[:10],  # Limite à 10 éléments
            'technical': technical_requirements,
            'performance': performance_requirements
        }
    
    def _generate_action_plan(self, project_type: str, complexity: str, requirements: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """Génère un plan d'action détaillé"""
        
        base_steps = [
            {'step': 'Analyse', 'description': 'Analyse des besoins et définition des exigences', 'status': 'completed'},
            {'step': 'Architecture', 'description': 'Conception de l\'architecture et choix techniques', 'status': 'pending'},
            {'step': 'Développement', 'description': 'Implémentation du code principal', 'status': 'pending'},
            {'step': 'Tests', 'description': 'Tests unitaires et d\'intégration', 'status': 'pending'},
            {'step': 'Documentation', 'description': 'Documentation du code et guide utilisateur', 'status': 'pending'}
        ]
        
        # Ajout d'étapes spécifiques selon le type de projet
        if project_type == 'web_application':
            base_steps.insert(3, {
                'step': 'Frontend', 
                'description': 'Développement de l\'interface utilisateur',
                'status': 'pending'
            })
            base_steps.insert(4, {
                'step': 'Backend', 
                'description': 'Développement de la logique serveur',
                'status': 'pending'
            })
        
        if complexity == 'complex':
            base_steps.insert(2, {
                'step': 'Prototypage',
                'description': 'Création d\'un prototype pour validation',
                'status': 'pending'
            })
            base_steps.append({
                'step': 'Déploiement',
                'description': 'Configuration et déploiement en production',
                'status': 'pending'
            })
        
        return base_steps
    
    def _estimate_resources(self, project_type: str, complexity: str) -> Dict[str, Any]:
        """Estime les ressources nécessaires"""
        
        base_estimates = {
            'simple': {'time_hours': 2, 'agents_needed': 2, 'cost_euros': 0.0},
            'medium': {'time_hours': 8, 'agents_needed': 4, 'cost_euros': 0.02},
            'complex': {'time_hours': 24, 'agents_needed': 6, 'cost_euros': 0.10}
        }
        
        estimate = base_estimates.get(complexity, base_estimates['medium']).copy()
        
        # Ajustements selon le type de projet
        multipliers = {
            'web_application': 1.2,
            'mobile_app': 1.5,
            'api': 0.8,
            'script': 0.5,
            'documentation': 0.3
        }
        
        multiplier = multipliers.get(project_type, 1.0)
        estimate['time_hours'] = int(estimate['time_hours'] * multiplier)
        estimate['cost_euros'] = round(estimate['cost_euros'] * multiplier, 4)
        
        return estimate
    
    def _generate_suggestions(self, description: str, project_type: str) -> List[str]:
        """Génère des suggestions d'amélioration"""
        suggestions = []
        
        description_lower = description.lower()
        
        # Suggestions basées sur les bonnes pratiques
        if 'test' not in description_lower:
            suggestions.append("Ajout de tests automatisés recommandé pour assurer la qualité")
        
        if 'sécurité' not in description_lower and 'security' not in description_lower:
            suggestions.append("Considérer les aspects sécurité (validation, authentification)")
        
        if project_type == 'web_application' and 'responsive' not in description_lower:
            suggestions.append("Prévoir un design responsive pour mobile et tablette")
        
        if 'performance' not in description_lower:
            suggestions.append("Optimiser les performances dès la conception")
        
        if 'documentation' not in description_lower:
            suggestions.append("Prévoir une documentation utilisateur et technique")
        
        return suggestions
    
    def _recommend_workflow(self, project_type: str, complexity: str) -> str:
        """Recommande le type de workflow optimal"""
        
        if complexity == 'complex':
            return 'full_project'
        elif project_type == 'web_application':
            return 'web_app'
        elif project_type == 'documentation':
            return 'documentation'
        elif 'bug' in project_type or 'fix' in project_type:
            return 'bug_fix'
        else:
            return 'simple_task'
    
    def _suggest_tech_stack(self, project_type: str, requirements: Dict[str, List[str]]) -> Dict[str, str]:
        """Suggère une pile technologique appropriée"""
        
        tech_suggestions = {
            'web_application': {
                'backend': 'FastAPI ou Django',
                'frontend': 'React ou Vue.js',
                'database': 'PostgreSQL',
                'deployment': 'Docker + Cloud provider'
            },
            'api': {
                'framework': 'FastAPI',
                'database': 'PostgreSQL ou MongoDB',
                'authentication': 'JWT',
                'documentation': 'OpenAPI/Swagger'
            },
            'script': {
                'language': 'Python',
                'dependencies': 'Minimal',
                'distribution': 'pip package'
            },
            'documentation': {
                'format': 'Markdown',
                'generator': 'MkDocs ou Sphinx',
                'hosting': 'GitHub Pages'
            }
        }
        
        return tech_suggestions.get(project_type, {
            'language': 'Python',
            'framework': 'À déterminer selon les besoins'
        })
    
    def _assess_risks(self, project_type: str, complexity: str) -> List[Dict[str, str]]:
        """Évalue les risques potentiels"""
        risks = []
        
        if complexity == 'complex':
            risks.append({
                'type': 'Complexité technique',
                'level': 'Élevé',
                'mitigation': 'Développement par phases, prototypage'
            })
        
        if project_type == 'web_application':
            risks.append({
                'type': 'Sécurité web',
                'level': 'Moyen',
                'mitigation': 'Validation stricte, authentification robuste'
            })
        
        risks.append({
            'type': 'Évolution des besoins',
            'level': 'Moyen',
            'mitigation': 'Architecture modulaire, documentation claire'
        })
        
        return risks
    
    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """L'agent d'analyse peut gérer toutes les demandes d'analyse"""
        return task.get('type') == 'analysis' or 'description' in task
    
    def estimate_task_cost(self, task: Dict[str, Any]) -> float:
        """L'analyse est toujours gratuite avec Ollama"""
        return 0.0
    
    # Templates privés pour différents types d'analyse
    def _web_app_analysis_template(self):
        return "Template pour applications web..."
    
    def _bug_fix_analysis_template(self):
        return "Template pour correction de bugs..."
    
    def _refactoring_analysis_template(self):
        return "Template pour refactoring..."
    
    def _documentation_analysis_template(self):
        return "Template pour documentation..."
    
    def _simple_task_analysis_template(self):
        return "Template pour tâches simples..."

# Instance de l'agent d'analyse
analysis_agent = AnalysisAgent()
