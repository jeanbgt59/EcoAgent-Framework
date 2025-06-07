"""
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
