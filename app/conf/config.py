from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    db_url: str | None
    # postgres_db: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: int
    # POSTGRES_PORT: int
    # sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    # mail_username: str
    # mail_password: str
    # mail_from: str
    # mail_port: int
    # mail_server: str
    redis_host: str = 'localhost'
    redis_port: int
    redis_password: str 
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    

    # model_config= SettingsConfigDict( env_file = ".env", env_file_encoding = "utf-8", extra = "allow")


settings = Settings(db_url="postgresql+psycopg2://postgres:567234@localhost:5432/rest_app",
                    # DB_TYPE=postgresql,
                    # DB_CONNECTOR=psycopg2,
                    # DB_HOST=host_database,
                    # DB_PORT=5432,
                    # DB_USER=username,
                    # DB_PASSWORD=password,
                    # DB_NAME=db_name,
                    secret_key="secret_key",
                    algorithm='HS256',
                    redis_host='redis_host',
                    redis_port=16565,
                    redis_password='redis_password',
                    cloudinary_name='cloudinary_name',
                    cloudinary_api_key='1234567890',
                    cloudinary_api_secret='cloudinary_api_secret',
                    )
