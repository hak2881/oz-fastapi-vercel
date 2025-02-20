from fastapi import FastAPI

from route.task import task_router
from route.user import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)

responses = {
    "en": {"message": "Hello, welcome!"},
    "ko": {"message": "안녕하세요, 환영합니다!"},
    "fr": {"message": "Bonjour, bienvenue!"},
    "de": {"message": "Hallo, willkommen!"},
    "es": {"message": "iHola, bienvenido!"}
}