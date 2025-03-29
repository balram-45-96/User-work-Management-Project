from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    _id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
