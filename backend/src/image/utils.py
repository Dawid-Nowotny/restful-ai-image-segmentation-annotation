import json

def convert_to_json(pred_boxes, pred_class) -> str:
    pred_boxes_int = [[[int(coord) for coord in box_coords] for box_coords in box] for box in pred_boxes]
    
    data = {
        "pred_boxes": pred_boxes_int,
        "pred_class": pred_class
    }

    json_data = json.dumps(data)
    return json_data

def create_images_dict(images) -> dict:
    images_dict = {}
    for image in images:
        images_dict[image.id] = image.image

    return images_dict

def check_start_end_id(start_id, end_id) -> bool:
    return start_id < 0 or end_id < 0 or start_id > end_id