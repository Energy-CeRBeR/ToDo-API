import uvicorn

from fastapi import FastAPI

from src.users.user_routers import router as users_router
# from src.users.admin_routers import router as admin_router
from src.categories.routers import router as categories_router
from src.tasks.routers import router as tasks_router

app = FastAPI(
    title="ToDo-API"
)

app.include_router(users_router)
# app.include_router(admin_router)
app.include_router(categories_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )
