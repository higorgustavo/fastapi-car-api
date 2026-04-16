from fastapi import FastAPI, status

from car_api.routers import auth, brands, cars, users

app = FastAPI(
    title='Car API',
    description='API de carros',
    version='0.1.0',
)

app.include_router(
    router=auth.router,
    prefix='/api/v1/auth',
    tags=['Authentication'],
)

app.include_router(
    router=users.router,
    prefix='/api/v1/users',
    tags=['Users'],
)

app.include_router(
    router=brands.router,
    prefix='/api/v1/brands',
    tags=['Brands'],
)

app.include_router(
    router=cars.router,
    prefix='/api/v1/cars',
    tags=['Cars'],
)


@app.get('/health_check', status_code=status.HTTP_200_OK)
def read_root():
    return {'status': 'ok'}
