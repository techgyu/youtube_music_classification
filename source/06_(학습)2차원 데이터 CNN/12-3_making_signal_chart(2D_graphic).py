# 2차시에 앞 전에서 이야기 했던 음성 신호 그래프 만들고, peak 뽑아서 처리하려고 했었지만!
# 이건 과제에 반영하지 않음
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

# 1. 처리할 최상위 디렉토리 경로
dir_path = "data/temp"  # 여기에 대상 디렉토리 경로 입력

# 2. os.walk를 이용해 하위 디렉토리까지 순회
for root, dirs, files in os.walk(dir_path):
    for file_name in files:
        if file_name.endswith(".txt"):
            txt_path = os.path.join(root, file_name)

            # 3. waveform 로드
            with open(txt_path, "r") as f:
                waveform = np.array([float(line.strip()) for line in f if line.strip() != ""])

            # 4. 샘플링 주파수
            sr = 44100  # 고정값

            # 5. Mel-spectrogram 생성
            S = librosa.feature.melspectrogram(y=waveform, sr=sr, n_mels=128)
            S_dB = librosa.power_to_db(S, ref=np.max)

            # 6. 저장 경로 설정 (.png) - 같은 폴더에 저장
            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(root, f"{base_name}.png")

            # 7. 시각화 및 저장
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
            plt.colorbar(format='%+2.0f dB')
            plt.title(f'Mel-frequency spectrogram: {base_name}')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
            plt.close()

            print(f"Saved: {output_path}")