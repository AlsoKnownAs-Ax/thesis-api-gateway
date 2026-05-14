from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "Thesis API Gateway"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""

    # ENV related variables
    ENV: str

    BENCHMARK_SERVICE_URL: str = "localhost:9093"

    # CORS
    ALLOWED_ORIGINS: str

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


config = Config()
