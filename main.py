from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

app = FastAPI(
    title="FastAPI 기본 애플리케이션",
    description="FastAPI로 만든 기본 API 서버",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[datetime] = None
    views: Optional[int] = None
    like: Optional[int] = None
    content: Optional[str] = None


class BoardCreate(BaseModel):
    title: str
    author: str
    content: str


class BoardOut(BoardCreate):
    id: int
    date: datetime
    views: int = 0
    like: int = 0


class LikeToggle(BaseModel):
    is_liked: bool


board_db: List[BoardOut] = []
board_id_counter = 1


@app.post("/board", response_model=BoardOut, status_code=status.HTTP_201_CREATED)
async def create_board(board: BoardCreate):
    global board_id_counter
    new = BoardOut(id=board_id_counter, date=datetime.now(), **board.dict())
    board_db.append(new)
    board_id_counter += 1
    return new


@app.get("/board", response_model=List[BoardOut], status_code=status.HTTP_200_OK)
async def read_boards():
    return board_db


@app.get("/board/{id}", response_model=BoardOut, status_code=status.HTTP_200_OK)
def read_board(id: int):
    found = next((board for board in board_db if board.id == id), None)
    if not found:
        raise HTTPException(status_code=404, detail="Not found")
    return found


@app.post("/board/update/{id}", status_code=status.HTTP_200_OK)
async def update_board(id: int, board: BoardUpdate):
    for idx, item in enumerate(board_db):
        if item.id == id:
            item.title = board.title if board.title else item.title
            item.author = board.author if board.author else item.author
            item.date = board.date if board.date else item.date
            item.views = board.views if board.views else item.views
            item.like = board.like if board.like else item.like
            item.content = board.content if board.content else item.content
            board_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Not found")


@app.post("/board/editpost/{id}", status_code=status.HTTP_200_OK)
async def editpost_board(id: int, board: BoardUpdate):
    for idx, item in enumerate(board_db):
        if item.id == id:
            item.title = board.title if board.title else item.title
            item.date = board.date if board.date else datetime.now()
            item.content = board.content if board.content else item.content
            board_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Not found")


@app.post("/board/{id}/views", status_code=status.HTTP_200_OK)
async def views_board(id: int):
    for idx, item in enumerate(board_db):
        if item.id == id:
            item.views += 1
            board_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Not found")


@app.post("/board/{id}/like", response_model=BoardOut, status_code=status.HTTP_200_OK)
async def like_board(id: int, payload: LikeToggle):
    for idx, item in enumerate(board_db):
        if item.id == id:
            item.like += 1 if payload.is_liked else -1
            item.like = max(0, item.like)
            board_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Not found")


@app.delete("/board/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(id: int):
    index = next((i for i, b in enumerate(board_db) if b.id == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Not found")
    del board_db[index]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
