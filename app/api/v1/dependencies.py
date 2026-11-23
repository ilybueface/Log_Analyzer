from typing import Annotated
from fastapi import Depends
from app.core.config import Settings, settings


def get_settings() -> Settings:
    return settings


SettingsDependency = Annotated[Settings, Depends(get_settings)]
