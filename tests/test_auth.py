from http import HTTPStatus


def test_token_success(client, user, user_data):
    login_data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = client.post('/api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_token_invalid_credentials(client):
    login_data = {
        'email': 'wrong@example.com',
        'password': 'wrongpassword',
    }

    response = client.post('/api/v1/auth/token', json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'E-mail ou senha incorreto'


def test_refresh_token_success(client, user, headers):
    response = client.post('/api/v1/auth/refresh_token', headers=headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_refresh_token_invalid(client):
    response = client.post(
        '/api/v1/auth/refresh_token',
        headers={'Authorization': 'Bearer invalidtoken'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert (
        response.json()['detail'] == 'Não foi possível validar as credenciais'
    )
