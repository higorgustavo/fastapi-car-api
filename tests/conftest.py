import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.app import app
from car_api.core.database import get_session
from car_api.core.security import create_access_token, get_password_hash
from car_api.models import Base
from car_api.models.cars import Brand, Car, FuelType, TransmissionType
from car_api.models.users import User


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    await engine.dispose()


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'secret123',
    }


@pytest_asyncio.fixture
async def user(session, user_data):
    hashed_password = get_password_hash(user_data['password'])
    db_user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest.fixture
def token(user):
    return create_access_token({'sub': str(user.id)})


@pytest.fixture
def headers(token):
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def brand(session):
    brand = Brand(name='Toyota', description='Toyota Brand')
    session.add(brand)
    await session.commit()
    await session.refresh(brand)
    return brand


@pytest_asyncio.fixture
async def car(session, user, brand):
    car = Car(
        model='Corolla',
        factory_year=2020,
        model_year=2021,
        color='Silver',
        plate='ABC1234',
        fuel_type=FuelType.FLEX,
        transmission=TransmissionType.AUTOMATIC,
        price=100000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car)
    await session.commit()
    await session.refresh(car)
    return car
