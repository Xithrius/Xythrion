from pydantic import BaseModel, ConfigDict


class License(BaseModel):
    id: str
    name: str
    url: str | None


class DonationUrl(BaseModel):
    id: str
    platform: str
    url: str


class GalleryItem(BaseModel):
    url: str
    featured: bool
    title: str
    description: str
    created: str
    ordering: int


class ProjectResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    client_side: str
    server_side: str
    game_versions: list[str]
    id: str
    slug: str
    project_type: str
    team: str
    organization: str
    title: str
    description: str
    body: str
    body_url: str | None
    published: str
    updated: str
    approved: str
    status: str
    license: License
    downloads: int
    followers: int
    categories: list[str]
    additional_categories: list
    loaders: list[str]
    versions: list[str]
    icon_url: str
    issues_url: str
    source_url: str
    wiki_url: str
    discord_url: str
    donation_urls: list[DonationUrl]
    gallery: list[GalleryItem]
    color: int
    thread_id: str
    monetization_status: str
