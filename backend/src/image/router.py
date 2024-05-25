from fastapi import APIRouter, UploadFile, File, Depends, Response, status
from sqlalchemy.orm import Session

from .service import UserServices, ImageServices, SegmentationServices, AiAnnotationServices
from .schemas import ImageData
from .utils import convert_to_json
from get_db import get_db

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(image_data: ImageData = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db)):
    user_services = UserServices()
    segmentation_services = SegmentationServices()

    binary_pred = file.file.read()
    file.file.seek(0)
    binary_seg_output = file.file.read()
    file.file.seek(0)

    await user_services.validate_file_size_type(file)
    file.file.seek(0)
    
    masks, pred_boxes, pred_class = segmentation_services.get_prediction(binary_pred, threshold=image_data.threshold)
    segmented_image = segmentation_services.get_segmented_image(binary_seg_output, masks, pred_boxes, pred_class)
    segmentation_data = convert_to_json(pred_boxes, pred_class)

    await user_services.add_image_to_database(db, segmented_image, segmentation_data, image_data, file)

    return {"saved_image": file.filename}

@router.get("/get_images/{start_id}/{end_id}")
def get_images(start_id: int, end_id: int, db: Session = Depends(get_db)):
    image_service = ImageServices()

    images_dict = image_service.get_images_BLOBs_by_range(start_id, end_id, db)
    zip_buffer = image_service.zip_images(images_dict)

    return Response(
        content=zip_buffer.getvalue(), 
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"},
        )

@router.get("/suggest-annotations/{image_id}")
def suggest_annotations(image_id: int, db: Session = Depends(get_db)):
    image_services = ImageServices()
    ai_annotation_services = AiAnnotationServices()

    image_blob = image_services.get_image_BLOB_by_id(image_id, db)
    image = image_services.BLOB_to_image(image_blob)

    annotations = ai_annotation_services.annotate_image(image)

    return {"annotations": annotations}

@router.get("/get-image/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    image_Services = ImageServices()
    image_blob = image_Services.get_image_BLOB_by_id(image_id, db)
    image = image_Services.BLOB_to_bytes(image_blob)
    
    return Response(
        content=image, 
        media_type="image/jpg"
        )

@router.get("/get-segmented-image/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    image_Services = ImageServices()
    image_blob = image_Services.get_segmented_image_BLOB_by_id(image_id, db)
    image = image_Services.BLOB_to_bytes(image_blob)
    
    return Response(
        content=image, 
        media_type="image/jpg"
        )

@router.get("/image-data/{image_id}")
def get_image_data(image_id: int, db: Session = Depends(get_db)):
    image_Services = ImageServices()
    image_uploader = image_Services.get_uploader_by_image(image_id, db)
    super_tag_author = image_Services.get_supertag_author_by_image(image_id, db)
    
    return {"image_uploader": image_uploader,
            "super_tag_author": super_tag_author}