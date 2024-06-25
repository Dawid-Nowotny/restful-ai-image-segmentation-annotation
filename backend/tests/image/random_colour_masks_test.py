import pytest
import numpy as np

from src.image.service import SegmentationServices

def test_random_colour_masks():
    segmentation_services = SegmentationServices()
    img = np.array([[0, 1, 0],
                    [1, 0, 1],
                    [0, 1, 0]])

    coloured_mask = segmentation_services._SegmentationServices__random_colour_masks(img)

    assert coloured_mask.shape == (img.shape[0], img.shape[1], 3)

    colours = [[0, 255, 0],[0, 0, 255],[255, 0, 0],[0, 255, 255],[255, 255, 0],
               [255, 0, 255],[80, 70, 180],[250, 80, 190],[245, 145, 50],[70, 150, 250]]
    
    expected_colours = set(tuple(c) for c in colours)
    actual_colours = set(tuple(col) for col in coloured_mask.reshape(-1, 3) if any(col))

    assert actual_colours <= expected_colours

    example_img = np.array([[0, 1, 0],
                            [1, 0, 1],
                            [0, 1, 0]])
    example_coloured_mask = segmentation_services._SegmentationServices__random_colour_masks(example_img)
    assert example_coloured_mask.shape == (3, 3, 3)