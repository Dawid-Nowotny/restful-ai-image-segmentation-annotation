import pytest
import torch

from src.image.service import AiAnnotationServices

def test_get_model():
    annotation_services = AiAnnotationServices()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = annotation_services._AiAnnotationServices__get_model(device)

    assert isinstance(model, torch.nn.Module)
    assert model.training is False
    assert model.parameters()
    assert model.parameters().__next__().device.type == device.type