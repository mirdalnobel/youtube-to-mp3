import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
from pathlib import Path

# Fungsi untuk mengonversi video YouTube ke MP3
def convert(youtube_url):
    # Download playlist
    playlist = YouTube(youtube_url)
    for video in playlist.video_urls:
        yt = YouTube(video)
        ys = yt.streams.filter(only_audio=True).first()
        ys.download('downloads')

    # Convert to MP3
    for video_path in Path("downloads").glob("*.webm"):
        clip = VideoFileClip(video_path)
        mp3_path = video_path.with_suffix(".mp3")
        clip.audio.write_audiofile(mp3_path)
        clip.close()

    return mp3_path

# Streamlit UI
st.title("YouTube to MP3 Converter")

# Mendapatkan URL YouTube dari pengguna
youtube_url = st.text_input("Masukkan URL YouTube:")

if st.button("Konversi"):
    if youtube_url:
        st.info("Sedang mengonversi... Ini mungkin memakan waktu beberapa saat.")
        mp3_path = convert(youtube_url)
        st.success(f"Konversi selesai! File MP3 tersimpan di {mp3_path}")
