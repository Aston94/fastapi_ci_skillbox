from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables, drop_tables
from router import router as recipe_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print('База очищена')
    await create_tables()
    print('База создана и готова к работе')
    yield
    print('Выключение')


app = FastAPI(lifespan=lifespan)
app.include_router(recipe_router)

