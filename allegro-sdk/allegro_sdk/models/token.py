from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    allegro_api: bool
    jti: str
