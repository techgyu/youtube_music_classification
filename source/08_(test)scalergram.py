# 음성 데이터 시각화 테스트(실제로 사용하지 않았음)
import os
import pywt
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import csv
import re

# 자연스러운 파일 정렬을 위한 키
def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# MP3를 waveform으로 변환
def mp3_to_waveform(mp3_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path).set_channels(1)
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        return samples, audio.frame_rate
    except Exception as e:
        print("[!] mp3_to_waveform 에러:", e)
        return None, None

# 라벨 추출 (폴더 이름에 따라)
def get_label_from_path(path):
    path_lower = path.lower()
    if 'classic' in path_lower:
        return 0
    elif 'hiphop' in path_lower:
        return 1
    elif 'trot' in path_lower:
        return 2
    else:
        return -1  # 알 수 없는 경우

# 스케일로그램 이미지 생성 및 저장
def generate_scalogram(samples, wavelet='morl', save_path=None, figsize=(4, 4)):
    try:
        widths = np.arange(1, 128)
        cwtmatr, _ = pywt.cwt(samples, widths, wavelet)
        plt.ioff()  # matplotlib GUI 비활성화
        fig, ax = plt.subplots(figsize=figsize)
        ax.imshow(np.abs(cwtmatr), extent=[0, len(samples), 1, 128], cmap='jet', aspect='auto', origin='lower')
        ax.axis('off')
        plt.tight_layout(pad=0)
        if save_path:
            fig.savefig(save_path, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            return save_path
        else:
            plt.show()
    except Exception as e:
        print("[!] generate_scalogram 에러:", e)
        return None

# 전체 디렉토리 처리
def process_directory_with_scalogram(input_path, image_output_dir, csv_output_path=None, wavelet_name='morl'):
    if csv_output_path is None:
        csv_output_path = os.path.join(input_path, "label.csv")
    os.makedirs(image_output_dir, exist_ok=True)
    results = []

    for root, dirs, files in os.walk(input_path):
        files.sort(key=natural_key)
        for file in files:
            if file.lower().endswith('.mp3'):
                full_path = os.path.join(root, file)
                print(f"🎵 처리 중: {full_path}")
                samples, sr = mp3_to_waveform(full_path)
                if samples is not None:
                    try:
                        filename_wo_ext = os.path.splitext(file)[0]
                        relative_path = os.path.relpath(root, input_path)
                        save_folder = os.path.join(image_output_dir, relative_path)
                        os.makedirs(save_folder, exist_ok=True)
                        save_path = os.path.join(save_folder, f"{filename_wo_ext}.png")
                        generate_scalogram(samples, wavelet=wavelet_name, save_path=save_path)
                        label = get_label_from_path(root)
                        results.append([save_path, label])
                    except Exception as e:
                        print(f"[X] 스케일로그램 생성 실패: {file}", e)
                else:
                    print(f"[X] waveform 추출 실패: {file}")

    # CSV 저장
    if results:
        with open(csv_output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['image_path', 'label'])  # 헤더
            writer.writerows(results)
        print(f"CSV 저장 완료: {csv_output_path}")
    else:
        print("[X] 처리할 mp3 파일이 없습니다.")

input_path = "./data/07-2_add_label(randomized pick)/02_evaluation"  # mp3가 있는 폴더
image_output_dir = "./scalograms"  # 이미지 저장할 폴더
csv_output_path = "./scalograms/labels.csv"  # 결과 CSV 파일

process_directory_with_scalogram(input_path, image_output_dir, csv_output_path)
