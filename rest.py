import base64

from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from model.resolv import Resolver
import jwt  # Import the jwt module from PyJWT
from jwt import PyJWTError  # Import the specific JWTError

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "vfsR6kj4QNDJkH7W5kFAnvf4pmLpShI+sZ2J5aEyi1/Uj9QhtbHtPaKNvd1QkoC5"
decoded_key = base64.urlsafe_b64decode(SECRET_KEY)
ALGORITHM = "HS256"


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


def construct_furniture(furniture_string):
    furniture = Furniture(
        furnitureType="",
        name="",
        company="",
        details="",
        price=0.0
    )
    count_commas = 0
    index = -1

    for i in range(len(furniture_string) - 1, -1, -1):
        if furniture_string[i] == ',':
            count_commas += 1
            if count_commas == 4:
                index = i
                break

    details = furniture_string[:index]
    rest_furniture = furniture_string[index + 1:].strip()
    parts = rest_furniture.split(',')

    for part in parts:
        separated_elements = part.split(": ' ")
        key = separated_elements[0].strip().strip("'")
        value = separated_elements[1].strip().strip("'")

        if key == "Price":
            furniture.price = float(value)
        elif key == "Company":
            furniture.company = value
        elif key == "Name":
            furniture.name = value
        elif key == "Furniture Type":
            furniture.furnitureType = value.strip('\'}')

    furniture.details = details.strip()
    return furniture


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, decoded_key, algorithms=[ALGORITHM])
        return payload  # returning the whole payload for demonstration
    except PyJWTError as e:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/optimize/", response_model=List[Furniture])
async def optimize_room(room_request: RoomRequest, user_payload: dict = Depends(get_current_user)):
    try:
        result = process_request(room_request)
        result_furniture = []
        for item in result:
            result_furniture.append(construct_furniture(str(item)))
        return result_furniture
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def process_request(room_request: RoomRequest) -> List[Furniture]:
    resolver = Resolver(room_request.budget, room_request.furniture, room_request.alreadyGenerated)
    if isinstance(resolver.furniture, str):
        raise ValueError("Invalid furniture data: " + resolver.furniture)

    resolver.set_index_generated()
    resolver.make_ga()
    return resolver.find_furniture()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
