# gpu 사용 가능한지 테스트 하는 코드
import tensorflow as tf
print("TensorFlow 버전:", tf.__version__)
print("GPU 사용 가능한가?", tf.config.list_physical_devices('GPU'))