# 1회성으로 wavelet 변환을 적용하고, 특징을 추출하여 CSV로 저장하는 스크립트, 코드에 사용하지 않음(no processed))
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
        audio = AudioSegment.from_mp3(mp3_path).set_channels(1) # 모노로 변환
        samples = np.array(audio.get_array_of_samples()).astype(np.float32) # 정규화 처리
        return samples, audio.frame_rate # 샘플(배열)과 샘플링 레이트(44100) 반환
    except Exception as e:
        print("[!] mp3_to_waveform 에러:", e)
        return None, None

# Wavelet 변환 받은 걸 이용해서 4가지 특징 추출
# 절대 평균, 제곱 평균, 표준 편차, 중앙값
# 각 레벨별로 계산하여 리스트로 반환
def calculate_stats(coeffs):
    stats = []
    for i, coef in enumerate(coeffs): # 각 레벨의 계수(배열)에 대해
        abs_mean = np.mean(np.abs(coef)) # 절대 평균
        mean_square = np.mean(coef**2) # 제곱 평균
        std_dev = np.std(coef) # 표준 편차
        median = np.median(coef) # 중앙값

        stats.extend([abs_mean, mean_square, std_dev, median]) # 각 특징을 리스트에 추가(나중에 csv에 넣을 거임)
    return stats

# Wavelet 변환을 적용하여 특징 추출
def extract_wavelet_features(samples, wavelet_name='db4', level=5): # wavelet_name: 'db4' (Daubechies 4) 등 다양한 웨이블릿 사용 가능
    try:
        coeffs = pywt.wavedec(samples, wavelet_name, level=level) # 웨이블릿 변환 적용
        stats = calculate_stats(coeffs) # 각 레벨별로 특징 계산
        return stats
    except Exception as e:
        print("[!] extract_wavelet_features 에러:", e)
        return None

# 디렉토리 내의 모든 mp3 파일을 처리하고, 특징을 추출하여 CSV로 저장
def process_directory(input_path, csv_output_path="wavelet_features.csv", wavelet_name='db4', level=5):
    results = []
    for root, dirs, files in os.walk(input_path):
        files.sort(key=natural_key)  # ← 자연 정렬 추가
        for file in files:
            if file.lower().endswith('.mp3'):
                    full_path = os.path.join(root, file)
                    print(f"처리 중: {full_path}")
                    samples, sr = mp3_to_waveform(full_path)
                    if samples is not None:
                        features = extract_wavelet_features(samples, wavelet_name, level)
                        if features is not None:
                            filename_without_ext = os.path.splitext(file)[0]
                            results.append([filename_without_ext] + features)
                        else:
                            print(f"[X] 특징 추출 실패: {file}")
                    else:
                        print(f"[X] waveform 추출 실패: {file}")

    # CSV 저장
    if results:
        header = ["filename"]
        for i in range(level + 1):  # level=5 이면 0~5 레벨
            for stat in ['abs_mean', 'mean_square', 'std_dev', 'median']:
                header.append(f"L{i}_{stat}")

        with open(csv_output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(results)
        print(f"CSV 저장 완료: {csv_output_path}")
    else:
        print("[X] 처리할 mp3 파일이 없습니다.")

# 사용 예시
input_path = "./data/05_wavelet_transform_and_csv"  # 여기에 실제 mp3 파일들이 있는 최상위 디렉토리 경로를 입력하세요
process_directory(input_path)
