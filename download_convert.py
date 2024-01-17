from pytube import YouTube
from moviepy.editor import VideoFileClip

# 1. Скачивание видео с YouTube
def download_video(youtube_url, output_path='./'):
    yt = YouTube(youtube_url)
    video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
    video_stream.download(output_path)
    return video_stream.default_filename

# 2. Преобразование видео в MP3
def convert_to_mp3(video_path, output_path='./'):
    video = VideoFileClip(video_path)
    audio = video.audio
    mp3_output_path = f"{output_path}{video_path[:-4]}.mp3"
    audio.write_audiofile(mp3_output_path)
    return mp3_output_path

# Пример использования
youtube_url = 'https://youtu.be/oCXNBscuy0w?si=X-cY9m9k3VRYAEkA'
video_filename = download_video(youtube_url)
mp3_filename = convert_to_mp3(video_filename)

print(f"Видео успешно скачано: {video_filename}")
print(f"Аудио успешно преобразовано в MP3: {mp3_filename}")
