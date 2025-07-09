from pydantic import BaseModel

class BordsBase(BaseModel):
    title: str
    content: str

class BordsCreate(BordsBase):
    pass

class BordsOut(BordsBase):
    id: int

    class Config:
        orm_mode = True