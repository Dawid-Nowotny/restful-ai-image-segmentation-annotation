from fastapi import HTTPException, status
import json

def convert_to_json(pred_boxes, pred_class) -> str:
    pred_boxes_int = [[[int(coord) for coord in box_coords] for box_coords in box] for box in pred_boxes]
    
    data = {
        "pred_boxes": pred_boxes_int,
        "pred_class": pred_class
    }

    json_data = json.dumps(data)
    return json_data

def get_images_in_range(images, start_id, end_id):
    if start_id < 0 or end_id < 0 or start_id >= end_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nieprawidłowy zakres identyfikatorów obrazów")

    images_dict = {}
    images_in_range = images[start_id:end_id]
    for image in images_in_range:
        images_dict[image.id] = image.image

    return images_dict