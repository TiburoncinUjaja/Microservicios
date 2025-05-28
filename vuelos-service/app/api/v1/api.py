from fastapi import APIRouter
from app.api.v1.endpoints import vuelos, tripulacion

api_router = APIRouter()
 
api_router.include_router(vuelos.router, prefix="/vuelos", tags=["vuelos"])
api_router.include_router(tripulacion.router, prefix="/tripulacion", tags=["tripulacion"]) 