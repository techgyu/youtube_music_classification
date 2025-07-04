#10-1 코드를 멀티 코어로 처리하여 엄청 빠름
import os
import numpy as np
import matplotlib.pyplot as plt
import re
import multiprocessing
from functools import partial

def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def process_single_eeg_file(txt_path, eeg_width=189000):
    eeg_data = []
    eeg_result_x = []
    eeg_result_y = []

    try:
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

    except Exception as e:
        print(f"[X] 오류 발생: {txt_path} → {e}")

def process_all_eeg_txt_files(root_directory, num_workers=None):
    txt_files = []
    for root, _, files in os.walk(root_directory):
        files = [f for f in files if f.lower().endswith('.txt')]
        files.sort(key=natural_key)
        txt_files.extend([os.path.join(root, f) for f in files])

    print(f"\n총 {len(txt_files)}개 파일 발견")

    # 병렬 처리
    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.map(process_single_eeg_file, txt_files)

# ▶시작
if __name__ == '__main__':# 멀티프로세싱할 때 필수
    multiprocessing.set_start_method("spawn", force=True)  # Windows/macOS 대응
    process_all_eeg_txt_files('./data/temp/01_training', num_workers=os.cpu_count())
