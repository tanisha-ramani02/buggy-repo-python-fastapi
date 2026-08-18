"""FastAPI Application Main Entrypoint."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.api.routes import items, search, orders, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on application startup."""
    init_db()
    yield


app = FastAPI(
    title="Inventory & Orders API (Testbed)",
    description="A Python FastAPI + SQLite testbed application for Autonomous Bug Fixer Agent evaluation.",
    version="1.0.0",
    lifespan=lifespan
)

# Register routers
app.include_router(items.router)
app.include_router(search.router)
app.include_router(orders.router)
app.include_router(reports.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "inventory-api"}
