import json

def convert_to_json(pred_boxes, pred_class) -> str:
    pred_boxes_int = [[[int(coord) for coord in box_coords] for box_coords in box] for box in pred_boxes]
    
    data = {
        "pred_boxes": pred_boxes_int,
        "pred_class": pred_class
    }

    json_data = json.dumps(data)
    return json_data