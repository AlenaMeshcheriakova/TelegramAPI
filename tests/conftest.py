from fastapi.testclient import TestClient
from main_service import app

client = TestClient(app)
