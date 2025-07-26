import os # 디렉토리 탐색
import pywt # 웨이블릿 변환
import numpy as np
from pydub import AudioSegment # mp3 파일 로딩
import csv # CSV 파일 저장
import re # 자연 정렬(디렉토리 탐색)

# 자연 정렬을 위한 함수
# 숫자가 포함된 문자열을 자연스럽게 정렬
def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)] # 정규 표현식으로 숫자와 문자를 분리하여 리스트 반환

# MP3 파일을 Waveform으로 변환하고, Wavelet 변환을 적용하여 특징을 추출한 후 CSV로 저장
def mp3_to_waveform(mp3_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path).set_channels(1)
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        return samples, audio.frame_rate
    except Exception as e:
        print("[!] mp3_to_waveform 에러:", e)
        return None, None

# Wavelet 변환 받은 걸 이용해서 4가지 특징 추출
def calculate_stats(coeffs):
    stats = []
    for i, coef in enumerate(coeffs):
        abs_mean = np.mean(np.abs(coef))
        mean_square = np.mean(coef**2)
        std_dev = np.std(coef)
        median = np.median(coef)
        stats.extend([abs_mean, mean_square, std_dev, median])
    return stats

# Wavelet 변환을 적용하여 특징 추출
def extract_wavelet_features(samples, wavelet_name='db4', level=5):
    try:
        coeffs = pywt.wavedec(samples, wavelet_name, level=level)
        stats = calculate_stats(coeffs)
        return stats
    except Exception as e:
        print("[!] extract_wavelet_features 에러:", e)
        return None

# classic, hiphop, trot 임에 따라 레이블 반환
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

# 라벨 저장
def process_directory(input_path, csv_output_path=None, wavelet_name='db4', level=5):
    if csv_output_path is None:
        csv_output_path = f"{input_path}/label.csv"
    results = []
    for root, dirs, files in os.walk(input_path):
        files.sort(key=natural_key)
        for file in files:
            if file.lower().endswith('.mp3'):
                full_path = os.path.join(root, file)
                print(f"처리 중: {full_path}")
                samples, sr = mp3_to_waveform(full_path)
                if samples is not None:
                    features = extract_wavelet_features(samples, wavelet_name, level)
                    if features is not None:
                        label = get_label_from_path(root)
                        results.append(features + [label])  # 파일명 제거
                    else:
                        print(f"[X] 특징 추출 실패: {file}")
                else:
                    print(f"[X] waveform 추출 실패: {file}")

    # CSV 저장
    if results:
        with open(csv_output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(results)
        print(f"CSV 저장 완료: {csv_output_path}")
    else:
        print("[X] 처리할 mp3 파일이 없습니다.")

# 사용 예시
input_path = "./data//07-2_add_label(randomized pick)/02_evaluation"  # 최상위 mp3 경로
process_directory(input_path)
