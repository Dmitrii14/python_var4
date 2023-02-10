import torch
import torch.nn as nn
import os
from PIL import Image


class Cnn(nn.Module):
    """
    Класс построения модели:
    3 слоя свертки и пакетная нормализация для ограничения переобучения
    """
    def __init__(self):
        super(Cnn, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc1 = nn.Linear(3 * 3 * 64, 10)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(10, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0), -1)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return out


class Dataset(torch.utils.data.Dataset):
    """
        Этот класс предназначен для загрузки изображений
    """
    def __init__(self, file_list, transform=None):
        self.transform = transform
        self.file_list = file_list

    def __len__(self):
        self.filelength = len(self.file_list)
        return self.filelength

    def __getitem__(self, idx: int):
        img = Image.open(self.file_list[idx])
        img_transformed = self.transform(img.convert("RGB"))
        label = self.file_list[idx].split('/')[-1].split('.')[0]
        if label == os.path.join("new_dataset", "rose"):
            label = 1
        elif label == os.path.join("new_dataset", "tulip"):
            label = 0
        return img_transformed, label
