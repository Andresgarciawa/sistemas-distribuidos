import os


class Config:
    SECRET_KEY = os.getenv('BOOKSHARE_SECRET_KEY', 'bookshare-dev-key')
    API_BASE_URL = os.getenv('BOOKSHARE_API_URL', 'http://localhost:8000/api/v1')
    USE_MOCKS = os.getenv('BOOKSHARE_USE_MOCKS', 'true').lower() == 'true'
