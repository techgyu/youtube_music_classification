# 추출해낸 2차원 사상 이미지로 CNN 돌리는 거
# 엄청 오래 걸림(epoch 30회에 약 1시간 30분 정도 걸림)
import os
import numpy as np
import tensorflow as tf
from keras import layers
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras.regularizers import l2 # L2 정규화 사용을 위한 임포트

# 디렉토리 경로
base_dir = './data/09_chart_image_data'
train_dir = os.path.join(base_dir, 'training')
test_dir = os.path.join(base_dir, 'evaluation')

#  모델 정의 (3-class)
# model = tf.keras.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
# model.add(layers.MaxPooling2D(2, 2))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D(2, 2))
# model.add(layers.Flatten())
# model.add(layers.Dense(512, activation='relu'))
# model.add(layers.Dense(3, activation='softmax'))

model = tf.keras.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
#model.add(layers.BatchNormalization()) # 각 conv 레이어 뒤에 배치 정규화 추가
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
#model.add(layers.BatchNormalization()) # 각 conv 레이어 뒤에 배치 정규화 추가
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Flatten())
# model.add(layers.GlobalAveragePooling2D()) # 과적합 방지용, 파라미터를 flatten에 비해 줄일 수 있음, 오히려 악 영향
model.add(layers.Dense(128, activation='relu'))
# model.add(layers.Dense(512, activation='relu', kernel_regularizer=l2(0.001)))
model.add(layers.Dropout(0.5))  # 과적합 방지용 추가
model.add(layers.Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 데이터 전처리
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255.,
    validation_split=0.3
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=128,
    class_mode='categorical',
    subset='training',
    seed=1234
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=128,
    class_mode='categorical',
    subset='validation',
    seed=1234
)

# 학습
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=5,
    verbose=1,
    workers=6,
    max_queue_size=10          # queue 크기도 충분히 크게
)


# 모델 저장
model.save(os.path.join(base_dir, 'chart_classifier_model.h5'))

# 테스트 평가
test_datagen = ImageDataGenerator(rescale=1.0 / 255.)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(128, 128),
    batch_size=128,
    class_mode='categorical'
)

test_loss, test_acc = model.evaluate(test_generator)
print('\n테스트 정확도:', test_acc)