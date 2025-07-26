# 2차시에 앞 전에서 이야기 했던 음성 신호 그래프 만들고, peak 뽑아서 처리하려고 했었지만!
# 파동 그래프가 나와버렸다
import os
import numpy as np
import matplotlib.pyplot as plt
import re

def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def process_waveform_files(root_directory):
    # 저장할 디렉토리 생성
    output_dir = os.path.join(root_directory, 'waveform_plots')
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(root_directory):
        files = [f for f in files if f.lower().endswith('.txt')]
        files.sort(key=natural_key)

        for file in files:
            full_path = os.path.join(root, file)
            try:
                # txt 파일에서 waveform 데이터 읽기
                with open(full_path, 'r') as f:
                    data = f.read().split()
                    waveform = np.array(data, dtype=np.float32)

                # 데이터 다운샘플링 (선형 그래프를 위해)
                downsample_factor = 100  # 데이터 포인트 수 조절
                waveform_downsampled = waveform[::downsample_factor]
                
                # 샘플링 레이트 및 시간축 생성 (44100Hz, 30초)
                sr = 44100
                duration = len(waveform_downsampled) * downsample_factor / sr
                time = np.linspace(0, duration, len(waveform_downsampled))

                # 선형 그래프 시각화
                plt.figure(figsize=(15, 4))
                plt.plot(time, waveform_downsampled, 'b-', linewidth=1)  # 선형 그래프
                plt.xlabel('Time (seconds)')
                plt.ylabel('Signal Magnitude')
                plt.title(f'Waveform Visualization - {os.path.basename(file)}')
                plt.grid(True)
                plt.tight_layout()

                # 그래프 저장
                output_path = os.path.join(output_dir, f'{os.path.splitext(file)[0]}_waveform_linear.png')
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                print(f"[O] 저장 완료: {output_path}")
                
            except Exception as e:
                print(f"[X] 오류 발생: {full_path} → {e}")

# 시작 디렉토리
process_waveform_files('./data/temp')