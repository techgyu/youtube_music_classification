import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from keras import models, layers
from keras.preprocessing.image import ImageDataGenerator

# 1. 로컬 디렉토리 경로 설정 (여기만 바꾸면 됨)
base_dir = './data/PetImages'  # 이 경로를 본인의 데이터 위치로 바꿔주세요
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')

#  2. 모델 정의 (Binary Classification: 개 vs 고양이)
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))  # Binary 분류이므로 sigmoid 사용

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 3. 데이터 전처리
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.3  # 30%는 검증용
)

# 4. 데이터 로더
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=20,
    class_mode='binary',
    subset='training',
    seed=1234
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=20,
    class_mode='binary',
    subset='validation',
    seed=1234
)

# 5. 모델 학습
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=5,
    verbose=1
)

# 6. 모델 저장
model.save(os.path.join(base_dir, 'catdog_model_local.h5'))

# 7. 정확도 시각화
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Train vs Validation Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.grid(True)
plt.show()

# 8. 테스트 평가
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(128, 128),
    batch_size=20,
    class_mode='binary'
)

test_loss, test_acc = model.evaluate(test_generator)
print('\n🧪 테스트 정확도:', test_acc)
