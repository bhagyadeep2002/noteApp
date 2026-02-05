from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    heading: str = Field(..., max_length=64, min_length=1)
    body: str = Field(..., max_length=256, min_length=1)


class NoteResponse(BaseModel):
    id: str
    heading: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
