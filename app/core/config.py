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

    # Auth related settings
    HASHING_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_COOKIE_NAME: str = "Access-Token"
    ACCESS_SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: float = 30

    REFRESH_TOKEN_COOKIE_NAME: str = "Refresh-Token"
    REFRESH_SECRET_KEY: str = ""
    REFRESH_TOKEN_EXPIRE_DAYS: float = 7

    VERIFICATION_CODE_EXPIRATION_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: str
    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


config = Config()
