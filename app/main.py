from fastapi import FastAPI
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from app.routes.creators import router as creator_router

from app.models.creator import Creator
from app.models.lead import Lead
from app.models.product import Product
from app.models.order import Order


#Register
from app.routes.leads import router as lead_router
from app.routes.products import router as product_router
from app.routes.orders import router as order_router
from app.routes.auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for now (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if not exist
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(creator_router)
app.include_router(lead_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "API running"}