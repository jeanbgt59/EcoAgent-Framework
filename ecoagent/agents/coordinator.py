"""
EcoAgent Framework - Agent Coordinateur
Orchestre l'ensemble des agents et gère les workflows
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from .base_agent import BaseAgent, AgentStatus

class AgentCoordinator(BaseAgent):
    """
    Agent coordinateur principal qui remplace les 67+ agents de DafnckMachine
    par une approche plus économique et efficace
    """
    
    def __init__(self):
        super().__init__(
            name="Coordinateur",
            description="Orchestre tous les agents et gère les workflows de développement",
            model_preference="local"
        )
        
        # Registry des agents disponibles
        self.available_agents: Dict[str, BaseAgent] = {}
        self.workflow_templates: Dict[str, List[str]] = {}
        
        # État du workflow en cours
        self.current_workflow: Optional[Dict[str, Any]] = None
        self.workflow_history: List[Dict[str, Any]] = []
        
        # Statistiques globales
        self.total_workflows = 0
        self.successful_workflows = 0
        
        self._setup_default_workflows()
        
    def register_agent(self, agent: BaseAgent):
        """Enregistre un nouvel agent dans le système"""
        self.available_agents[agent.name] = agent
        self.logger.info(f"Agent {agent.name} enregistré")
    
    def _setup_default_workflows(self):
        """Configure les workflows par défaut"""
        self.workflow_templates = {
            'simple_task': ['analysis', 'coder'],
            'web_app': ['analysis', 'architect', 'coder', 'tester', 'documenter'],
            'full_project': ['analysis', 'architect', 'coder', 'reviewer', 'tester', 'documenter', 'git'],
            'bug_fix': ['analysis', 'coder', 'tester', 'reviewer'],
            'refactoring': ['analysis', 'architect', 'coder', 'reviewer', 'tester'],
            'documentation': ['analysis', 'documenter']
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute un workflow complet de développement
        """
        workflow_type = task.get('workflow_type', 'simple_task')
        project_description = task.get('description', '')
        
        self.logger.info(f"Début workflow '{workflow_type}' : {project_description}")
        
        # Sélection du workflow approprié
        if workflow_type not in self.workflow_templates:
            return {
                'success': False,
                'error': f"Type de workflow '{workflow_type}' inconnu",
                'available_workflows': list(self.workflow_templates.keys())
            }
        
        workflow_steps = self.workflow_templates[workflow_type]
        
        # Estimation des coûts totaux
        total_estimated_cost = await self._estimate_workflow_cost(task, workflow_steps)
        
        # Confirmation utilisateur si nécessaire
        from ..core.config import config
        if total_estimated_cost > config.cost_limits.require_confirmation_above_euros:
            # TODO: Implémenter confirmation utilisateur
            self.logger.warning(f"Coût estimé élevé: {total_estimated_cost:.4f}€")
        
        # Exécution séquentielle des étapes
        workflow_result = {
            'success': True,
            'workflow_type': workflow_type,
            'steps_completed': [],
            'steps_failed': [],
            'total_cost': 0.0,
            'outputs': {},
            'timeline': []
        }
        
        for step_name in workflow_steps:
            step_result = await self._execute_workflow_step(step_name, task, workflow_result)
            
            if step_result['success']:
                workflow_result['steps_completed'].append(step_name)
                workflow_result['outputs'][step_name] = step_result.get('output', {})
            else:
                workflow_result['steps_failed'].append(step_name)
                workflow_result['success'] = False
                # En cas d'échec, on peut continuer ou s'arrêter selon la criticité
                if step_name in ['analysis', 'architect']:  # Étapes critiques
                    break
            
            workflow_result['total_cost'] += step_result.get('actual_cost', 0.0)
            workflow_result['timeline'].append({
                'step': step_name,
                'timestamp': step_result.get('timestamp'),
                'duration': step_result.get('duration'),
                'success': step_result['success']
            })
        
        # Mise à jour des statistiques
        self.total_workflows += 1
        if workflow_result['success']:
            self.successful_workflows += 1
        
        self.workflow_history.append(workflow_result)
        
        return workflow_result
    
    async def _execute_workflow_step(self, step_name: str, original_task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute une étape spécifique du workflow"""
        
        if step_name not in self.available_agents:
            return {
                'success': False,
                'error': f"Agent '{step_name}' non disponible",
                'step': step_name
            }
        
        agent = self.available_agents[step_name]
        
        # Préparation de la tâche pour cet agent
        agent_task = {
            'id': f"{original_task.get('id', 'unknown')}_{step_name}",
            'type': step_name,
            'description': original_task.get('description', ''),
            'context': context['outputs'],  # Résultats des étapes précédentes
            'requirements': original_task.get('requirements', {}),
            'previous_outputs': context['outputs']
        }
        
        # Exécution de la tâche par l'agent
        return await agent.start_task(agent_task)
    
    async def _estimate_workflow_cost(self, task: Dict[str, Any], workflow_steps: List[str]) -> float:
        """Estime le coût total d'un workflow"""
        total_cost = 0.0
        
        for step_name in workflow_steps:
            if step_name in self.available_agents:
                agent = self.available_agents[step_name]
                step_task = {
                    'type': step_name,
                    'description': task.get('description', ''),
                    'complexity': task.get('complexity', 'medium')
                }
                step_cost = agent.estimate_task_cost(step_task)
                total_cost += step_cost
        
        return total_cost
    
    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """Le coordinateur peut gérer tous les types de workflows"""
        workflow_type = task.get('workflow_type', 'simple_task')
        return workflow_type in self.workflow_templates
    
    def estimate_task_cost(self, task: Dict[str, Any]) -> float:
        """Estime le coût d'un workflow complet"""
        workflow_type = task.get('workflow_type', 'simple_task')
        if workflow_type not in self.workflow_templates:
            return 0.0
        
        # Estimation simplifiée basée sur le type de workflow
        base_costs = {
            'simple_task': 0.0,      # Ollama uniquement
            'web_app': 0.02,         # Quelques appels API si nécessaire
            'full_project': 0.10,    # Projet complet
            'bug_fix': 0.01,         # Simple correction
            'refactoring': 0.05,     # Refactoring moyen
            'documentation': 0.0     # Ollama uniquement
        }
        
        return base_costs.get(workflow_type, 0.02)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retourne l'état complet du système"""
        agent_statuses = {}
        for name, agent in self.available_agents.items():
            agent_statuses[name] = agent.get_performance_summary()
        
        return {
            'coordinator': self.get_performance_summary(),
            'agents': agent_statuses,
            'total_workflows': self.total_workflows,
            'successful_workflows': self.successful_workflows,
            'success_rate': (self.successful_workflows / max(1, self.total_workflows)) * 100,
            'available_workflow_types': list(self.workflow_templates.keys()),
            'current_workflow': self.current_workflow is not None
        }
    
    def suggest_workflow_type(self, description: str) -> str:
        """Suggère le type de workflow le plus approprié"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['bug', 'fix', 'erreur', 'problème']):
            return 'bug_fix'
        elif any(word in description_lower for word in ['web', 'app', 'application', 'site']):
            return 'web_app'
        elif any(word in description_lower for word in ['doc', 'documentation', 'readme']):
            return 'documentation'
        elif any(word in description_lower for word in ['refactor', 'améliorer', 'optimiser']):
            return 'refactoring'
        elif any(word in description_lower for word in ['projet', 'complet', 'full', 'application complète']):
            return 'full_project'
        else:
            return 'simple_task'

# Instance globale du coordinateur
coordinator = AgentCoordinator()
