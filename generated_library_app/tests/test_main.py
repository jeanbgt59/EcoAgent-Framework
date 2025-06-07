"""
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
