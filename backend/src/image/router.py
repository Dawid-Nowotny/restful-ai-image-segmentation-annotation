from fastapi import APIRouter, UploadFile, File, Depends, Path, Response, status
from sqlalchemy.orm import Session

from .service import ImageServices, SegmentationServices, AiAnnotationServices, CommentServices
from .schemas import ImageData, ImageFilterParams, TagIdRequest, CommentRequest
from .utils import convert_to_json
from models import User
from get_db import get_db

from user.service import UserServices

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(
    image_data: ImageData = Depends(), 
    file: UploadFile = File(...),
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    image_service = ImageServices()
    segmentation_services = SegmentationServices()

    image_service.rename_file(file)
    binary_pred = file.file.read()
    file.file.seek(0)
    binary_seg_output = file.file.read()
    file.file.seek(0)

    await image_service.validate_file_size_type(file)
    file.file.seek(0)
    
    masks, pred_boxes, pred_class = segmentation_services.get_prediction(binary_pred, threshold=image_data.threshold)
    segmented_image = segmentation_services.get_segmented_image(binary_seg_output, masks, pred_boxes, pred_class)
    segmentation_data = convert_to_json(pred_boxes, pred_class)

    await image_service.add_image_to_database(db, segmented_image, segmentation_data, image_data, current_user.id, file)

    return {"message": "Dodano obrazek"}

@router.get("/get-image/{id}")
def get_image(id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    image = image_service.get_single_image(id, db)

    return Response (
        content=image.image,
        media_type="image/jpg"
    )

@router.get("/get-images/{start_id}/{end_id}")
def get_images(
        start_id: int = Path(..., ge=0), 
        end_id: int = Path(..., ge=0), 
        db: Session = Depends(get_db)
    ):
    image_service = ImageServices()

    images_dict = image_service.get_images_by_range(start_id, end_id, db)
    zip_buffer = image_service.zip_images(images_dict)

    return Response(
        content=zip_buffer.getvalue(), 
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"},
        )

@router.get("/get-user-images/{username}/images/{start_id}/{end_id}")
def get_user_images(username: str, start_id: int = Path(..., ge=0), end_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    user_service = UserServices()
    image_service = ImageServices()

    user = user_service.get_user_by_username(username, db)
    image_dict = image_service.get_user_images_by_range(user, start_id, end_id, db)
    zip_buffer = image_service.zip_images(image_dict)

    return Response(
        content=zip_buffer.getvalue(), 
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"},
        )

@router.get("/get-image-moderator/{image_id}")
def get_image_moderator(image_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    moderator = image_service.get_image_moderator(image_id, db)
    
    return {"username": moderator.username}

@router.get("/get-image-super-tags/{image_id}")
def get_image_supertags(image_id: int, db: Session = Depends(get_db)):
    image_service = ImageServices()
    super_tags = image_service.get_image_super_tags(image_id, db)
    
    return super_tags
      
@router.get("/get-filtered-images/{filters}/{start_id}/{end_id}")
def get_filtered_images(
    start_id: int = Path(..., ge=0),
    end_id: int = Path(..., ge=0),
    filters: ImageFilterParams = Depends(),
    db: Session = Depends(get_db),
    ):
    image_service = ImageServices()

    images_dict = image_service.get_filtered_images_by_range(filters, start_id, end_id, db)
    zip_buffer = image_service.zip_images(images_dict)

    return Response(
        content=zip_buffer.getvalue(), 
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"},
        )

@router.get("/get-images-number")
def get_images_number(db: Session = Depends(get_db)):
    image_service = ImageServices()
    number_of_images = image_service.get_images_number(db)

    return {"number_of_images": number_of_images}

@router.get("/suggest-annotations/{image_id}")
def suggest_annotations(image_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    ai_annotation_services = AiAnnotationServices()

    image = image_service.get_single_image(image_id, db)
    unblobed_image = image_service.blob_to_image(image.image)

    annotations = ai_annotation_services.annotate_image(unblobed_image)

    return {"annotations": annotations}

@router.get("/get-segmented-image/{image_id}")
def get_segmented_image(image_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    image = image_service.get_single_image(image_id, db)
    
    return Response(
        content=image.segmented_image, 
        media_type="image/jpg"
        )

@router.get("/get-image-uploader/{image_id}")
def get_image_data(image_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    image_uploader = image_service.get_uploader_by_image(image_id, db)
    
    return {"image_uploader": image_uploader}

@router.get("/get-image-super-tag-author/{image_id}")
def get_image_data(image_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    super_tag_author = image_service.get_super_tag_author_by_image(image_id, db)
    
    return {"super_tag_author": super_tag_author}

@router.get("/get-image-detections/{image_id}")
def get_image_detections(image_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    image_service = ImageServices()
    threshold = image_service.get_image_threshold(image_id, db)
    coordinates_classes = image_service.get_image_coordinates_classes(image_id, db)

    return {
        "threshold": threshold,
        "coordinates_classes": coordinates_classes
    }

@router.post("/add-tags-to-image", status_code=status.HTTP_201_CREATED)
async def add_tags_to_image(
    request: TagIdRequest,
    comment_data: CommentRequest,
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    comment_service = CommentServices()

    tags = [await comment_service.create_tag(tag_data.tag, db) for tag_data in comment_data.tags]

    await comment_service.create_comment(request.image_id, current_user, comment_data, tags, db)

    return {"message": "Komentarz został dodany do obrazka"}