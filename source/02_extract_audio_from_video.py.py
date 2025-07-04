import os
from moviepy import VideoFileClip

def extract_audio_from_mp4(input_dir, output_dir):
    # 출력 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 하위 디렉토리 포함해서 순회
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".mp4"): # mp4 파일 탐색
                mp4_path = os.path.join(root, file) # mp4 파일 경로 전달

                # 출력 파일 경로 설정 (디렉토리 구조 반영)
                rel_path = os.path.relpath(root, input_dir) # 상대 경로 계산
                out_subdir = os.path.join(output_dir, rel_path) # 출력 디렉토리 경로
                os.makedirs(out_subdir, exist_ok=True) # 출력 디렉토리 생성

                # mp3 파일 이름
                mp3_filename = os.path.splitext(file)[0] + ".mp3" 
                mp3_path = os.path.join(out_subdir, mp3_filename)

                try:
                    print(f"추출 중: {mp4_path}") # mp4 파일 경로 출력
                    video = VideoFileClip(mp4_path) # 비디오 파일 열기
                    video.audio.write_audiofile(mp3_path) # 오디오 추출 및 저장
                    video.close() # 비디오 파일 닫기
                except Exception as e:
                    print(f"오류 발생: {mp4_path}")
                    print(e)

# 사용 예시
#input_directory = "./data/03_Convert_mp4_to_mp3"     # MP4 파일이 있는 폴더 경로
input_directory = "./NA"     # MP4 파일이 있는 폴더 경로
#output_directory = "./data/03_Convert_mp4_to_mp3" # 오디오를 저장할 폴더 경로
output_directory = "./NA" # 오디오를 저장할 폴더 경로
extract_audio_from_mp4(input_directory, output_directory)
