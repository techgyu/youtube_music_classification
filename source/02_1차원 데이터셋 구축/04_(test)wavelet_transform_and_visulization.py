#웨이블릿 이해가 안 가서 만든 코드, print문을 통해 웨이블릿의 데이터 형태, 내용물을 확인 가능
import os
import pywt
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

def mp3_to_waveform(mp3_path):
    print(f"[1] MP3 파일 로드 중: {mp3_path}")
    try:
        audio = AudioSegment.from_mp3(mp3_path).set_channels(1) #mp3를 모노 오디오(1채널)로 불러서 audio에 넣음
        print(f"[2] 오디오 길이: {len(audio)} ms, 채널: {audio.channels}, 프레임 레이트: {audio.frame_rate}")
        samples = np.array(audio.get_array_of_samples()).astype(np.float32) #각 샘플링 주파수의 신호 값이 순서대로 들어감. samples[44100]은 1초 지점의 신호 값
        print(f"[3] 샘플 수: {len(samples)}, 샘플 타입: {samples.dtype}")
        print("[3-2] samples 데이터 길이:", len(samples)) #samples는 1차원 데이터로 구성, 1323000 / 44100 = 30초 분량의 오디오가 추출됨
        return samples, audio.frame_rate
    except Exception as e:
        print("[!] mp3_to_waveform 에러:", e)
        return None, None

def wavelet_transform_and_plot(samples, wavelet_name='db4', level=5, output_path="wavelet_plot.png"):
    try:
        print(f"[4] 웨이블릿 변환 시작: wavelet={wavelet_name}, level={level}") #db4로 5레벨로 나눠서 변환
        #coeffs는 여러 개의 벡터 값을 가진 배열
        coeffs = pywt.wavedec(samples, wavelet_name, level=level) #입력된 samples를 웨이블릿 변환하여, level 단계만큼 반복해서 분해함
        print(f"[5] 웨이블릿 계수 레벨 수: {len(coeffs)}")
        print(f"[5-1] 0레벨 웨이블릿 계수 내부 구성 디스플레이: \n{coeffs[0][:100]}") # 가장 낮은 주파수 성분을 가짐: Approximation 계수 (근사 계수)
        print(f"[5-2] 1레벨 웨이블릿 계수 내부 구성 디스플레이: \n{coeffs[1][:100]}")
        print(f"[5-3] 2레벨 웨이블릿 계수 내부 구성 디스플레이: \n{coeffs[2][:100]}")
        print(f"[5-4] 3레벨 웨이블릿 계수 내부 구성 디스플레이: \n{coeffs[3][:100]}")
        print(f"[5-5] 4레벨 웨이블릿 계수 내부 구성 디스플레이: \n{coeffs[4][:100]}") 
        print(f"[5-6] 5레벨 웨이블릿 계수 내부 구성 디스플레이: \n{coeffs[5][:100]}") # 가장 높은 주파수 성분을 가짐: Detail 계수 (세부 계수)
        for i, coef in enumerate(coeffs):
            print(f"   - Level {i} 계수 길이: {len(coef)}")

        # 그래프 시각화
        plt.figure(figsize=(12, 8))
        for i, coef in enumerate(coeffs):
            plt.subplot(len(coeffs), 1, i+1)
            plt.plot(coef)
            plt.title(f"Level {i} {'(Approximation)' if i==0 else f'(Detail {i})'}")
        plt.tight_layout()
        plt.suptitle("Wavelet Decomposition", fontsize=16)
        plt.subplots_adjust(top=0.95)

        plt.savefig(output_path)  # ← 그래프 저장
        print(f"그래프 저장 완료: {output_path}")
        stats = calculate_stats(coeffs)
        print(stats)
    except Exception as e:
        print("[!] wavelet_transform_and_plot 에러:", e)

def calculate_stats(coeffs):
    stats = []
    for i, coef in enumerate(coeffs): #coeffs[0][] ~ coeffs[5][]를 1줄(1레벨)씩 꺼내서 coef에 넣음
        abs_mean = np.mean(np.abs(coef))                  # (1) 절대값의 평균
        mean_square = np.mean(coef**2)                    # (2) 제곱 평균 (에너지)
        std_dev = np.std(coef)                            # (3) 표준편차
        median = np.median(coef)                          # (4) 중앙값

        stats.append({
            'level': i,
            'abs_mean': abs_mean,
            'mean_square': mean_square,
            'std_dev': std_dev,
            'median': median
        })

        print(f"Level {i}: abs_mean={abs_mean:.4f}, mean_square={mean_square:.4f}, std_dev={std_dev:.4f}, median={median:.4f}")
    return stats

# 사용 예시
mp3_path = "./test.mp3"  # ← 실제 MP3 파일 경로를 지정하세요

if os.path.exists(mp3_path):
    print(f"[0] 파일 확인 완료: {mp3_path}")
    waveform, sr = mp3_to_waveform(mp3_path)
    if waveform is not None:
        wavelet_transform_and_plot(waveform, wavelet_name='db4', level=5, output_path="wavelet_result.png")
    else:
        print("[X] waveform 추출 실패")
else:
    print("[X] 파일이 존재하지 않습니다:", mp3_path)

