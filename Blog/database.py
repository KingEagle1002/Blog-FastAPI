from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://test_user:test_user@cluster0.xdzl1ca.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URI)

db = client["blog_db"]
users_collection = db["users"]
blogs_collection = db["blogs"]
