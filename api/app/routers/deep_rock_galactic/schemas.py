from datetime import datetime

from pydantic import BaseModel


class DeepRockGalacticBuildCreate(BaseModel):
    user_id: int
    dwarf_class: str
    build: str
    overclock: str


class DeepRockGalacticBuild(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    dwarf_class: str
    build: str
    overclock: str
