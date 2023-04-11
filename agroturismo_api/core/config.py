from starlette.config import Config

APP_VERSION = "0.0.1"
APP_NAME = "Agroturismo API"
APP_DESCRIPTION = "API para o projeto de agroturismo 🚀"
API_PREFIX = "/api"

config = Config(".env")

IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)
DB_URI: str = config("DB_URI", cast=str, default="sqlite:///./db.sqlite3")

# Cloudinary config
CLOUDINARY_CLOUD_NAME: str = config("CLOUDINARY_CLOUD_NAME", cast=str, default="")
CLOUDINARY_API_KEY: str = config("CLOUDINARY_API_KEY", cast=str, default="")
CLOUDINARY_API_SECRET: str = config("CLOUDINARY_API_SECRET", cast=str, default="")
