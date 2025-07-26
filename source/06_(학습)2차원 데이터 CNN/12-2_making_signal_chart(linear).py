# 2차시에 앞 전에서 이야기 했던 음성 신호 그래프 만들고, peak 뽑아서 처리하려고 했었지만!
# 파동 그래프의 피크가 추출되는 그래프가 나와버렸다
import librosa
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

def extract_peaks_from_audio(file_path, duration=30, smoothing_window=101, distance=1000, prominence=0.02):
    """
    MP3 파일에서 첨점(peak) 추출하여 꺾은선 그래프 그리기 (SIM + PSR)
    
    Parameters:
        file_path (str): MP3 파일 경로
        duration (int): 로딩할 초 단위 오디오 길이
        smoothing_window (int): 이동 평균 윈도우 길이
        distance (int): 첨점 간 최소 거리 (샘플 단위)
        prominence (float): 첨점의 눈에 띄는 정도 (0~1)
    """
    # Step 1: Load MP3
    y, sr = librosa.load(file_path, duration=duration)

    # Step 2: Normalize (optional but common)
    y = y / np.max(np.abs(y))

    # Step 3: Smooth the signal using Savitzky-Golay filter (이동평균 느낌)
    y_smooth = scipy.signal.savgol_filter(y, window_length=smoothing_window, polyorder=3)

    # Step 4: Find peaks using SIM-like logic
    peaks, _ = scipy.signal.find_peaks(y_smooth, distance=distance, prominence=prominence)

    # Step 5: Plot signal and peaks
    plt.figure(figsize=(14, 5))
    plt.plot(y_smooth, label='Smoothed Signal')
    plt.plot(peaks, y_smooth[peaks], "x", label='Peaks')

    # Annotate peaks (최대 10개만 표시)
    for i, p in enumerate(peaks[:10]):
        plt.annotate(f"첨점{i+1}", (p, y_smooth[p]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title("SIM 기반 첨점 추출 그래프")
    plt.xlabel("Time (samples)")
    plt.ylabel("Signal Magnitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 사용 예시 (파일 경로 직접 지정)
extract_peaks_from_audio("./data/temp/c_01_1.mp3")