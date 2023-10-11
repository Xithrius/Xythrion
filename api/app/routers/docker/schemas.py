from pydantic import BaseModel


class DockerContainer(BaseModel):
    container_id: str
    image: str
    created: str
    status: str
    name: str
