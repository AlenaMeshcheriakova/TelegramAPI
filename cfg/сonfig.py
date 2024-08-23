from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    MODE: str

    JWT_SECRET: str
    JWT_LIFETIME: int

    GRPC_HOST: str
    GRPC_PORT: int

    GRPC_AUTH_HOST: str
    GRPC_AUTH_PORT: int

    @property
    def JWT_PASSWORD(self) -> str:
        return self.JWT_SECRET

    @property
    def JWT_LIFETIME(self) -> int:
        return self.JWT_LIFETIME

    @property
    def get_GRPC_conn(self) -> str:
        return f"{self.GRPC_HOST}:{str(self.GRPC_PORT)}"

    @property
    def get_AUTH_GRPC_conn(self) -> str:
        return f"{self.GRPC_AUTH_HOST}:{str(self.GRPC_AUTH_PORT)}"


    model_config = SettingsConfigDict(env_file="/cfg/development/.env")

load_dotenv()
settings = Settings()