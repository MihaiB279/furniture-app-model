import base64
import traceback

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List

from classes_for_requests import Furniture, RoomRequest
from resolv import Resolver
import jwt
from jwt import PyJWTError

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "vfsR6kj4QNDJkH7W5kFAnvf4pmLpShI+sZ2J5aEyi1/Uj9QhtbHtPaKNvd1QkoC5"
decoded_key = base64.urlsafe_b64decode(SECRET_KEY)
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, decoded_key, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/optimize/", response_model=List[Furniture])
async def optimize_room(room_request: RoomRequest, user_payload: dict = Depends(get_current_user)):
    try:
        return process_request(room_request)
    except ValueError as e:
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def process_request(room_request: RoomRequest) -> List[Furniture]:
    resolver = Resolver(room_request.budget, room_request.furniture, room_request.alreadyGenerated)
    if isinstance(resolver.furniture, str):
        raise ValueError(resolver.furniture)

    resolver.set_index_generated()
    resolver.make_ga()
    result = resolver.find_furniture()
    result_furniture = []
    for item in result:
        result_furniture.append(resolver.construct_furniture(str(item)))
    return result_furniture


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
