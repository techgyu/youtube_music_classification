# eggchart로 만들려고 waveform을 추출해서 txt 파일에 개행문자(\n) 넣으면서 저장한 코드
# 앞 전에 이미 웨이블릿 변환하기 직전에 나오는 형태를 txt로만 옮긴 것임
# 교수님 코드는 원래 Z_ALL.txt로 저장
import os
import numpy as np
from pydub import AudioSegment
import re

def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def mp3_to_waveform(mp3_path):
    print(f"[1] MP3 파일 로드 중: {mp3_path}")
    try:
        audio = AudioSegment.from_mp3(mp3_path).set_channels(1)
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        return samples
    except Exception as e:
        print("[!] mp3_to_waveform 에러:", e)
        return None

def save_waveform_to_txt(waveform, output_txt_path):
    try:
        with open(output_txt_path, "w") as f:
            for sample in waveform:
                f.write(f"{sample}\n")
    except Exception as e:
        print("[!] save_waveform_to_txt 에러:", e)

def process_directory_and_save_waveforms(input_path, output_txt_dir):
    os.makedirs(output_txt_dir, exist_ok=True)

    for root, dirs, files in os.walk(input_path):
        files.sort(key=natural_key)
        for file in files:
            if file.lower().endswith('.mp3'):
                full_path = os.path.join(root, file)
                print(f"🎵 처리 중: {full_path}")
                samples = mp3_to_waveform(full_path)
                if samples is not None:
                    filename_without_ext = os.path.splitext(file)[0]
                    txt_path = os.path.join(output_txt_dir, f"{filename_without_ext}.txt")
                    save_waveform_to_txt(samples, txt_path)
                else:
                    print(f"[X] waveform 추출 실패: {file}")

# 사용 예시
input_path = "./data/temp/01_training"  # MP3 파일들이 있는 폴더
output_txt_dir = "./data/temp/01_training"       # .txt 파일이 저장될 폴더

process_directory_and_save_waveforms(input_path, output_txt_dir)
