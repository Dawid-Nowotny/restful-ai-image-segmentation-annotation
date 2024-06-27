import torch
import requests
import filetype
import numpy as np
import cv2

from fastapi import UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from PIL import Image as PILImage
from torchvision import models

import zipfile
import random
import json
from datetime import date
from typing import IO, Tuple, List, Dict, Union, Any
from io import BytesIO
import os
import uuid

try:
    from models import Image, Tag, User, Comment
except ModuleNotFoundError:
    from src.models import Image, Tag, User, Comment
from .schemas import ImageData, ImageFilterParams
from .constants import FILE_SIZE, LABELS_URL, TRANSFORMS, COCO_INSTANCE_CATEGORY_NAMES
from .utils import get_images_in_range

class ImageServices:
    def get_single_image(self, image_id: int, db: Session) -> Image:
        image = db.query(Image).filter(Image.id == image_id).first()

        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono obrazu")
        return image
    
    def get_image_moderator(self, image_id: int, db: Session) -> User:
        image = self.get_single_image(image_id, db)

        if not image.moderator:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono moderatora dla danego zdjecia")
        return image.moderator
    
    def get_image_super_tags(self, image_id: int, db: Session) -> dict[str, Any]:
        comments_with_super_tags = db.query(Comment).filter(Comment.image_id == image_id, Comment.super_tag == True).all()

        if not comments_with_super_tags:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono supertagów dla danego zdjecia")
        
        super_tags_dict = {}
        
        for comment in comments_with_super_tags:
            super_tags_dict.update({
                "author": comment.user.username,
                "tags": comment.tags
            })

        if super_tags_dict is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono supertagów dla danego zdjecia")
        
        return super_tags_dict

    def get_images_by_range(self, start_id: int, end_id: int, db: Session) -> dict:
        images = db.query(Image).all()

        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono obrazów w podanym zakresie")

        return get_images_in_range(images, start_id, end_id)
    
    def get_filtered_images_by_range(self, filters: ImageFilterParams, start_id: int, end_id: int, db: Session) -> dict:
        query = db.query(Image).options(joinedload(Image.comments).joinedload(Comment.tags))

        if filters.threshold_range:
            query = query.filter(Image.threshold.between(*filters.threshold_range))
        
        if filters.tags:
            filters.tags = filters.tags[0].split(",")
            tag_filters = [Tag.tag.in_(filters.tags)]
            query = query.filter(Image.comments.any(Comment.tags.any(or_(*tag_filters))))

        if filters.classes:
            filters.classes = filters.classes[0].split(",")
            class_filters = [Image.coordinates_classes.op('->>')('pred_class').contains(c) for c in filters.classes]
            query = query.filter(or_(*class_filters))

        images = query.all()

        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono obrazów spełniających podane kryteria filtrowania.")

        return get_images_in_range(images, start_id, end_id)
    
    def get_user_images_by_range(self, user: User, start_id: int, end_id: int, db: Session) -> dict:
        images = db.query(Image).filter(Image.uploader_id == user.id).order_by(Image.id).all()

        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono obrazów spełniających podane kryteria filtrowania.")

        return get_images_in_range(images, start_id, end_id)

    def zip_images(self, images_dict: dict) -> BytesIO:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for image_id, image_blob in images_dict.items():
                zip_file.writestr(f'{image_id}.jpg', image_blob)
        zip_buffer.seek(0)
        return zip_buffer

    def blob_to_image(self, image_blob) -> PILImage.Image:
        return PILImage.open(BytesIO(image_blob))

    def get_images_number(self, db: Session) -> int:
        return db.query(Image).count()
    
    def get_uploader_by_image(self, image_id: int, db: Session) -> str:
        result = db.query(User.username).join(Image, User.id == Image.uploader_id).filter(Image.id == image_id).first()
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brak przesyłającego zdjęcie")
        return result[0]
    
    def get_super_tag_author_by_image(self, image_id: int, db: Session) -> str:
        result = db.query(User.username).join(Comment, Comment.user_id == User.id).join(
            Image, Image.id == Comment.image_id).filter(Image.id == image_id, Comment.super_tag == True).first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brak autora supertagów")
        return result[0]
    
    def get_image_threshold(self, image_id: int, db: Session) -> json:
        result = db.query(Image.threshold).filter(Image.id == image_id).first()
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brak progu detekcji")
        return result[0]

    def get_image_coordinates_classes(self, image_id: int, db: Session) -> json:
        result = db.query(Image.coordinates_classes).filter(Image.id == image_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brak koordynatów klas")
        return result[0]

    async def add_image_to_database(self, db: Session, segmented_image: PILImage.Image, segmentation_data: str, image_data: ImageData, uploader_id: int, image: UploadFile = File(...)) -> None:
        image_bytes = BytesIO()
        segmented_image.save(image_bytes, format="JPEG")

        db_image = Image(
            image=image.file.read(),
            segmented_image=image_bytes.getvalue(),
            coordinates_classes=json.loads(segmentation_data),
            threshold=image_data.threshold,
            upload_date=date.today(),
            uploader_id=uploader_id,
            moderator_id=None,
        )

        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
    async def validate_file_size_type(self, file: IO) -> None:
        accepted_file_types = [
            "image/png",
            "image/jpeg",
            "image/jpg",
            "png",
            "jpeg",
            "jpg",
        ]

        file_info = filetype.guess(file.file)
        if file_info is None:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Nie można określić typu pliku",
            )

        detected_content_type = file_info.extension.lower()

        if (
            file.content_type not in accepted_file_types
            or detected_content_type not in accepted_file_types
        ):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Nieobsługiwany typ pliku",
            )

        real_file_size = 0
        for chunk in file.file:
            real_file_size += len(chunk)
            if real_file_size > FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Przesłany plik jest za duży. Limit wynosi 5MB",
                )
            
    def rename_file(self, file: UploadFile) -> None:
        random_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        file.filename = random_filename

class SegmentationServices:
    def __get_model(self, device) -> torch.nn.Module:
        model = models.detection.maskrcnn_resnet50_fpn(pretrained=True, weights="MaskRCNN_ResNet50_FPN_Weights.DEFAULT")
        model.eval()
        return model.to(device)

    def __random_colour_masks(self, img) -> np.ndarray:
        colours = [[0, 255, 0],[0, 0, 255],[255, 0, 0],[0, 255, 255],[255, 255, 0],[255, 0, 255],[80, 70, 180],[250, 80, 190],[245, 145, 50],[70, 150, 250],[50, 190, 190]]
        r = np.zeros_like(img).astype(np.uint8)
        g = np.zeros_like(img).astype(np.uint8)
        b = np.zeros_like(img).astype(np.uint8)
        r[img == 1], g[img == 1], b[img == 1] = colours[random.randrange(0,10)]
        coloured_mask = np.stack([r, g, b], axis=2)
        return coloured_mask

    def get_prediction(self, binary, threshold=0.60) -> Tuple[np.ndarray, List[List[Tuple[int, int]]], List[str]]:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        img = PILImage.open(BytesIO(binary)).convert("RGB")
        transform = TRANSFORMS
        img = transform(img).to(device)
        model = self.__get_model(device)
        pred = model([img])
        pred_score = list(pred[0]['scores'].detach().cpu().numpy())
        if not any(x > threshold for x in pred_score):
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Nie znaleziono predykcji")
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
        masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cpu().numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
        masks = masks[:pred_t + 1]
        pred_boxes = pred_boxes[:pred_t + 1]
        pred_class = pred_class[:pred_t + 1]
        return masks, pred_boxes, pred_class
    
    def get_segmented_image(self, binary, masks, boxes, pred_cls, rect_th=3, text_size=3, text_th=3) -> PILImage.Image:
        img_pil = PILImage.open(BytesIO(binary)).convert("RGB")
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        for i in range(len(masks)):
            rgb_mask = self.__random_colour_masks(masks[i])
            img = cv2.addWeighted(img, 1, rgb_mask, 0.5, 0)
            pt1 = tuple(int(coord) for coord in boxes[i][0])
            pt2 = tuple(int(coord) for coord in boxes[i][1])
            cv2.rectangle(img, pt1, pt2, color=(0, 255, 0), thickness=rect_th)
            cv2.putText(img, pred_cls[i], pt1, cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,255,0), thickness=text_th)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return PILImage.fromarray(img)

class AiAnnotationServices:
    def __get_model(self, device) -> torch.nn.Module:
        model = models.resnet50(weights="ResNet50_Weights.DEFAULT")
        model.eval()
        return model.to(device)

    def __get_labels(self) -> list:
        return requests.get(LABELS_URL).json()

    def annotate_image(self, image) -> list:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = self.__get_model(device)
        labels = self.__get_labels()
        preprocess = TRANSFORMS

        image = preprocess(image)[:3]
        image = image.unsqueeze(0)
        image = image.to(device)

        with torch.no_grad():
            outputs = model(image)
        _, indices = torch.topk(outputs, 5)
        annotations = [labels[idx.item()] for idx in indices[0]]
        return annotations

class CommentServices:
    async def create_tag(self, tag_name, db) -> Tag:
        tag = Tag(tag=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    async def create_comment(self, image_id, user, comment_data, tags, db) -> None:
        comment = Comment(
            super_tag=comment_data.super_tag,
            comment_date=date.today(),
            image_id=image_id,
            user_id=user.id
        )

        comment.tags.extend(tags)

        db.add(comment)
        db.commit()
        db.refresh(comment)

    def check_if_image_has_supertags(self, image, db):
        supertag_comments = db.query(Comment).filter(
            Comment.image_id == image.id,
            Comment.super_tag == True
        ).all()

        if supertag_comments:
            raise HTTPException(status_code=400, detail="To zdjęcie już ma supertagi")
   
    def get_comments_with_tags_by_image_id(self, image_id: int, db: Session) -> List[Dict[str, Union[int, str, List[str]]]]:
        comments = db.query(Comment).filter(Comment.image_id == image_id).all()
        
        if not comments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono komentarzy dla danego obrazu")
        
        result = []
        for comment in comments:
            tags = [tag.tag for tag in comment.tags]
            result.append({
                "comment_id": comment.id,
                "username": comment.user.username,
                "tags": tags
            })
        
        return result