from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "Thesis API Gateway"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "local.db"

    # ENV related variables
    ENV: str

    USER_SERVICE_URL: int = "localhost:5141"
    PRODUCT_SERVICE_URL: int = "localhost:50051"
    ORDER_SERVICE_URL: int = "localhost:9093"

    # CORS
    ALLOWED_ORIGINS: str
    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


config = Config()
