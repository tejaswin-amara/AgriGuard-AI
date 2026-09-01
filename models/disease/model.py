import torch.nn as nn
from torchvision.models import mobilenet_v2


class DiseaseModelDemo(nn.Module):
    """
    A demo PyTorch model using MobileNetV2 for inference.
    THIS IS A PROTOTYPE/DEMO MODEL. Not trained on a real crop disease dataset.
    """

    def __init__(self, num_classes=3):
        super(DiseaseModelDemo, self).__init__()
        self.backbone = mobilenet_v2(pretrained=False)
        self.backbone.classifier[1] = nn.Linear(self.backbone.last_channel, num_classes)

    def forward(self, x):
        return self.backbone(x)
