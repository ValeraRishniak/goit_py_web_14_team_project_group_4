from typing import Optional
from pydantic import BaseModel
import datetime
from fastapi import Body

class CommentBase(BaseModel):
    
    comment_description:str
   

class CommentList(CommentBase):
    id: int
    post_id:int
    created_date: Optional[datetime.datetime]= Body(None)

    class Config:
        from_attributes= True
        