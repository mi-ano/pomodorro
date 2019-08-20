import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "DATABASE_URL"
    DEBUG = False

class DevConfig(Config):
    DEBUG = True


config_options = {"development": DevConfig, "production": ProdConfig}    