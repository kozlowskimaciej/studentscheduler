from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Channel(BaseModel):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)  # what is slug here? Answer: A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs. Alternative names for this: 

    class Config:
        allow_mutation = False


class UserBase(BaseModel):
    username: str = Field(min_length=1)

    class Config:
        allow_mutation = False


class User(UserBase):
    password: str = Field(min_length=1)


class MessageBody(BaseModel):
    text: str

    class Config:
        allow_mutation = False


class MessageBase(BaseModel):
    body: MessageBody

    class Config:
        allow_mutation = False


class Message(MessageBase):
    sender_username: str
    channel_slug: str  # identifier for the channel
    timestamp: datetime = Field(default_factory=datetime.now)  # created_at
