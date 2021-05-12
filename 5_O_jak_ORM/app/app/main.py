from fastapi import FastAPI

from .views import router as northwind_api_router

app = FastAPI()

app.include_router(northwind_api_router, tags=["northwind"])
