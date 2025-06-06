"""
EcoAgent Framework - Agent de base
Classe abstraite pour tous les agents du système
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum

class AgentStatus(Enum):
    """États possibles d'un agent"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"

class BaseAgent(ABC):
    """
    Classe de base pour tous les agents EcoAgent
    Implémente les fonctionnalités communes et l'interface standard
    """
    
    def __init__(self, 
                 name: str, 
                 description: str,
                 model_preference: str = "local"):
        """
        Initialise un agent de base
        
        Args:
            name: Nom unique de l'agent
            description: Description de la fonction de l'agent
            model_preference: "local" (Ollama prioritaire) ou "api" (API prioritaire)
        """
        self.name = name
        self.description = description
        self.model_preference = model_preference
        self.status = AgentStatus.IDLE
        
        # Configuration
        self.logger = logging.getLogger(f"ecoagent.agents.{name.lower()}")
        self.creation_time = time.time()
        self.last_activity = time.time()
        
        # Historique des tâches
        self.task_history: List[Dict[str, Any]] = []
        self.current_task: Optional[Dict[str, Any]] = None
        
        # Métriques
        self.total_tasks = 0
        self.successful_tasks = 0
        self.failed_tasks = 0
        self.total_cost_euros = 0.0
        
        self.logger.info(f"Agent {self.name} initialisé")
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une tâche spécifique à l'agent
        
        Args:
            task: Dictionnaire contenant les détails de la tâche
            
        Returns:
            Résultat de la tâche avec métadonnées
        """
        pass
    
    @abstractmethod
    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """
        Détermine si l'agent peut gérer une tâche donnée
        
        Args:
            task: Dictionnaire décrivant la tâche
            
        Returns:
            True si l'agent peut gérer la tâche
        """
        pass
    
    @abstractmethod
    def estimate_task_cost(self, task: Dict[str, Any]) -> float:
        """
        Estime le coût en euros pour exécuter une tâche
        
        Args:
            task: Dictionnaire décrivant la tâche
            
        Returns:
            Coût estimé en euros
        """
        pass
    
    def get_model_config(self) -> Dict[str, Any]:
        """Retourne la configuration optimale de modèle pour cet agent"""
        from ..core.resource_manager import resource_manager
        
        base_config = resource_manager.get_optimal_model_config()
        
        # Personnalisation selon le type d'agent
        if hasattr(self, 'specialized_model'):
            if self.specialized_model in base_config:
                base_config['selected_model'] = base_config[self.specialized_model]
            else:
                base_config['selected_model'] = base_config.get('primary_model', 'mistral:7b')
        else:
            base_config['selected_model'] = base_config.get('primary_model', 'mistral:7b')
            
        return base_config
    
    async def start_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Point d'entrée principal pour exécuter une tâche
        Gère les métriques, logging et gestion d'erreurs
        """
        task_start_time = time.time()
        self.current_task = task
        self.status = AgentStatus.WORKING
        self.last_activity = task_start_time
        
        # Vérification préalable
        if not self.can_handle_task(task):
            error_msg = f"Agent {self.name} ne peut pas gérer cette tâche"
            self.logger.error(error_msg)
            self.status = AgentStatus.ERROR
            return {
                'success': False,
                'error': error_msg,
                'agent': self.name,
                'duration': 0.0
            }
        
        # Estimation du coût
        estimated_cost = self.estimate_task_cost(task)
        self.logger.info(f"Début tâche {task.get('id', 'unknown')} - Coût estimé: {estimated_cost:.4f}€")
        
        try:
            # Exécution de la tâche
            result = await self.execute_task(task)
            
            # Mise à jour des métriques
            duration = time.time() - task_start_time
            actual_cost = result.get('cost', estimated_cost)
            
            self._update_metrics(True, duration, actual_cost)
            self.status = AgentStatus.COMPLETED
            
            # Enrichissement du résultat
            result.update({
                'agent': self.name,
                'duration': duration,
                'estimated_cost': estimated_cost,
                'actual_cost': actual_cost,
                'timestamp': task_start_time
            })
            
            self.logger.info(f"Tâche terminée avec succès en {duration:.2f}s - Coût: {actual_cost:.4f}€")
            return result
            
        except Exception as e:
            # Gestion d'erreur
            duration = time.time() - task_start_time
            self._update_metrics(False, duration, 0.0)
            self.status = AgentStatus.ERROR
            
            error_msg = f"Erreur lors de l'exécution: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'agent': self.name,
                'duration': duration,
                'estimated_cost': estimated_cost,
                'actual_cost': 0.0,
                'timestamp': task_start_time
            }
        finally:
            self.current_task = None
            self.last_activity = time.time()
    
    def _update_metrics(self, success: bool, duration: float, cost: float):
        """Met à jour les métriques de performance"""
        self.total_tasks += 1
        self.total_cost_euros += cost
        
        if success:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1
        
        # Enregistrement dans l'historique
        task_record = {
            'success': success,
            'duration': duration,
            'cost': cost,
            'timestamp': time.time(),
            'task_id': self.current_task.get('id', 'unknown') if self.current_task else 'unknown'
        }
        
        self.task_history.append(task_record)
        
        # Limite l'historique à 100 entrées
        if len(self.task_history) > 100:
            self.task_history = self.task_history[-100:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des performances de l'agent"""
        success_rate = (self.successful_tasks / max(1, self.total_tasks)) * 100
        avg_duration = 0.0
        
        if self.task_history:
            avg_duration = sum(t['duration'] for t in self.task_history) / len(self.task_history)
        
        return {
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'total_tasks': self.total_tasks,
            'successful_tasks': self.successful_tasks,
            'failed_tasks': self.failed_tasks,
            'success_rate_percent': round(success_rate, 1),
            'total_cost_euros': round(self.total_cost_euros, 4),
            'average_duration_seconds': round(avg_duration, 2),
            'uptime_minutes': round((time.time() - self.creation_time) / 60, 1)
        }
    
    def reset_metrics(self):
        """Remet à zéro les métriques de performance"""
        self.task_history.clear()
        self.total_tasks = 0
        self.successful_tasks = 0
        self.failed_tasks = 0
        self.total_cost_euros = 0.0
        self.logger.info(f"Métriques de {self.name} remises à zéro")
    
    def __str__(self) -> str:
        return f"Agent({self.name}, status={self.status.value}, tasks={self.total_tasks})"
    
    def __repr__(self) -> str:
        return self.__str__()
