import os
from pydub import AudioSegment

def split_mp3_files(input_dir, output_dir, chunk_length_ms=30_000):
    # 출력 폴더 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 하위 디렉토리 포함해서 순회
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.mp3'): # mp3 파일 탐색
                file_path = os.path.join(root, file) # mp3 파일 경로 전달
                audio = AudioSegment.from_mp3(file_path) # mp3 파일 로드

                # 출력 파일 경로 설정 (디렉토리 구조 반영)
                rel_path = os.path.relpath(root, input_dir) # 상대 경로 계산
                out_subdir = os.path.join(output_dir, rel_path) # 출력 디렉토리 경로
                os.makedirs(out_subdir, exist_ok=True) # 출력 디렉토리 생성
                # 파일 이름에서 확장자 제거
                base_name = os.path.splitext(file)[0]
                total_length = len(audio) # 오디오 길이 (ms 단위)
                num_chunks = (total_length + chunk_length_ms - 1) // chunk_length_ms # 올림 연산으로 청크 수 계산

                for i in range(num_chunks): # 청크 단위로 나누기
                    start = i * chunk_length_ms
                    end = min(start + chunk_length_ms, total_length) # 청크의 끝 위치 계산
                    chunk = audio[start:end]

                    chunk_filename = f"{base_name}_{i+1}.mp3" # 청크 파일 이름 생성
                    chunk_path = os.path.join(out_subdir, chunk_filename) # 청크 파일 경로 설정
                    chunk.export(chunk_path, format="mp3") # mp3로 저장
                    print(f"저장 완료: {chunk_path}")

# 사용 예시
# input_dir = "./data/04_Split_mp3_by_30sec"     # mp3 파일이 있는 폴더
input_dir = "./NA"     # mp3 파일이 있는 폴더
# output_dir = "./data/04_Split_mp3_by_30sec"    # 자른 mp3 저장할 폴더
output_dir = "./NA" # 자른 mp3 저장할 폴더
split_mp3_files(input_dir, output_dir)
