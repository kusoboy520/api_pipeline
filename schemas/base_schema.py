from pydantic import BaseModel
from typing import Optional

class ResponseSchema(BaseModel):
    userid: Optional[str]
    rec_list: list
    

class Errorinfo(BaseModel):
    error_code: int
    description: str

class ErrorSchema(BaseModel):
    userid: Optional[str]
    error: Errorinfo

    