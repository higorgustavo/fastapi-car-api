from http import HTTPStatus


def test_create_brand(client, headers):
    response = client.post(
        '/api/v1/brands/',
        headers=headers,
        json={
            'name': 'Honda',
            'description': 'Honda Brand',
            'is_active': True,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Honda'


def test_create_brand_duplicate_name(client, headers, brand):
    response = client.post(
        '/api/v1/brands/',
        headers=headers,
        json={
            'name': brand.name,
            'description': 'Duplicate',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Nome da marca já está em uso'


def test_list_brands(client, headers, brand):
    response = client.get('/api/v1/brands/', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['brands']) > 0


def test_get_brand_by_id(client, headers, brand):
    response = client.get(f'/api/v1/brands/{brand.id}', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == brand.name


def test_update_brand(client, headers, brand):
    response = client.put(
        f'/api/v1/brands/{brand.id}',
        headers=headers,
        json={'name': 'Toyota Updated'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'Toyota Updated'


def test_delete_brand_success(client, headers, brand):
    # Brand with no cars
    response = client.delete(f'/api/v1/brands/{brand.id}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_brand_with_cars(client, headers, brand, car):
    # Brand with cars should fail
    response = client.delete(f'/api/v1/brands/{brand.id}', headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.json()['detail']
        == 'Não é possível deletar marca que possui carros associados'
    )
