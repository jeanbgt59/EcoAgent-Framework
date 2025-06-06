"""
EcoAgent Framework - Agent Architecte
Conçoit l'architecture technique basée sur l'analyse
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ArchitectAgent(BaseAgent):
    """
    Agent architecte qui conçoit la structure technique du projet
    """
    
    def __init__(self):
        super().__init__(
            name="architect",
            description="Conçoit l'architecture technique, structure des fichiers et choix technologiques",
            model_preference="local"
        )
        
        # Modèle spécialisé pour l'architecture
        self.specialized_model = "primary_model"
        
        # Templates d'architecture
        self.architecture_templates = self._load_architecture_templates()
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conçoit l'architecture technique basée sur l'analyse
        """
        description = task.get('description', '')
        context = task.get('context', {})
        
        # Récupération de l'analyse précédente
        analysis_result = context.get('analysis', {})
        project_type = analysis_result.get('project_type', 'general_application')
        complexity = analysis_result.get('complexity', 'medium')
        requirements = analysis_result.get('requirements', {})
        
        self.logger.info(f"Conception architecture pour {project_type} ({complexity})")
        
        # Génération de l'architecture
        architecture = {
            'success': True,
            'project_structure': self._design_project_structure(project_type, complexity),
            'technology_stack': self._select_technology_stack(project_type, requirements),
            'database_design': self._design_database(project_type, requirements),
            'api_design': self._design_api(project_type, requirements),
            'deployment_strategy': self._design_deployment(complexity),
            'security_considerations': self._design_security(project_type),
            'scalability_plan': self._design_scalability(complexity),
            'file_structure': self._generate_file_structure(project_type),
            'dependencies': self._list_dependencies(project_type),
            'configuration_files': self._generate_config_files(project_type)
        }
        
        return architecture
    
    def _design_project_structure(self, project_type: str, complexity: str) -> Dict[str, Any]:
        """Conçoit la structure générale du projet"""
        
        base_structure = {
            'pattern': 'layered_architecture',
            'layers': ['presentation', 'business', 'data'],
            'principles': ['separation_of_concerns', 'single_responsibility', 'dependency_injection']
        }
        
        if project_type == 'web_application':
            base_structure.update({
                'pattern': 'mvc_pattern',
                'frontend_pattern': 'component_based',
                'backend_pattern': 'rest_api',
                'layers': ['presentation', 'controller', 'service', 'repository', 'model']
            })
        
        elif project_type == 'api':
            base_structure.update({
                'pattern': 'layered_api',
                'layers': ['router', 'service', 'repository', 'model'],
                'api_style': 'REST',
                'documentation': 'OpenAPI/Swagger'
            })
        
        elif project_type == 'script':
            base_structure.update({
                'pattern': 'functional',
                'layers': ['main', 'utils', 'config'],
                'structure': 'simple_modular'
            })
        
        if complexity == 'complex':
            base_structure['additional_patterns'] = ['factory', 'observer', 'strategy']
            base_structure['layers'].extend(['middleware', 'cache', 'monitoring'])
        
        return base_structure
    
    def _select_technology_stack(self, project_type: str, requirements: Dict[str, List[str]]) -> Dict[str, str]:
        """Sélectionne la pile technologique optimale"""
        
        tech_requirements = requirements.get('technical', [])
        
        # Stack par défaut selon le type de projet
        stacks = {
            'web_application': {
                'backend': 'FastAPI',
                'frontend': 'React',
                'database': 'PostgreSQL',
                'cache': 'Redis',
                'webserver': 'Uvicorn',
                'containerization': 'Docker'
            },
            'api': {
                'framework': 'FastAPI',
                'database': 'PostgreSQL',
                'authentication': 'JWT',
                'documentation': 'OpenAPI',
                'testing': 'pytest',
                'containerization': 'Docker'
            },
            'script': {
                'language': 'Python 3.11+',
                'packaging': 'pip',
                'configuration': 'YAML/JSON',
                'logging': 'logging module',
                'testing': 'pytest'
            },
            'data_analysis': {
                'core': 'Python',
                'data_processing': 'pandas',
                'visualization': 'matplotlib/plotly',
                'database': 'PostgreSQL',
                'notebook': 'Jupyter'
            }
        }
        
        selected_stack = stacks.get(project_type, stacks['api']).copy()
        
        # Personnalisation basée sur les exigences
        for tech in tech_requirements:
            tech_lower = tech.lower()
            if 'django' in tech_lower:
                selected_stack['backend'] = 'Django'
            elif 'vue' in tech_lower:
                selected_stack['frontend'] = 'Vue.js'
            elif 'mysql' in tech_lower:
                selected_stack['database'] = 'MySQL'
            elif 'mongodb' in tech_lower:
                selected_stack['database'] = 'MongoDB'
        
        return selected_stack
    
    def _design_database(self, project_type: str, requirements: Dict[str, List[str]]) -> Dict[str, Any]:
        """Conçoit la structure de base de données"""
        
        if project_type == 'script' or 'database' not in str(requirements):
            return {'type': 'none', 'reason': 'No database required for this project type'}
        
        functional_req = requirements.get('functional', [])
        
        # Détection des entités principales
        entities = []
        if any('utilisateur' in req.lower() or 'user' in req.lower() for req in functional_req):
            entities.append('User')
        if any('tâche' in req.lower() or 'task' in req.lower() for req in functional_req):
            entities.append('Task')
        if any('produit' in req.lower() or 'product' in req.lower() for req in functional_req):
            entities.append('Product')
        
        if not entities:
            entities = ['Entity']  # Entité générique
        
        database_design = {
            'type': 'relational',
            'engine': 'PostgreSQL',
            'entities': entities,
            'relationships': self._infer_relationships(entities),
            'indexes': [f"{entity.lower()}_id" for entity in entities],
            'constraints': ['foreign_keys', 'unique_constraints', 'not_null'],
            'migrations': True,
            'seeding': 'development_data'
        }
        
        return database_design
    
    def _infer_relationships(self, entities: List[str]) -> List[Dict[str, str]]:
        """Infère les relations entre entités"""
        relationships = []
        
        if 'User' in entities and 'Task' in entities:
            relationships.append({
                'from': 'User',
                'to': 'Task', 
                'type': 'one_to_many',
                'description': 'Un utilisateur peut avoir plusieurs tâches'
            })
        
        if 'User' in entities and 'Product' in entities:
            relationships.append({
                'from': 'User',
                'to': 'Product',
                'type': 'many_to_many',
                'description': 'Relation utilisateur-produit'
            })
        
        return relationships
    
    def _design_api(self, project_type: str, requirements: Dict[str, List[str]]) -> Dict[str, Any]:
        """Conçoit l'API REST"""
        
        if project_type not in ['web_application', 'api']:
            return {'type': 'none'}
        
        functional_req = requirements.get('functional', [])
        
        # Endpoints basés sur les entités détectées
        endpoints = []
        
        # CRUD basique pour les entités principales
        if any('utilisateur' in req.lower() or 'user' in req.lower() for req in functional_req):
            endpoints.extend([
                {'path': '/users', 'method': 'GET', 'description': 'Liste des utilisateurs'},
                {'path': '/users', 'method': 'POST', 'description': 'Créer un utilisateur'},
                {'path': '/users/{id}', 'method': 'GET', 'description': 'Détails utilisateur'},
                {'path': '/users/{id}', 'method': 'PUT', 'description': 'Modifier utilisateur'},
                {'path': '/users/{id}', 'method': 'DELETE', 'description': 'Supprimer utilisateur'}
            ])
        
        if any('tâche' in req.lower() or 'task' in req.lower() for req in functional_req):
            endpoints.extend([
                {'path': '/tasks', 'method': 'GET', 'description': 'Liste des tâches'},
                {'path': '/tasks', 'method': 'POST', 'description': 'Créer une tâche'},
                {'path': '/tasks/{id}', 'method': 'PUT', 'description': 'Modifier tâche'},
                {'path': '/tasks/{id}', 'method': 'DELETE', 'description': 'Supprimer tâche'}
            ])
        
        # Endpoints par défaut si rien détecté
        if not endpoints:
            endpoints = [
                {'path': '/health', 'method': 'GET', 'description': 'Health check'},
                {'path': '/api/v1/items', 'method': 'GET', 'description': 'Liste des éléments'},
                {'path': '/api/v1/items', 'method': 'POST', 'description': 'Créer un élément'}
            ]
        
        api_design = {
            'style': 'REST',
            'version': 'v1',
            'base_url': '/api/v1',
            'endpoints': endpoints,
            'authentication': 'JWT' if 'auth' in str(requirements).lower() else 'optional',
            'documentation': 'OpenAPI 3.0',
            'rate_limiting': True,
            'cors': True,
            'response_format': 'JSON'
        }
        
        return api_design
    
    def _design_deployment(self, complexity: str) -> Dict[str, Any]:
        """Conçoit la stratégie de déploiement"""
        
        if complexity == 'simple':
            return {
                'strategy': 'single_server',
                'platform': 'VPS ou shared hosting',
                'containerization': 'optional',
                'ci_cd': 'simple'
            }
        
        elif complexity == 'medium':
            return {
                'strategy': 'docker_containers',
                'platform': 'Cloud provider (OVH, AWS, Azure)',
                'containerization': 'Docker',
                'orchestration': 'docker-compose',
                'ci_cd': 'GitHub Actions',
                'monitoring': 'basic_logging'
            }
        
        else:  # complex
            return {
                'strategy': 'microservices',
                'platform': 'Kubernetes cluster',
                'containerization': 'Docker',
                'orchestration': 'Kubernetes',
                'ci_cd': 'GitLab CI/GitHub Actions',
                'monitoring': 'Prometheus + Grafana',
                'load_balancing': 'nginx ou cloud load balancer',
                'scaling': 'horizontal auto-scaling'
            }
    
    def _design_security(self, project_type: str) -> List[str]:
        """Conçoit les considérations de sécurité"""
        
        base_security = [
            'Input validation',
            'SQL injection prevention',
            'XSS protection',
            'CSRF protection',
            'Secure headers',
            'Environment variables for secrets'
        ]
        
        if project_type in ['web_application', 'api']:
            base_security.extend([
                'JWT authentication',
                'Rate limiting',
                'CORS configuration',
                'HTTPS enforcement',
                'Password hashing (bcrypt)',
                'Session security'
            ])
        
        return base_security
    
    def _design_scalability(self, complexity: str) -> Dict[str, Any]:
        """Conçoit le plan de scalabilité"""
        
        scalability_plans = {
            'simple': {
                'approach': 'vertical_scaling',
                'database': 'single_instance',
                'caching': 'application_level',
                'cdn': 'optional'
            },
            'medium': {
                'approach': 'horizontal_scaling',
                'database': 'read_replicas',
                'caching': 'Redis',
                'cdn': 'recommended',
                'load_balancing': 'nginx'
            },
            'complex': {
                'approach': 'microservices',
                'database': 'sharding + clustering',
                'caching': 'distributed_cache',
                'cdn': 'required',
                'load_balancing': 'auto_scaling',
                'message_queue': 'Redis/RabbitMQ'
            }
        }
        
        return scalability_plans.get(complexity, scalability_plans['medium'])
    
    def _generate_file_structure(self, project_type: str) -> Dict[str, Any]:
        """Génère la structure de fichiers recommandée"""
        
        structures = {
            'web_application': {
                'root': [
                    'src/',
                    'tests/',
                    'docs/',
                    'docker/',
                    'requirements.txt',
                    'README.md',
                    'Dockerfile',
                    'docker-compose.yml',
                    '.env.example',
                    '.gitignore'
                ],
                'src': [
                    'app/',
                    'static/',
                    'templates/',
                    'config/',
                    'utils/'
                ],
                'app': [
                    'main.py',
                    'models/',
                    'routers/',
                    'services/',
                    'dependencies.py'
                ]
            },
            'api': {
                'root': [
                    'app/',
                    'tests/',
                    'docs/',
                    'requirements.txt',
                    'main.py',
                    'README.md',
                    'Dockerfile',
                    '.env.example',
                    '.gitignore'
                ],
                'app': [
                    'routers/',
                    'models/',
                    'services/',
                    'database.py',
                    'config.py'
                ]
            },
            'script': {
                'root': [
                    'src/',
                    'tests/',
                    'config/',
                    'main.py',
                    'requirements.txt',
                    'README.md',
                    '.gitignore'
                ],
                'src': [
                    'utils.py',
                    'config.py',
                    'main.py'
                ]
            }
        }
        
        return structures.get(project_type, structures['api'])
    
    def _list_dependencies(self, project_type: str) -> Dict[str, List[str]]:
        """Liste les dépendances nécessaires"""
        
        dependencies = {
            'web_application': {
                'core': ['fastapi', 'uvicorn', 'sqlalchemy', 'alembic'],
                'database': ['psycopg2-binary', 'redis'],
                'auth': ['python-jose', 'passlib', 'bcrypt'],
                'dev': ['pytest', 'black', 'flake8', 'pre-commit'],
                'frontend': ['react', 'axios', 'react-router-dom']
            },
            'api': {
                'core': ['fastapi', 'uvicorn', 'pydantic'],
                'database': ['sqlalchemy', 'psycopg2-binary'],
                'dev': ['pytest', 'black', 'flake8'],
                'docs': ['mkdocs', 'mkdocs-material']
            },
            'script': {
                'core': ['click', 'pydantic'],
                'utils': ['python-dotenv', 'pyyaml'],
                'dev': ['pytest', 'black']
            }
        }
        
        return dependencies.get(project_type, dependencies['api'])
    
    def _generate_config_files(self, project_type: str) -> Dict[str, str]:
        """Génère le contenu des fichiers de configuration"""
        
        configs = {}
        
        if project_type in ['web_application', 'api']:
            configs['docker-compose.yml'] = """version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:"""
            
            configs['.env.example'] = """# Database
DATABASE_URL=postgresql://user:password@localhost:5432/appdb

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Development
DEBUG=True
LOG_LEVEL=INFO"""
        
        return configs
    
    def _load_architecture_templates(self) -> Dict[str, Any]:
        """Charge les templates d'architecture"""
        return {
            'mvc': 'Model-View-Controller pattern',
            'layered': 'Layered architecture pattern',
            'microservices': 'Microservices architecture',
            'api_first': 'API-first design approach'
        }
    
    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """L'architecte peut gérer les tâches d'architecture"""
        return task.get('type') == 'architect'
    
    def estimate_task_cost(self, task: Dict[str, Any]) -> float:
        """L'architecture est gratuite avec Ollama"""
        return 0.0

# Instance de l'agent architecte
architect_agent = ArchitectAgent()
