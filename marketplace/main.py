from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, products, seller, orders

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_tables()

origins = [
    "http://localhost:5173",
    "https://test-marketplace-frontend.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(seller.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API"}