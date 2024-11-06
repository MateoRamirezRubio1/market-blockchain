from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:root123@db_market:5432/market_bill_microservice"
    )
    BLOCKCHAIN_SERVICE_URL: str = "http://backend:3000/api/v1"

    class Config:
        """
        Configuration for the Settings class.

        Attributes:
        - case_sensitive (bool): Indicates if the settings should be case sensitive.
        """

        case_sensitive = True


# Instantiate the settings object
settings = Settings()
