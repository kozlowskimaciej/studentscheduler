"""The main APIRouter is defined to include all the sub routers from each
module inside the API folder"""
from fastapi import APIRouter
from .base import base_router
from .courses import courses_router

api_router = APIRouter()
api_router.include_router(base_router)
api_router.include_router(courses_router)
