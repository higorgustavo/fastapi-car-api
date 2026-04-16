import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from car_api.models.cars import Brand, Car, FuelType, TransmissionType
from car_api.models.users import User


@pytest.mark.asyncio
async def test_db_connection(session):
    """Test if we can connect to the database and run a simple query."""
    result = await session.execute(select(1))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_user_creation(session):
    """Test user creation and persistence."""
    new_user = User(
        username='testdb', email='testdb@example.com', password='password123'
    )
    session.add(new_user)
    await session.commit()

    result = await session.execute(
        select(User).where(User.username == 'testdb')
    )
    db_user = result.scalar_one()
    assert db_user.email == 'testdb@example.com'


@pytest.mark.asyncio
async def test_unique_email_constraint(session, user):
    """Test that duplicate emails are not allowed."""
    duplicate_user = User(
        username='other', email=user.email, password='password'
    )
    session.add(duplicate_user)
    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_brand_car_relationship(session, user, brand):
    """Test relationship between Brand and Car."""
    car = Car(
        model='Yaris',
        factory_year=2022,
        model_year=2023,
        color='White',
        plate='XYZ9876',
        fuel_type=FuelType.FLEX,
        transmission=TransmissionType.AUTOMATIC,
        price=90000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car)
    await session.commit()

    result = await session.execute(
        select(Brand)
        .options(selectinload(Brand.cars))
        .where(Brand.id == brand.id)
    )
    db_brand = result.scalar_one()
    assert len(db_brand.cars) > 0
    assert db_brand.cars[0].model == 'Yaris'
