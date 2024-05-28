from sqlalchemy.orm import Session

from collections import Counter
from typing import List, Dict

from models import Tag

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
    pass