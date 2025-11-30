from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from typing import Optional, List, Dict
import logging
from core.config import config

logger = logging.getLogger(__name__)

class DatabaseAuthService:
    def __init__(self):
        """Initialize MongoDB connection for authentication"""
        try:
            self.client = MongoClient(config.MONGODB_URL)
            self.db = self.client[config.MONGODB_DB_NAME]
            self.users = self.db["users"]
            self.query_history = self.db["query_history"]
            
            # Create indexes
            self.users.create_index("email", unique=True)
            self.users.create_index("username", unique=True)
            self.query_history.create_index("user_id")
            self.query_history.create_index("timestamp")
            
            logger.info("MongoDB authentication database initialized")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    # User Operations
    def create_user(self, email: str, username: str, hashed_password: str, 
                   full_name: str, role: str = "user") -> Optional[Dict]:
        """Create a new user"""
        try:
            user_doc = {
                "email": email.lower(),
                "username": username.lower(),
                "hashed_password": hashed_password,
                "full_name": full_name,
                "role": role,
                "is_active": True,
                "is_verified": False,  # Email verification pending
                "created_at": datetime.utcnow(),
                "last_login": None,
                "total_queries": 0
            }
            
            result = self.users.insert_one(user_doc)
            user_doc["_id"] = str(result.inserted_id)
            logger.info(f"Created user: {email}")
            return user_doc
        except DuplicateKeyError:
            logger.warning(f"User already exists: {email}")
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            user = self.users.find_one({"email": email.lower()})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            user = self.users.find_one({"username": username.lower()})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception as e:
            logger.error(f"Error getting user by username: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            from bson import ObjectId
            user = self.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def update_last_login(self, email: str):
        """Update user's last login time"""
        try:
            self.users.update_one(
                {"email": email.lower()},
                {"$set": {"last_login": datetime.utcnow()}}
            )
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
    
    def verify_user_email(self, email: str):
        """Mark user's email as verified"""
        try:
            self.users.update_one(
                {"email": email.lower()},
                {"$set": {"is_verified": True}}
            )
            logger.info(f"Verified email for user: {email}")
        except Exception as e:
            logger.error(f"Error verifying email: {e}")
    
    def get_all_users(self) -> List[Dict]:
        """Get all users (admin only)"""
        try:
            users = list(self.users.find())
            for user in users:
                user["_id"] = str(user["_id"])
            return users
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            from bson import ObjectId
            result = self.users.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count > 0:
                # Also delete user's query history
                self.query_history.delete_many({"user_id": user_id})
                logger.info(f"Deleted user: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
    
    def update_user_role(self, user_id: str, new_role: str) -> bool:
        """Update user's role"""
        try:
            from bson import ObjectId
            result = self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"role": new_role}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating user role: {e}")
            return False
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        try:
            return self.users.count_documents({})
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
    
    # Query History Operations
    def save_query(self, user_id: str, query: str, answer: str, 
                   sources: List[Dict], evaluation: Dict, response_time: float):
        """Save a query to history"""
        try:
            query_doc = {
                "user_id": user_id,
                "query": query,
                "answer": answer,
                "sources": sources,
                "evaluation": evaluation,
                "response_time": response_time,
                "timestamp": datetime.utcnow()
            }
            
            self.query_history.insert_one(query_doc)
            
            # Increment user's total queries
            from bson import ObjectId
            self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"total_queries": 1}}
            )
            
            logger.info(f"Saved query for user: {user_id}")
        except Exception as e:
            logger.error(f"Error saving query: {e}")
    
    def get_user_queries(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's query history"""
        try:
            queries = list(
                self.query_history.find({"user_id": user_id})
                .sort("timestamp", -1)
                .limit(limit)
            )
            for query in queries:
                query["_id"] = str(query["_id"])
            return queries
        except Exception as e:
            logger.error(f"Error getting user queries: {e}")
            return []
    
    def get_all_queries(self, limit: int = 100) -> List[Dict]:
        """Get all queries (admin only)"""
        try:
            queries = list(
                self.query_history.find()
                .sort("timestamp", -1)
                .limit(limit)
            )
            for query in queries:
                query["_id"] = str(query["_id"])
            return queries
        except Exception as e:
            logger.error(f"Error getting all queries: {e}")
            return []
    
    def get_query_stats(self) -> Dict:
        """Get query statistics"""
        try:
            total_queries = self.query_history.count_documents({})
            total_users = self.users.count_documents({})
            active_users = self.users.count_documents({"total_queries": {"$gt": 0}})
            
            return {
                "total_queries": total_queries,
                "total_users": total_users,
                "active_users": active_users,
                "avg_queries_per_user": total_queries / total_users if total_users > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting query stats: {e}")
            return {}

# Global instance
db_auth_service = DatabaseAuthService()
