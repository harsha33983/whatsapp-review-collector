from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import whatsapp, reviews

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WhatsApp Review Collector")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(whatsapp.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {"message": "WhatsApp Review Collector API is running"}
