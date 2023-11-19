from typing import List

from fastapi import APIRouter, Body, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.tags import ImageTagModel, ImageTagResponse
from app.repository import tags as repository_tags

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/all tags/", response_model=List[ImageTagResponse])
async def read_tags(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    return await repository_tags.get_tags(skip, limit, db)


@router.get("/get tag by id/{tag_id}", response_model=ImageTagResponse)
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post("/", response_model=List[ImageTagResponse])
async def create_tag(tags: list[ImageTagModel], db: Session = Depends(get_db)):
    return await repository_tags.create_tag(tags, db)


@router.put("/{tag_id}", response_model=ImageTagResponse)
async def update_tag(body: ImageTagModel, tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=ImageTagResponse)
async def remove_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag
