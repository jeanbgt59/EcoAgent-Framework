"""
EcoAgent Framework - Alternative économique aux frameworks multi-agents
"""

__version__ = "1.0.0"
__author__ = "EcoAgent Team"

from .core.config import config
from .core.resource_manager import resource_manager  
from .core.cost_estimator import cost_estimator

__all__ = ['config', 'resource_manager', 'cost_estimator']
