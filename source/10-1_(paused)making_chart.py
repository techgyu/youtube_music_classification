# tooleegchart.py 수정 보안
# 가능하면 그대로 코드 사용
# 근데 싱글 코어로 하면 너무 느려서 멀티 코어로 처리하였음(10-2)
import os
import numpy as np
import matplotlib.pyplot as plt
import re

def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def process_single_eeg_file(txt_path):
    eeg_width = 189000  # 데이터 가져온 거 얼마로 자를지(44100 * 30의 약수)
    eeg_data = []

    eeg_result_x = []
    eeg_result_y = []

    with open(txt_path, "r") as eeg_file:
        for line_data in eeg_file:
            eeg_data.append(abs(float(line_data.strip())))

    np_eeg_data = np.array(eeg_data)
    output_dir = os.path.join(os.path.dirname(txt_path), "eegImages")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(txt_path))[0]
    print(f"\n처리 시작: {base_name} ({len(np_eeg_data)} samples)")

    chunk_count = len(np_eeg_data) // eeg_width
    for i in range(chunk_count):
        eeg_width_data = np_eeg_data[(i * eeg_width):(i + 1) * eeg_width]

        eeg_result_x.clear()
        eeg_result_y.clear()

        for j in range(0, len(eeg_width_data), 100):
            if j + 1 < len(eeg_width_data):
                eeg_result_x.append(eeg_width_data[j])
                eeg_result_y.append(eeg_width_data[j + 1])

        point_count = len(eeg_result_x)
        print(f"  ├─ 청크 {i+1}/{chunk_count} → 포인트 {point_count}개")

        plt.scatter(eeg_result_x, eeg_result_y)
        save_path = os.path.join(output_dir, f"{base_name}_{i}.png")
        plt.savefig(save_path, dpi=600)
        plt.clf()
        print(f"  └─ 저장 완료: {save_path}")

    print(f"완료: {base_name} → 총 {chunk_count}개 이미지 생성")

def process_all_eeg_txt_files(root_directory):
    for root, _, files in os.walk(root_directory):
        files = [f for f in files if f.lower().endswith('.txt')]
        files.sort(key=natural_key)

        for file in files:
            full_path = os.path.join(root, file)
            try:
                process_single_eeg_file(full_path)
            except Exception as e:
                print(f"[X] 오류 발생: {full_path} → {e}")

# 시작 디렉토리
process_all_eeg_txt_files('./data/temp/02_evaluation')
