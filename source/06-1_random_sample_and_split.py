# 학습률을 올리기 위해 전 처리된 데이터에서 랜덤하게 1024개와 128개를 뽑아내어
# training과 evaluation 으로 나누는 코드
import os
import random # 랜덤 샘플링을 위해(랜덤하게 1024, 128개 뽑아냄)
import shutil

# 원본 mp3 파일들이 있는 디렉토리 경로
source_dir = './data/07_add_label(randomized pick)/trot'  # 예: './mp3_files'
train_dir = './data/07_add_label(randomized pick)/trot/training'    # 예: './train'
eval_dir = './data/07_add_label(randomized pick)/trot/evaluation'  # 예: './evaluation'

# 디렉토리가 없으면 생성
os.makedirs(train_dir, exist_ok=True)
os.makedirs(eval_dir, exist_ok=True)

# .mp3 파일 리스트 얻기
mp3_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.mp3')]
random.shuffle(mp3_files)

# 샘플링
train_samples = mp3_files[:1024] # 1024개를 뽑고
eval_samples = mp3_files[1024:1024+128] # 나머지 중에서 128개를 뽑는다

# 파일 복사 함수
def copy_files(file_list, dest_dir):
    for file_name in file_list:
        src_path = os.path.join(source_dir, file_name)
        dst_path = os.path.join(dest_dir, file_name)
        shutil.copy2(src_path, dst_path)

# 복사 실행
copy_files(train_samples, train_dir)
copy_files(eval_samples, eval_dir)

print(f"Train files copied: {len(train_samples)}")
print(f"Eval files copied: {len(eval_samples)}")
