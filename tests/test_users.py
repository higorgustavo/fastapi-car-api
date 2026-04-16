from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == 'newuser'
    assert 'id' in response.json()


def test_create_user_duplicate_username(client, user):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': user.username,
            'email': 'different@example.com',
            'password': 'password123',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username já está em uso'


def test_list_users(client, user):
    response = client.get('/api/v1/users/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['users']) > 0


def test_get_user_by_id(client, user):
    response = client.get(f'/api/v1/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user.username


def test_get_user_not_found(client):
    response = client.get('/api/v1/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user, headers):
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers=headers,
        json={'username': 'updatedname'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'updatedname'


def test_delete_user(client, user, headers):
    response = client.delete(f'/api/v1/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Verify it's gone
    response = client.get(f'/api/v1/users/{user.id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
