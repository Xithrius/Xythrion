from pydantic import BaseModel


class Hit(BaseModel):
    project_id: str
    project_type: str
    slug: str
    author: str
    title: str
    description: str
    categories: list[str]
    display_categories: list[str]
    versions: list[str]
    downloads: int
    follows: int
    icon_url: str
    date_created: str
    date_modified: str
    latest_version: str
    license: str
    client_side: str
    server_side: str
    gallery: list[str]
    featured_gallery: str | None
    color: int


class ProjectSearchResults(BaseModel):
    hits: list[Hit]
    offset: int
    limit: int
    total_hits: int
