from pydantic import BaseModel
from backend_config.environments import DB_URL_REAL


class DBSettings(BaseModel):
    url: str = DB_URL_REAL
    # echo: bool = False
    echo: bool = True


db_settings = DBSettings()
