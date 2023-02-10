import torch
import torch.nn as nn
import os
from PIL import Image
import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


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

def сreating_and_training_neural_network():
    """
        эта функция создает и обучает модели нейронной сети и сохраняет результаты в специальный файл - result.csv,
        а также строит графики и анализирует результаты.
    """

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    torch.manual_seed(1234)
    if device == 'cuda':
        torch.cuda.manual_seed_all(1234)

    class_labels = []
    for i in range(1000):
        class_labels.append(True)
    for i in range(1000):
        class_labels.append(False)

    list_pictures = glob.glob(os.path.join('new_dataset', '*.jpg'))
    train_list, train_test_val, train_val, test_val = train_test_split(list_pictures, class_labels, test_size=0.2, shuffle=True)
    test_list, val_list, test, val = train_test_split(train_test_val, test_val, test_size=0.5)

    random_idx = np.random.randint(1, len(list_pictures), size=10)
    fig = plt.figure()
    i = 1
    for idx in random_idx:
        ax = fig.add_subplot(2, 5, i)
        img = Image.open(list_pictures[idx])
        plt.imshow(img)
        i += 1
    plt.axis('off')
    plt.show()
