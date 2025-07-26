# 교수님 train4csv 파일을 3-class 분류에 맞추고, 파인 튜닝하여 정확도 극대화(0.986)
from keras import models
from keras import layers
import numpy as np

data4train_path = 'data/07-2_add_label(randomized pick)/01_training/label.csv'
data4test_path = 'data/07-2_add_label(randomized pick)/02_evaluation/label.csv'

data4train = np.loadtxt(data4train_path, delimiter=',', dtype=np.float32)
data4test = np.loadtxt(data4test_path, delimiter=',', dtype=np.float32)

train_images = data4train[:, 0:-1]
train_labels = data4train[:, -1].astype(int)   # 1차원 정수 인덱스
test_images = data4test[:, 0:-1]
test_labels = data4test[:, -1].astype(int)

# PCA 정규화(best)
from sklearn.decomposition import PCA
pca = PCA(whiten=True)
train_images = pca.fit_transform(train_images)
test_images = pca.transform(test_images)

# Z-score 정규화(middle)
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# train_images = scaler.fit_transform(train_images)
# test_images = scaler.transform(test_images)

network = models.Sequential()
network.add(layers.Dense(32, activation='relu', input_shape=(24,)))
network.add(layers.Dense(64, activation='relu'))
network.add(layers.Dropout(0.3))
network.add(layers.Dense(32, activation='relu'))
network.add(layers.Dense(3, activation='softmax'))

network.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# batch 사이즈 129 < 256 < 512
# epochs는 지금 당장은 55인데, batch가 작아지면 더 늘려야 함
network.fit(train_images, train_labels, epochs=55, batch_size=256)

test_loss, test_acc = network.evaluate(test_images, test_labels, verbose=2)
print('\n테스트 정확도:', test_acc)