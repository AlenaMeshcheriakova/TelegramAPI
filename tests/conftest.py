from fastapi.testclient import TestClient
from src.api.main_service import app

client = TestClient(app)
