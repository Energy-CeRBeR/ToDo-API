import uvicorn

from fastapi import FastAPI

from src.users.routers import router as users_router
from src.categories.routers import router as categories_router
from src.tasks.routers import router as tasks_router
from src.admin.routers import router as admin_router

app = FastAPI(
    title="ToDo-API"
)

app.include_router(users_router)
app.include_router(categories_router)
app.include_router(tasks_router)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )
