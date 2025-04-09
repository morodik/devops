from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    """Получение существующего пользователя"""
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    """Получение несуществующего пользователя"""
    response = client.get("/api/v1/user", params={'email': "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    """Создание пользователя с уникальной почтой"""
    new_user = {
        'name': 'New User',
        'email': 'new.user@mail.com'
    }
    
    # Сначала проверяем, что пользователя нет
    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 404
    
    # Создаем пользователя
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    
    # Проверяем, что пользователь создан
    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 200
    assert response.json()['name'] == new_user['name']
    assert response.json()['email'] == new_user['email']

def test_create_user_with_invalid_email():
    """Создание пользователя с почтой, которую использует другой пользователь"""
    existing_email = users[0]['email']
    new_user = {
        'name': 'Duplicate User',
        'email': existing_email
    }
    
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_delete_user():
    """Удаление пользователя"""
    # Сначала создаем тестового пользователя для удаления
    test_user = {
        'name': 'User to delete',
        'email': 'to.delete@mail.com'
    }
    client.post("/api/v1/user", json=test_user)
    
    # Удаляем пользователя
    response = client.delete("/api/v1/user", params={'email': test_user['email']})
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    
    # Проверяем, что пользователь действительно удален
    response = client.get("/api/v1/user", params={'email': test_user['email']})
    assert response.status_code == 404