# Youtube Music Classification

이 프로젝트는 유튜브에서 음악 영상을 다운로드하고, 오디오 추출, 분할, 웨이블릿 변환, 신호 시각화, CNN 학습 등 음악 분류를 위한 다양한 파이프라인을 제공합니다.

## 주요 기능
- 유튜브 영상 다운로드 (`01_v2.0_YoutubeDownloader_byIndex.py`)
- 영상에서 오디오 추출 및 분할
- 웨이블릿 변환 및 시각화
- 오디오 신호 차트 생성
- CNN 기반 음악 분류 모델 학습

## 폴더 구조
```
source/
    01_v2.0_YoutubeDownloader_byIndex.py   # 유튜브 영상 다운로드
    02_extract_audio_from_video.py.py      # 영상에서 오디오 추출
    03_split_mp3_by_30sec.py               # 오디오 30초 단위 분할
    04_(test)wavelet_transform_and_visulization.py
    05_(no processed)wavelet_transform_and_csv.py
    06_wavelet_transform_and_csv_label.py
    06-1_random_sample_and_split.py
    07_gpu_test.py
    07_train4csv-edited.py
    08_(test)scalergram.py
    09_extract_waveform.py
    10-1_(paused)making_chart.py
    10-2_(paused)making_chart_multicore.py
    11_cnn_by_eggimage_extractor.py
    12-1_making_signal_chart(wave).py
    12-2_making_signal_chart(linear).py
    12-3_making_signal_chart(2D_graphic).py
    cnn_고양이 강아지.py
    matploblib_test.py
    tooleegchart.py
    train4csv-학습예제.py
    wavelet_features.csv
    wavelet_result.png
```

## 설치 및 실행 방법
1. Python 3.8 이상 설치
2. 의존성 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
3. 유튜브 영상 다운로드 예시 실행
   ```bash
   python source/01_v2.0_YoutubeDownloader_byIndex.py
   ```

## 필요 패키지
- yt-dlp: 유튜브 영상 다운로드
- numpy, pandas: 데이터 처리
- librosa: 오디오 신호 처리
- matplotlib: 시각화
- scikit-learn: 머신러닝
- tensorflow/keras: 딥러닝

## 참고
- 각 파이썬 파일의 주석을 참고하여 원하는 기능을 실행하세요.
- 영상 다운로드 시 yt-dlp의 정책 및 유튜브 이용약관을 준수하세요.