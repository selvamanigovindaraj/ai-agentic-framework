"""Agent Builder Backend API (Modular)"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

# Routers
from agentic_framework.server.routers import components, agents

app = FastAPI(title="Agent Builder API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(components.router)
app.include_router(agents.router)

if __name__ == "__main__":
    uvicorn.run("agentic_framework.server.main:app", host="0.0.0.0", port=8000, reload=True)
