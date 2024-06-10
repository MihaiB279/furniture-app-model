from pydantic import BaseModel
from typing import List, Optional


class Furniture(BaseModel):
    furnitureType: str
    name: Optional[str] = None
    company: Optional[str] = None
    details: Optional[str] = None
    price: Optional[float] = 0.0

    class Config:
        allow_mutation = True


class RoomRequest(BaseModel):
    budget: float
    furniture: List[Furniture]
    alreadyGenerated: Optional[List[List[Furniture]]] = None
