import torch
import torch.nn as nn
import os
from PIL import Image
import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from torchvision import datasets, models, transforms
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import random


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


def creating_and_training_neural_network():
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
    train_list, train_test_val, train_val, test_val = train_test_split(list_pictures, class_labels, test_size=0.2,
                                                                       shuffle=True)
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

    fixed_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()
    ])

    train_data = Dataset(train_list, transform=fixed_transforms)
    test_data = Dataset(test_list, transform=fixed_transforms)
    val_data = Dataset(val_list, transform=fixed_transforms)
    train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=10, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_data, batch_size=10, shuffle=True)
    val_loader = torch.utils.data.DataLoader(dataset=val_data, batch_size=10, shuffle=True)

    model = Cnn().to(device)
    model.train()
    optimizer = optim.Adam(params=model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    epochs = 10

    train_accuracy = []
    train_loss = []
    valid_accuracy = []
    valid_loss = []

    for epoch in range(epochs):
        epoch_loss = 0
        epoch_accuracy = 0
        for data, label in train_loader:
            data = data.to(device)
            label = label.to(device)
            output = model(data)
            loss = criterion(output, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            acc = ((output.argmax(dim=1) == label).float().mean())
            epoch_accuracy += acc / len(train_loader)
            epoch_loss += loss / len(train_loader)
        train_accuracy.append(float(epoch_accuracy))
        train_loss.append(float(epoch_loss))
        print('Epoch : {}, train accuracy : {}, train loss : {}'.format(epoch + 1, epoch_accuracy, epoch_loss))
        with torch.no_grad():
            epoch_val_accuracy = 0
            epoch_val_loss = 0
            for data, label in val_loader:
                data = data.to(device)
                label = label.to(device)
                val_output = model(data)
                val_loss = criterion(val_output, label)
                acc = ((val_output.argmax(dim=1) == label).float().mean())
                epoch_val_accuracy += acc / len(val_loader)
                epoch_val_loss += val_loss / len(val_loader)
            valid_accuracy.append(float(epoch_val_accuracy))
            valid_loss.append(float(epoch_val_loss))
            print('Epoch : {}, val_accuracy : {}, val_loss : {}'.format(epoch + 1, epoch_val_accuracy, epoch_val_loss))

        plt.figure(figsize=(15, 5))
        plt.plot(range(len(train_accuracy)), train_accuracy, color="green")
        plt.plot(range(len(valid_accuracy)), valid_accuracy, color="red")
        plt.legend(["Train accuracy", "Valid accuracy"])
        plt.show()
        plt.figure(figsize=(15, 5))
        plt.plot(range(len(train_loss)), [float(value) for value in train_loss], color="green")
        plt.plot(range(len(valid_loss)), [float(value) for value in valid_loss], color="red")
        plt.legend(["Train loss", "Valid loss"])
        plt.show()
    idx = []
    prob = []
    for i in range(len(train_accuracy)):
        idx.append(i)
        prob.append(train_accuracy[i])
    submission = pd.DataFrame({'id': idx, 'label': prob})
    submission.to_csv('result.csv', index=False)


if __name__ == '__main__':
    submission = pd.read_csv('result.csv')
    id_list = []
    class_ = {1: os.path.join("new_dataset", "rose"), 0: os.path.join("new_dataset", "tulip")}
    fig = plt.figure()
    while True:
        try:
            i = random.choice(submission['id'].values)
            class_label_random = random.choice(['tulip', 'rose'])
            label = submission.loc[submission['id'] == i, 'label'].values[0]
            if label > 0.5:
                label = 1
            else:
                label = 0
            img_path = os.path.join("new_dataset", f'{class_label_random}.{i:05d}.jpg')
            img = Image.open(img_path)
            plt.imshow(Image.open(img_path))
            plt.axis('off')
            plt.suptitle(class_[label])
            plt.show()
        except:
            print("error! i'm not this path!")
