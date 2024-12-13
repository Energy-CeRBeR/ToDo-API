import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.users.user_routers import router as users_router
from src.users.admin_routers import router as admin_router
from src.categories.routers import router as categories_router
from src.tasks.routers import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.system("alembic upgrade head")

    yield


app = FastAPI(
    title="ToDo-API",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping_pong():
    return "pong"


app.include_router(users_router)
app.include_router(admin_router)
app.include_router(categories_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0"
    )
