from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from typing import List

from .service import ImageStatsServices, UserStatsServices
from get_db import get_db

router = APIRouter()

@router.get("/top_tags/{limit}", response_model=List[dict])
def get_top_tags(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    image_stats_service = ImageStatsServices()
    tags = image_stats_service.get_top_tags(limit, db)

    return tags