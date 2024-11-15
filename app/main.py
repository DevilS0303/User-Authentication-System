import logging
from fastapi import FastAPI
from app.endpoints import auth, user

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to the console
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Middleware to log requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users")
