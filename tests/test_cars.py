from http import HTTPStatus

from car_api.models.cars import FuelType, TransmissionType


def test_create_car(client, headers, brand):
    response = client.post(
        '/api/v1/cars/',
        headers=headers,
        json={
            'model': 'Civic',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Black',
            'plate': 'KLI9876',
            'fuel_type': FuelType.FLEX,
            'transmission': TransmissionType.AUTOMATIC,
            'price': 150000.00,
            'brand_id': brand.id,
            'description': 'New Civic',
            'is_available': True,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['model'] == 'Civic'


def test_create_car_duplicate_plate(client, headers, brand, car):
    response = client.post(
        '/api/v1/cars/',
        headers=headers,
        json={
            'model': 'Another',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Black',
            'plate': car.plate,
            'fuel_type': FuelType.FLEX,
            'transmission': TransmissionType.AUTOMATIC,
            'price': 150000.00,
            'brand_id': brand.id,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Placa já está em uso'


def test_list_cars(client, headers, car):
    response = client.get('/api/v1/cars/', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['cars']) > 0


def test_get_car_by_id(client, headers, car):
    response = client.get(f'/api/v1/cars/{car.id}', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['model'] == car.model


def test_update_car(client, headers, car):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=headers,
        json={'model': 'Corolla Updated'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['model'] == 'Corolla Updated'


def test_delete_car(client, headers, car):
    response = client.delete(f'/api/v1/cars/{car.id}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Verify it's gone
    response = client.get(f'/api/v1/cars/{car.id}', headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_transfer_car(client, headers, car):
    # Create another user to transfer to
    resp_user = client.post(
        '/api/v1/users/',
        json={
            'username': 'receiver',
            'email': 'receiver@example.com',
            'password': 'password',
        },
    )
    new_user_id = resp_user.json()['id']

    response = client.post(
        f'/api/v1/cars/{car.id}/transfer',
        headers=headers,
        json={'new_owner_id': new_user_id},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['owner']['id'] == new_user_id
