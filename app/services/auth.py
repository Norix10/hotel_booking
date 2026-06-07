import jwt 
from datetime import datetime, timedelta, timezone

from app.schemas.auth import AccessTokenDataSchema
from app.core.config import settings

def create_access_token(data: AccessTokenDataSchema):
    to_encode = data.model_dump().copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt