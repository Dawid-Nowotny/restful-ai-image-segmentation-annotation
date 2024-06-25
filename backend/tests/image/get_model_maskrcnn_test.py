import pytest
import torch

from src.image.service import SegmentationServices

def test_get_model():
    segmentation_services = SegmentationServices()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = segmentation_services._SegmentationServices__get_model(device)

    assert isinstance(model, torch.nn.Module)
    assert model.training is False
    assert model.parameters()
    assert model.parameters().__next__().device.type == device.type