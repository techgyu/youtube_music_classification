import yt_dlp

# 재생목록 또는 첫 영상 URL만 포함된 목록
playlist_urls = [
    #1. 힙합
    #'https://youtu.be/Wym_B7-zAJU?si=BLkeYsHB-0ZLmirl',
    #'https://youtu.be/4IMcmqu4mSI?si=JRaQegEa5ekksYfL',
    #'https://youtu.be/mQKlwsJfsEc?si=tb2iNcp76CdepOl8',
    #'https://youtu.be/jvkkMAaQ3d4?si=6Hlw43WD4qiaKGOM',
    #'https://youtu.be/S3b641gs830?si=4QJa097JhXqpx1Hd',
    #2. 트로트
    #'https://youtu.be/0sPdDDHoit0?si=lMmTi9U0Vw3aUAc1',
    #'https://youtu.be/vZh42o3uTXw?si=xXNCg6oljrmDJeId',
    #'https://youtu.be/votbUw48yxY?si=9Tv5g40o0gj85X6-',
    #'https://youtu.be/QB46Q-LCipQ?si=ac8I8bMhzdiri8h9',
    #3. 클래식
    #'https://youtu.be/HdzIP0twVag?si=txv-_BDnwV8gSvaL',
    #'https://youtu.be/0adpqW1_EOE?si=h4XACtsqzNbRd2go',
    #'https://youtu.be/SVjdqRf_w1g?si=ML51BCVTvhi5w86y',
    #'https://youtu.be/7gD3icdreJU?si=pMrHQiVzySqcPnwD',
    #'https://youtu.be/u420qsrNTRQ?si=e6TUGPvN55An9OeY'

    'https://www.youtube.com/watch?v=Hzi6f_RWJ3Y'
]

# yt-dlp 옵션 설정
ydl_opts = {
    'outtmpl': './%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'ignoreerrors': True
}

# yt-dlp 실행
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(playlist_urls)
