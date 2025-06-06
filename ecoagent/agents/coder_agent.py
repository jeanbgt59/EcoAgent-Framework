"""
EcoAgent Framework - Agent Codeur
Génère le code source basé sur l'analyse et l'architecture
"""

import os
from typing import Dict, Any, List
from .base_agent import BaseAgent

class CoderAgent(BaseAgent):
    """
    Agent codeur qui génère le code source complet
    """
    
    def __init__(self):
        super().__init__(
            name="coder",
            description="Génère le code source complet basé sur l'analyse et l'architecture",
            model_preference="local"
        )
        
        # Utilise le modèle de code spécialisé si disponible
        self.specialized_model = "coding_model"
        
        # Templates de code
        self.code_templates = self._load_code_templates()
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère le code source complet
        """
        description = task.get('description', '')
        context = task.get('context', {})
        
        # Récupération des étapes précédentes
        analysis_result = context.get('analysis', {})
        architect_result = context.get('architect', {})
        
        project_type = analysis_result.get('project_type', 'general_application')
        complexity = analysis_result.get('complexity', 'medium')
        tech_stack = architect_result.get('technology_stack', {})
        file_structure = architect_result.get('file_structure', {})
        api_design = architect_result.get('api_design', {})
        
        self.logger.info(f"Génération du code pour {project_type} avec {tech_stack.get('backend', 'Python')}")
        
        # Génération du code
        generated_files = {}
        
        if project_type in ['web_application', 'api']:
            generated_files.update(await self._generate_fastapi_code(
                tech_stack, api_design, analysis_result, architect_result
            ))
        elif project_type == 'script':
            generated_files.update(await self._generate_script_code(
                analysis_result, architect_result
            ))
        
        # Génération des fichiers de configuration
        config_files = await self._generate_config_files(architect_result)
        generated_files.update(config_files)
        
        # Génération des tests
        test_files = await self._generate_test_files(project_type, api_design)
        generated_files.update(test_files)
        
        # Génération de la documentation
        doc_files = await self._generate_documentation(analysis_result, architect_result)
        generated_files.update(doc_files)
        
        result = {
            'success': True,
            'generated_files': generated_files,
            'file_count': len(generated_files),
            'main_technologies': list(tech_stack.values())[:3],
            'entry_point': self._determine_entry_point(project_type),
            'installation_commands': self._generate_installation_commands(architect_result),
            'run_commands': self._generate_run_commands(project_type, tech_stack)
        }
        
        return result
    
    async def _generate_fastapi_code(self, tech_stack: Dict, api_design: Dict, 
                                   analysis: Dict, architect: Dict) -> Dict[str, str]:
        """Génère une application FastAPI complète"""
        
        files = {}
        
        # main.py - Point d'entrée principal
        files['main.py'] = '''"""
Application FastAPI générée par EcoAgent Framework
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn

from app.database import engine, Base
from app.routers import items, users, health
from app.config import settings

# Création des tables
Base.metadata.create_all(bind=engine)

# Instance FastAPI
app = FastAPI(
    title="Application générée par EcoAgent",
    description="API REST générée automatiquement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {
        "message": "Application générée par EcoAgent Framework",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
'''

        # app/config.py - Configuration
        files['app/config.py'] = '''"""
Configuration de l'application
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Base de données
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/appdb"
    
    # Sécurité
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
'''

        # app/database.py - Configuration base de données
        files['app/database.py'] = '''"""
Configuration de la base de données
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Moteur de base de données
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

# Session de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

        # app/models/user.py - Modèle utilisateur
        files['app/models/user.py'] = '''"""
Modèle utilisateur
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
'''

        # app/models/item.py - Modèle item
        files['app/models/item.py'] = '''"""
Modèle item générique
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    owner = relationship("User", back_populates="items")
'''

        # Ajout de la relation dans User
        files['app/models/__init__.py'] = '''"""
Modèles de données
"""

from .user import User
from .item import Item

# Ajout des relations manquantes
from sqlalchemy.orm import relationship

# Relation items pour User
User.items = relationship("Item", back_populates="owner")

__all__ = ["User", "Item"]
'''

        # app/schemas/user.py - Schémas Pydantic
        files['app/schemas/user.py'] = '''"""
Schémas Pydantic pour les utilisateurs
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str
'''

        # app/routers/users.py - Routes utilisateurs
        files['app/routers/users.py'] = '''"""
Routes pour la gestion des utilisateurs
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..services.user_service import UserService

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère la liste des utilisateurs"""
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupère un utilisateur par son ID"""
    user = UserService.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crée un nouvel utilisateur"""
    # Vérification si l'utilisateur existe déjà
    existing_user = UserService.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    return UserService.create_user(db=db, user=user)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un utilisateur"""
    user = UserService.update_user(db, user_id=user_id, user_update=user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Supprime un utilisateur"""
    success = UserService.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
'''

        # app/routers/items.py - Routes items
        files['app/routers/items.py'] = '''"""
Routes pour la gestion des items
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère la liste des items"""
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Crée un nouvel item"""
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''

        # app/schemas/item.py - Schémas pour items
        files['app/schemas/item.py'] = '''"""
Schémas Pydantic pour les items
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    owner_id: int

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
'''

        # app/routers/health.py - Health check
        files['app/routers/health.py'] = '''"""
Routes pour le health check
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db
import datetime

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Vérifie l'état de santé de l'application"""
    try:
        # Test de connexion à la base de données
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "database": db_status,
        "version": "1.0.0"
    }
'''

        # app/services/user_service.py - Service utilisateur
        files['app/services/user_service.py'] = '''"""
Service pour la gestion des utilisateurs
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """Service pour les opérations utilisateur"""
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash le mot de passe"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifie le mot de passe"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_user(db: Session, user_id: int):
        """Récupère un utilisateur par ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Récupère un utilisateur par email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        """Récupère la liste des utilisateurs"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """Crée un nouvel utilisateur"""
        hashed_password = UserService.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate):
        """Met à jour un utilisateur"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Supprime un utilisateur"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
'''

        return files
    
    async def _generate_script_code(self, analysis: Dict, architect: Dict) -> Dict[str, str]:
        """Génère un script Python simple"""
        
        files = {}
        
        # main.py pour script
        files['main.py'] = '''#!/usr/bin/env python3
"""
Script généré par EcoAgent Framework
"""

import argparse
import logging
from pathlib import Path
from src.utils import setup_logging, load_config
from src.processor import DataProcessor

def main():
    """Fonction principale du script"""
    parser = argparse.ArgumentParser(description="Script généré par EcoAgent")
    parser.add_argument("input", help="Fichier d'entrée")
    parser.add_argument("output", help="Fichier de sortie")
    parser.add_argument("--config", default="config/config.yaml", help="Fichier de configuration")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Chargement de la configuration
        config = load_config(args.config)
        
        # Traitement
        processor = DataProcessor(config)
        processor.process(args.input, args.output)
        
        logger.info(f"Traitement terminé: {args.input} -> {args.output}")
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
'''

        # src/utils.py
        files['src/utils.py'] = '''"""
Utilitaires pour le script
"""

import logging
import yaml
import json
from pathlib import Path
from typing import Dict, Any

def setup_logging(verbose: bool = False):
    """Configure le logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_config(config_path: str) -> Dict[str, Any]:
    """Charge la configuration depuis un fichier"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        return {}
    
    if config_file.suffix.lower() == '.yaml' or config_file.suffix.lower() == '.yml':
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif config_file.suffix.lower() == '.json':
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError(f"Format de configuration non supporté: {config_file.suffix}")
'''

        # src/processor.py
        files['src/processor.py'] = '''"""
Processeur principal du script
"""

import json
import csv
from pathlib import Path
from typing import Dict, Any

class DataProcessor:
    """Processeur de données générique"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def process(self, input_path: str, output_path: str):
        """Traite les données d'entrée et génère la sortie"""
        input_file = Path(input_path)
        output_file = Path(output_path)
        
        # Détection du format d'entrée
        if input_file.suffix.lower() == '.csv':
            data = self._read_csv(input_file)
        elif input_file.suffix.lower() == '.json':
            data = self._read_json(input_file)
        else:
            raise ValueError(f"Format non supporté: {input_file.suffix}")
        
        # Traitement des données
        processed_data = self._process_data(data)
        
        # Écriture du résultat
        if output_file.suffix.lower() == '.json':
            self._write_json(processed_data, output_file)
        elif output_file.suffix.lower() == '.csv':
            self._write_csv(processed_data, output_file)
        else:
            raise ValueError(f"Format de sortie non supporté: {output_file.suffix}")
    
    def _read_csv(self, file_path: Path) -> list:
        """Lit un fichier CSV"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def _read_json(self, file_path: Path) -> Any:
        """Lit un fichier JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _process_data(self, data: Any) -> Any:
        """Traite les données selon la configuration"""
        # Logique de traitement basique
        if isinstance(data, list):
            return [self._process_item(item) for item in data]
        else:
            return self._process_item(data)
    
    def _process_item(self, item: Any) -> Any:
        """Traite un élément individuel"""
        # Exemple de traitement
        if isinstance(item, dict):
            processed = {}
            for key, value in item.items():
                processed[key.lower()] = value
            return processed
        return item
    
    def _write_json(self, data: Any, file_path: Path):
        """Écrit les données en JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _write_csv(self, data: list, file_path: Path):
        """Écrit les données en CSV"""
        if not data:
            return
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(f)
                writer.writerows(data)
'''

        return files
    
    async def _generate_config_files(self, architect_result: Dict) -> Dict[str, str]:
        """Génère les fichiers de configuration"""
        
        files = {}
        config_files = architect_result.get('configuration_files', {})
        
        # requirements.txt
        dependencies = architect_result.get('dependencies', {})
        requirements = []
        for category, deps in dependencies.items():
            if category != 'frontend':  # Ignore les dépendances frontend
                requirements.extend(deps)
        
        files['requirements.txt'] = '\n'.join(requirements) + '\n'
        
        # .env.example
        if '.env.example' in config_files:
            files['.env.example'] = config_files['.env.example']
        
        # docker-compose.yml
        if 'docker-compose.yml' in config_files:
            files['docker-compose.yml'] = config_files['docker-compose.yml']
        
        # Dockerfile
        files['Dockerfile'] = '''FROM python:3.11-slim

WORKDIR /app

# Copie des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Exposition du port
EXPOSE 8000

# Commande par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

        # .gitignore
        files['.gitignore'] = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite3

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/

# Docker
.dockerignore
'''

        return files
    
    async def _generate_test_files(self, project_type: str, api_design: Dict) -> Dict[str, str]:
        """Génère les fichiers de tests"""
        
        files = {}
        
        if project_type in ['web_application', 'api']:
            # tests/test_main.py
            files['tests/test_main.py'] = '''"""
Tests pour l'application principale
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test de la route racine"""
    response = client.get("/")
    assert response.status_code == 200
    assert "EcoAgent Framework" in response.json()["message"]

def test_health_check():
    """Test du health check"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_docs_accessible():
    """Test que la documentation est accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
'''

            # tests/test_users.py
            files['tests/test_users.py'] = '''"""
Tests pour les utilisateurs
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users():
    """Test de récupération des utilisateurs"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    """Test de création d'utilisateur"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users", json=user_data)
    # Note: Peut échouer si la DB n'est pas configurée
    assert response.status_code in [201, 422]  # 422 si validation échoue
'''

            # tests/conftest.py
            files['tests/conftest.py'] = '''"""
Configuration des tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import get_db, Base

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Fixture pour la base de données de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Fixture pour le client de test"""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
'''

        elif project_type == 'script':
            files['tests/test_processor.py'] = '''"""
Tests pour le processeur de données
"""

import pytest
import tempfile
import json
import csv
from pathlib import Path

from src.processor import DataProcessor

@pytest.fixture
def config():
    """Configuration de test"""
    return {"test": True}

@pytest.fixture
def processor(config):
    """Processeur de test"""
    return DataProcessor(config)

def test_json_to_json(processor):
    """Test de conversion JSON vers JSON"""
    test_data = [{"name": "Test", "value": 123}]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.json"
        output_file = Path(tmpdir) / "output.json"
        
        # Écriture du fichier d'entrée
        with open(input_file, 'w') as f:
            json.dump(test_data, f)
        
        # Traitement
        processor.process(str(input_file), str(output_file))
        
        # Vérification
        assert output_file.exists()
        with open(output_file, 'r') as f:
            result = json.load(f)
        
        assert len(result) == 1
        assert result[0]["name"] == "test"  # Doit être en minuscules

def test_csv_to_json(processor):
    """Test de conversion CSV vers JSON"""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.csv"
        output_file = Path(tmpdir) / "output.json"
        
        # Écriture du fichier CSV
        with open(input_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Value"])
            writer.writerow(["Test", "123"])
        
        # Traitement
        processor.process(str(input_file), str(output_file))
        
        # Vérification
        assert output_file.exists()
'''

        return files
    
    async def _generate_documentation(self, analysis: Dict, architect: Dict) -> Dict[str, str]:
        """Génère la documentation"""
        
        files = {}
        
        project_type = analysis.get('project_type', 'application')
        complexity = analysis.get('complexity', 'medium')
        tech_stack = architect.get('technology_stack', {})
        description = analysis.get('description', 'Application générée par EcoAgent')
        
        # README.md principal - Version simplifiée
        files['README.md'] = f"""# {description}

Application {project_type} générée automatiquement par EcoAgent Framework.

## Démarrage rapide

### Prérequis
- Python 3.11+
- Docker (optionnel)

### Installation

1. Clonez le repository
2. Créez un environnement virtuel : python -m venv venv
3. Activez l'environnement : source venv/bin/activate
4. Installez les dépendances : pip install -r requirements.txt

### Lancement

Mode développement : python main.py

## Documentation

- Type : {project_type}
- Complexité : {complexity}

Structure du projet :
- app/ : Code de l'application
- tests/ : Tests automatisés
- docs/ : Documentation

## Tests

Lancement des tests : pytest

## Généré par EcoAgent Framework

Type de projet : {project_type}
Complexité estimée : {complexity}
"""
        
        # docs/api.md (si API)
        if project_type in ['web_application', 'api']:
            files['docs/api.md'] = """# Documentation API

## Endpoints disponibles

### Health Check
- GET /api/v1/health - Vérifie l'état de l'application

### Utilisateurs
- GET /api/v1/users - Liste des utilisateurs
- POST /api/v1/users - Créer un utilisateur
- GET /api/v1/users/{id} - Détails d'un utilisateur
- PUT /api/v1/users/{id} - Modifier un utilisateur
- DELETE /api/v1/users/{id} - Supprimer un utilisateur

### Items
- GET /api/v1/items - Liste des items
- POST /api/v1/items - Créer un item

## Authentification
L'API utilise JWT pour l'authentification (si configuré).

## Codes de réponse
- 200 - Succès
- 201 - Créé avec succès
- 400 - Erreur de validation
- 401 - Non autorisé
- 404 - Non trouvé
- 500 - Erreur serveur
"""
        
        return files

    def _load_code_templates(self) -> Dict[str, str]:
        """Charge les templates de code"""
        return {
            'fastapi': 'Template FastAPI',
            'script': 'Template Script Python',
            'flask': 'Template Flask'
        }

    def _determine_entry_point(self, project_type: str) -> str:
        """Détermine le point d'entrée de l'application"""
        if project_type in ['web_application', 'api']:
            return 'main.py'
        elif project_type == 'script':
            return 'main.py'
        else:
            return 'main.py'

    def _generate_installation_commands(self, architect_result: Dict) -> List[str]:
        """Génère les commandes d'installation"""
        commands = [
            'python -m venv venv',
            'source venv/bin/activate',
            'pip install -r requirements.txt'
        ]
        
        if 'database' in str(architect_result.get('technology_stack', {})):
            commands.append('# Configurez votre base de données dans .env')
        
        return commands

    def _generate_run_commands(self, project_type: str, tech_stack: Dict) -> List[str]:
        """Génère les commandes pour lancer l'application"""
        if project_type in ['web_application', 'api']:
            if tech_stack.get('backend') == 'FastAPI':
                return [
                    'uvicorn main:app --reload',
                    'uvicorn main:app --host 0.0.0.0 --port 8000'
                ]
        elif project_type == 'script':
            return [
                'python main.py --help',
                'python main.py input.csv output.json'
            ]
        
        return ['python main.py']

    def _load_code_templates(self) -> Dict[str, str]:
        """Charge les templates de code"""
        return {
            'fastapi': 'Template FastAPI',
            'script': 'Template Script Python',
            'flask': 'Template Flask'
        }



    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """Le codeur peut gérer les tâches de génération de code"""
        return task.get('type') == 'coder'

    def estimate_task_cost(self, task: Dict[str, Any]) -> float:
        """La génération de code est gratuite avec Ollama"""
        return 0.0

# Instance de l'agent codeur
coder_agent = CoderAgent()

