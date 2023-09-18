from pydantic import BaseModel


class DockerContainerModel(BaseModel):
    container_id: str
    image: str
    created: str
    status: str
    name: str
