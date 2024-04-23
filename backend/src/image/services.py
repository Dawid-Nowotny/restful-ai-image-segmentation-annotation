import torch
import requests
import filetype
import numpy as np
import cv2

from fastapi import UploadFile, File, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from PIL import Image as PILImage
from torchvision import models

import random
import json
from datetime import date
from typing import IO, Tuple, List
from io import BytesIO

from models import Image
from .schemas import ImageData
from .constants import LABELS_URL, TRANSFORMS, COCO_INSTANCE_CATEGORY_NAMES

class ImageServices:
    def get_image_BLOB_by_id(self, image_id: int, db: Session) -> bytes:
        image_blob = db.query(Image.image).filter(Image.id == image_id).first()

        if not image_blob:
            raise HTTPException(status_code=404, detail="Image not found")
        return image_blob[0]

    def BLOB_to_image(self, image_blob) -> PILImage.Image:
        return PILImage.open(BytesIO(image_blob))

class UserServices:
    def add_image_to_database(self, db: Session, segmented_image: PILImage.Image, segmentation_data: str, image_data: ImageData, image: UploadFile = File(...)) -> None:
        try:
            image_bytes = BytesIO()
            segmented_image.save(image_bytes, format="JPEG")

            db_image = Image(
                image=image.file.read(),
                segmented_image=image_bytes.getvalue(),
                coordinates_classes=json.loads(segmentation_data),
                upload_date=date.today(),
                uploader_id=image_data.uploader_id,
                moderator_id=image_data.moderator_id,
            )

            db.add(db_image)
            db.commit()
            db.refresh(db_image)

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def validate_file_size_type(self, file: IO) -> None:
        FILE_SIZE = 5 * 1024 * 1024  # 5MB
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
                detail="Unable to determine file type",
            )

        detected_content_type = file_info.extension.lower()

        if (
            file.content_type not in accepted_file_types
            or detected_content_type not in accepted_file_types
        ):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported file type",
            )

        real_file_size = 0
        for chunk in file.file:
            real_file_size += len(chunk)
            if real_file_size > FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Uploaded file is too large. Limit is 5MB",
                )

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

    def get_prediction(self, file, threshold=0.60) -> Tuple[np.ndarray, List[List[Tuple[int, int]]], List[str]]:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        img = PILImage.open(BytesIO(file.file.read()))
        transform = TRANSFORMS
        img = transform(img).to(device)
        model = self.__get_model(device)
        pred = model([img])
        pred_score = list(pred[0]['scores'].detach().cpu().numpy())
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
        masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cpu().numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
        masks = masks[:pred_t + 1]
        pred_boxes = pred_boxes[:pred_t + 1]
        pred_class = pred_class[:pred_t + 1]
        return masks, pred_boxes, pred_class
    
    def get_segmented_image(self, file, masks, boxes, pred_cls, rect_th=3, text_size=3, text_th=3) -> PILImage.Image:
        img_pil = PILImage.open(BytesIO(file.file.read()))
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

        image = preprocess(image).unsqueeze(0)
        image = image.to(device)
        with torch.no_grad():
            outputs = model(image)
        _, indices = torch.topk(outputs, 5)
        annotations = [labels[idx.item()] for idx in indices[0]]
        return annotations