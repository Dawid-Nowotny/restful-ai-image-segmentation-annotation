from fastapi import APIRouter, UploadFile, File, Depends, Response
from sqlalchemy.orm import Session

import json

from .services import UserServices, ImageServices, SegmentationServices, AiAnnotationServices
from .schemas import ImageData
from .utils import convert_to_json
from get_db import get_db

router = APIRouter()

@router.post("/upload")
def upload(image_data: ImageData = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db)):
    user_services = UserServices()
    segmentation_services = SegmentationServices()

    binary_pred = file.file.read()
    file.file.seek(0)
    binary_seg_output = file.file.read()
    file.file.seek(0)

    user_services.validate_file_size_type(file)
    file.file.seek(0)
    
    masks, pred_boxes, pred_class = segmentation_services.get_prediction(binary_pred, threshold=image_data.threshold)
    segmented_image = segmentation_services.get_segmented_image(binary_seg_output, masks, pred_boxes, pred_class)
    segmentation_data = convert_to_json(pred_boxes, pred_class)

    user_services.add_image_to_database(db, segmented_image, segmentation_data, image_data, file)

    return Response(
        content=json.dumps({"saved_image": file.filename}),
        media_type="application/json",
        status_code=200,
    )

@router.get("/suggest-annotations/{image_id}")
def suggest_annotations(image_id: int, db: Session = Depends(get_db)):
    image_services = ImageServices()
    ai_annotation_services = AiAnnotationServices()

    image_blob = image_services.get_image_BLOB_by_id(image_id, db)
    image = image_services.BLOB_to_image(image_blob)

    annotations = ai_annotation_services.annotate_image(image)

    return Response(
        content=json.dumps({"annotations": annotations}),
        media_type="application/json",
        status_code=200,
    )