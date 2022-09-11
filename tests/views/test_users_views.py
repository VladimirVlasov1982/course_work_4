import pytest

from project.models import User
from project.tools import generate_password_hash


class TestUsersView:

    @pytest.fixture
    def passwords(self):
        passwords = {"old_password": "password_new", "new_password": "password_update"}
        return passwords

    def test_auth_required(self, client):
        response = client.get('/user')
        assert response.status_code == 401

    def test_get_user(self, client, token, user):
        response = client.get('/user', headers={'Authorization': f"Bearer {token}"})
        assert response.status_code == 200
        assert type(response.json) == dict

    def test_patch_user(self, client, token):
        response = client.patch('/user', headers={'Authorization': f"Bearer {token}"})
        assert response.status_code == 204

    def test_update_password_user(self, client, token, passwords, user):
        response = client.put('/user/password', headers={'Authorization': f"Bearer {token}"}, json=passwords)
        assert response.status_code == 204
