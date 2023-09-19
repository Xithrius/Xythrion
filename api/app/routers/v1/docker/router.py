import docker
from docker.models.containers import Container
from fastapi import APIRouter, status

from .models import DockerContainerModel

router = APIRouter()

docker_client = docker.from_env()


def extract_container_info(container: Container) -> DockerContainerModel | None:
    attrs = container.attrs

    if attrs is None:
        return None

    d = {
        "container_id": attrs["Id"][:12],
        "image": attrs["Config"]["Image"],
        "created": attrs["Created"],
        "status": attrs["State"]["Status"],
        "name": attrs["Name"][1:],
    }

    docker_container = DockerContainerModel.parse_obj(d)

    return docker_container


@router.get(
    "/containers",
    response_model=list[DockerContainerModel],
    status_code=status.HTTP_200_OK,
)
async def list_running_containers() -> list[DockerContainerModel]:
    containers = []

    for container in docker_client.containers.list():
        if not isinstance(container, Container):
            continue

        info = extract_container_info(container)

        if info is not None:
            containers.append(info)

    return containers
