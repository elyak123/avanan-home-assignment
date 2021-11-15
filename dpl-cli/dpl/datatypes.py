from dataclasses import dataclass


@dataclass
class Config:
    queue_name: str
    region: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
    django_url: str
