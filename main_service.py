import logging
import fastapi
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from fastapi import Request

from src.api.router.auth_router import router as auth_router
from src.api.router.word_router import router as word_router
from src.api.router.level_router import router as level_router
from src.api.router.group_router import router as group_router
from src.api.router.word_type_router import router as word_type_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --------------------CORS--------------------
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# --------------------Routers--------------------

app.include_router(word_router)
app.include_router(level_router)
app.include_router(group_router)
app.include_router(word_type_router)
app.include_router(auth_router)

# --------------------HELLOW WORLD--------------------
def hello():
    return fastapi.Response(status_code=200, content='Hello, world!')

app.add_api_route('/hello', hello, methods=['GET'])


# --------------------MAIN--------------------

if __name__ == '__main__':
    logging.info("Server is starting ...")
    uvicorn.run(app, host='0.0.0.0', port=8000)