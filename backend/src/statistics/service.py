from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from collections import Counter, defaultdict
from typing import List, Dict, Any

from .constants import MONTHS
from models import User, Image, Tag, Comment

class ImageStatsServices:
    def get_top_tags(self, limit: int, db: Session) -> List[Dict[str, int]]:
        tags = [
            {"tag": tag.lower(), "count": count}
            for tag, count in Counter(
                [t.tag.lower() for t in db.query(Tag.tag).all()]
            ).most_common(limit)
        ]

        return tags
    
    def get_popular_tags_by_month(self, db: Session) -> List[Dict[str, Any]]:
        tags_by_month = defaultdict(Counter)
        result = []

        for tag, comment_date in db.query(Tag.tag, Comment.comment_date).join(Comment, Tag.comment_id == Comment.id):
            month_year = (comment_date.year, comment_date.month)
            tags_by_month[month_year].update([tag.lower()])

        for (year, month), tag_counts in sorted(tags_by_month.items()):
            if tag_counts:
                most_common_tag, count = tag_counts.most_common(1)[0]
                result.append({
                    "year": year,
                    "month": MONTHS[month],
                    "top_tag": {"tag": most_common_tag, "count": count}
                })

        return result

    def get_top_classes(self, limit: int, db: Session) -> List[Dict[str, int]]:
        class_counts = Counter()
        images = db.query(Image.coordinates_classes).all()
        for image in images:
            classes = image.coordinates_classes.get("pred_class", [])
            class_counts.update(classes)
        top_classes = [{"class_name": class_name, "count": count} for class_name, count in class_counts.most_common(limit)]

        return top_classes
    
    def get_popular_classes_by_month(self, db: Session) -> Dict[str, Any]:
        classes_by_month = defaultdict(Counter)
        result = []

        for image in db.query(Image.coordinates_classes, Image.upload_date):
            month_year = (image.upload_date.year, image.upload_date.month)
            classes = image.coordinates_classes.get("pred_class", [])
            classes_by_month[month_year].update(classes)

        for (year, month), class_counts in sorted(classes_by_month.items()):
            if class_counts:
                most_common_class, count = class_counts.most_common(1)[0]
                result.append({
                    "year": year,
                    "month": MONTHS[month],
                    "top_classes": {"class_name": most_common_class, "count": count}
                })

        return result

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
    
    def get_top_commenters(self, limit: int, db: Session) -> List[Dict[str, int]]:
        top_commenters = (
            db.query(User.username, func.count(Comment.id).label("comment_count"))
            .join(Comment, User.id == Comment.user_id)
            .filter(Comment.super_tag == False)
            .group_by(User.username)
            .order_by(func.count(Comment.id).desc())
            .limit(limit)
            .all()
        )

        return top_commenters
    
    def get_moderated_images_count(self, limit: int, db: Session) -> List[Dict[str, int]]:
        moderated_counts = (
            db.query(User.username, func.count(Image.id).label("moderated_count"))
            .join(Image, User.id == Image.moderator_id)
            .join(Comment, and_(Comment.image_id == Image.id, Comment.super_tag == True), isouter=True)
            .filter(Comment.id.isnot(None))
            .group_by(User.username)
            .order_by(func.count(Image.id).desc())
            .limit(limit)
            .all()
        )

        return moderated_counts