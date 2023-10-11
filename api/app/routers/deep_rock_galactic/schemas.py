from pydantic import BaseModel


class DeepRockGalacticBuild(BaseModel):
    user_id: int
    dwarf_class: str
    build: str
    overclock: str
