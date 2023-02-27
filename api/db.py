from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def connect_to_mongo():
    logger.info("Connecting to MongoDB..")
    c = Config()
    logger.info(f"URI: {c.mongo_uri()}")
    client = AsyncIOMotorClient(
        str(c.mongo_uri())#, maxPoolSize=Config.max_conn, minPoolSize=Config.min_conn
    )
    db = client[c.mongo_db()]
    logger.info(
        f"Connection succesfully established at {datetime.now().strftime('%Y-%B-%d %H:%M:%S')}."
    )
    return db