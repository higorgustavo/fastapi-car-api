from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.models.cars import Brand
from car_api.schemas.brands import BrandPublicSchema, BrandSchema

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=BrandPublicSchema,
    summary='Criar nova marca',
)
async def create_brand(
    brand: BrandSchema, db: AsyncSession = Depends(get_session)
):
    name_exists = await db.scalar(
        select(exists().where(Brand.name == brand.name))
    )

    if name_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Nome da marca já está em uso',
        )

    db_brand = Brand(
        name=brand.name,
        description=brand.description,
        is_active=brand.is_active,
    )

    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)

    return db_brand
