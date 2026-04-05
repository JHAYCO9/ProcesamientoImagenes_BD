import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    
    SSL_CA_PATH = os.getenv('SSL_CA_PATH', 'ca.pem')