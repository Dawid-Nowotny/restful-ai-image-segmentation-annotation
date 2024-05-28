from sqlalchemy import func
from sqlalchemy.orm import Session

from collections import Counter
from typing import List, Dict

from models import User, Image, Tag

class ImageStatsServices:
    def get_top_tags(self, limit: int, db: Session) -> List[Dict[str, int]]:
        tags = [
            {"tag": tag.lower(), "count": count}
            for tag, count in Counter(
                [t.tag.lower() for t in db.query(Tag.tag).all()]
            ).most_common(limit)
        ]

        return tags

class UserStatsServices:
    def get_top_uploaders(self, limit: int, db: Session) -> List[Dict[str, int]]:
        top_uploaders = (
            db.query(User.username, func.count(Image.id).label("upload_count"))
            .join(Image, User.id == Image.uploader_id)
            .group_by(User.username)
            .order_by(func.count(Image.id).desc())
            .limit(limit)
            .all()
        )

        return top_uploaders