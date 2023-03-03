import os

class Config(object):
    def mongo_uri(self):
        mongo_user = os.getenv('MONGO_USER')
        mongo_pass = os.getenv('MONGO_PASS')
        mongo_url = os.getenv('MONGO_URL')
        mongo_port = os.getenv('MONGO_PORT')
        mongo_db = os.getenv('MONGO_DB')
        
        return f"mongodb://{mongo_user}:{mongo_pass}@{mongo_url}:{mongo_port}/{mongo_db}?authSource={mongo_db}"
    
    def mongo_db(self):
        return os.getenv('MONGO_DB')
    
    def security_key(self):
        return os.getenv('SECRET_KEY')
    
    def algorithm(self):
        return os.getenv('ALGORITHM')
    
    def access_token_expire_minutes(self):
        return os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
        
