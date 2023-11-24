import cloudinary
from pydantic_settings import BaseSettings


def config_cloudinary():
    """
    The config_cloudinary function is used to configure the cloudinary library with the
        credentials stored in settings.py. This function should be called before any other
        cloudinary functions are called.
    
    :return: A dict with the cloudinary configuration
    """
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )
    


class Settings(BaseSettings):
    database_url: str = "database_url"
    secret_key: str = "secretkey"
    algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "secretPassword"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "redis_host"
    redis_port: int = 6379
    redis_password: str = "redis_password"
    cloudinary_name: str = "name"
    cloudinary_api_key: int = 716354361176382
    cloudinary_api_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()
