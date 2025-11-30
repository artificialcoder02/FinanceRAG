from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from core.pipeline import pipeline
from core.auth import get_current_user, get_current_admin_user, auth_service, get_current_user_optional
from core.database_auth import db_auth_service
from core.config import config
from datetime import timedelta
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FinanceRAG API", description="API for FinanceRAG Multi-Agent System with Authentication")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list
    evaluation: dict

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    total_queries: int

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Initialize first admin user on startup
@app.on_event("startup")
async def create_admin_user():
    """Create the first admin user if no users exist"""
    try:
        user_count = db_auth_service.get_user_count()
        if user_count == 0:
            logger.info("No users found. Creating admin user...")

            raw_password = config.ADMIN_PASSWORD

            if not raw_password:
                raise ValueError("ADMIN_PASSWORD is not set in environment")

            # Enforce bcrypt 72-byte limit
            pwd_bytes = raw_password.encode("utf-8")
            if len(pwd_bytes) > 72:
                logger.warning(
                    f"ADMIN_PASSWORD is {len(pwd_bytes)} bytes; truncating to 72 bytes for bcrypt."
                )
                pwd_bytes = pwd_bytes[:72]
                # Decode back to string for your get_password_hash(password: str)
                raw_password = pwd_bytes.decode("utf-8", errors="ignore")

            logger.info(f"Admin password length (chars): {len(raw_password)}")
            logger.info(f"Admin password length (bytes): {len(raw_password.encode('utf-8'))}")

            hashed_password = auth_service.get_password_hash(raw_password)

            admin_user = db_auth_service.create_user(
                email=config.ADMIN_EMAIL,
                username=config.ADMIN_USERNAME,
                hashed_password=hashed_password,
                full_name=config.ADMIN_FULL_NAME,
                role="admin",
            )

            if admin_user:
                db_auth_service.verify_user_email(config.ADMIN_EMAIL)
                logger.info(f"✅ Admin user created: {config.ADMIN_EMAIL}")
                # ⚠️ Don't log the password in real environments
                # logger.info(f"🔑 Password: {raw_password}")
            else:
                logger.error("Failed to create admin user")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")


# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserRegister):
    """Register a new user"""
    # Validate password strength
    is_strong, message = auth_service.validate_password_strength(user.password)
    if not is_strong:
        raise HTTPException(status_code=400, detail=message)
    
    # Check if user already exists
    existing_user = db_auth_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = db_auth_service.get_user_by_username(user.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password and create user
    hashed_password = auth_service.get_password_hash(user.password)
    new_user = db_auth_service.create_user(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role="user"  # Default role
    )
    
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    logger.info(f"New user registered: {user.email}")
    
    return UserResponse(
        id=new_user["_id"],
        email=new_user["email"],
        username=new_user["username"],
        full_name=new_user["full_name"],
        role=new_user["role"],
        is_active=new_user["is_active"],
        is_verified=new_user["is_verified"],
        total_queries=new_user["total_queries"]
    )

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active"):
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    # Update last login
    db_auth_service.update_last_login(user["email"])
    
    # Create access token
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user['email']}")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user["_id"],
            email=user["email"],
            username=user["username"],
            full_name=user["full_name"],
            role=user["role"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
            total_queries=user["total_queries"]
        )
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user["_id"],
        email=current_user["email"],
        username=current_user["username"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        is_active=current_user["is_active"],
        is_verified=current_user.get("is_verified", False),
        total_queries=current_user.get("total_queries", 0)
    )

@app.post("/auth/verify-email/{email}")
async def verify_email(email: str, current_user: dict = Depends(get_current_admin_user)):
    """Verify a user's email (admin only)"""
    db_auth_service.verify_user_email(email)
    return {"message": f"Email verified for {email}"}

# Admin endpoints
@app.get("/auth/users")
async def list_users(current_user: dict = Depends(get_current_admin_user)):
    """List all users (admin only)"""
    users = db_auth_service.get_all_users()
    return {"users": users}

@app.delete("/auth/users/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Delete a user (admin only)"""
    success = db_auth_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.put("/auth/users/{user_id}/role")
async def update_user_role(user_id: str, role: str, current_user: dict = Depends(get_current_admin_user)):
    """Update user role (admin only)"""
    if role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    success = db_auth_service.update_user_role(user_id, role)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User role updated to {role}"}

@app.get("/auth/stats")
async def get_stats(current_user: dict = Depends(get_current_admin_user)):
    """Get system statistics (admin only)"""
    stats = db_auth_service.get_query_stats()
    return stats

# Main application endpoints
@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    """Ask a question (requires authentication)"""
    logger.info(f"Received query from {current_user['email']}: {request.query}")
    
    start_time = time.time()
    
    try:
        result = pipeline.run(request.query)
        
        response_time = time.time() - start_time
        
        # Save query to history
        db_auth_service.save_query(
            user_id=current_user["_id"],
            query=request.query,
            answer=result["answer"],
            sources=result["sources"],
            evaluation=result["evaluation"],
            response_time=response_time
        )
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            evaluation=result["evaluation"]
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(limit: int = 50, current_user: dict = Depends(get_current_user)):
    """Get user's query history"""
    queries = db_auth_service.get_user_queries(current_user["_id"], limit)
    return {"queries": queries}

@app.get("/health")
async def health_check():
    """Health check endpoint (public)"""
    return {"status": "healthy", "auth_enabled": config.ENABLE_AUTH}
