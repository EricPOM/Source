from fastapi import FastAPI
from routers import platform, business_unit, api_key, routing, logging # Import the new logging router

app = FastAPI(
    title="AI/BU API Key Management Service",
    description="Manages AI Platforms, Business Units, and their API Keys.",
    version="0.1.0"
)

# Include routers
app.include_router(platform.router, prefix="/api/v1", tags=["AI Platforms"])
app.include_router(business_unit.router, prefix="/api/v1", tags=["Business Units"])
app.include_router(api_key.router, prefix="/api/v1", tags=["API Keys"])
app.include_router(routing.router, prefix="/api/v1", tags=["Key Routing"])
app.include_router(logging.router, prefix="/api/v1", tags=["Logging"]) # Include the new logging router

@app.get("/")
async def root():
    return {"message": "Welcome to the API Key Management Service. See /docs for API documentation."}

# In a real application, you would also configure database connections,
# logging, middleware for authentication, etc. here.

# Example: Placeholder for database initialization
# from sqlalchemy import create_engine
# from models.platform import Base as PlatformBase
# from models.business_unit import Base as BUBase
# from models.api_key import Base as APIKeyBase

# DATABASE_URL = "sqlite:///./test.db" # Replace with your actual DB URL
# engine = create_engine(DATABASE_URL)

# This is a simplified way to ensure tables are created.
# In a production app, you'd use Alembic for migrations.
# def create_db_and_tables():
#     PlatformBase.metadata.create_all(bind=engine)
#     BUBase.metadata.create_all(bind=engine)
#     APIKeyBase.metadata.create_all(bind=engine)

# @app.on_event("startup")
# async def on_startup():
#     print("Application startup...")
#     # create_db_and_tables() # Uncomment if you have a DB engine configured
#     print("Database tables (simulated) creation attempted.")

# @app.on_event("shutdown")
# async def on_shutdown():
#     print("Application shutdown...")

# --- Permission Control Implementation Note ---
# The API routers (e.g., in routers/platform.py, routers/api_key.py, etc.) use
# placeholder `Depends(...)` functions for authentication and authorization (e.g.,
# `verify_sdk_request`, `verify_admin_access`). These are crucial for security
# and must be fully implemented. This would typically involve:
#   - Integrating an authentication system (e.g., OAuth2, JWT tokens).
#   - Defining roles and permissions (e.g., 'admin', 'business_unit_manager', 'sdk_user').
#   - Verifying tokens and checking user roles/permissions in these dependency functions
#     to ensure that only authorized users/services can access specific endpoints
#     or perform certain operations.
# For instance, creating/deleting API keys should be restricted to authenticated users
# with appropriate administrative privileges for the target business unit or platform.
# Log viewing might be restricted based on user's business unit affiliation.
# The `select-key` endpoint's SDK authentication needs to be robust.
# --- End Permission Control Implementation Note ---

if __name__ == "__main__":
    import uvicorn
    # This is for development only. For production, use a Gunicorn or similar ASGI server.
    uvicorn.run(app, host="0.0.0.0", port=8000)
