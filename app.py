import subprocess

subprocess.call(['pip', 'install', '--upgrade', 'youtube_dl'])

import streamlit as st
import youtube_dl
from pydub import AudioSegment
from pathlib import Path

st.title("YouTube Playlist to MP3 Converter")

# Formulir untuk URL playlist YouTube
youtube_url = st.text_input("Masukkan URL Playlist YouTube:")
if st.button("Konversi ke MP3"):
    # Fungsi konversi akan dipanggil di sini
    st.write("Memulai konversi...")

    # Fungsi untuk mengunduh playlist
    def download_playlist(url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': False,  # Untuk melihat pesan kesalahan
            'verbose': True,  # Menampilkan informasi verbose
            'noplaylist': False,  # Memastikan bahwa ini adalah playlist
            'extractor_args': f'--extractor-args youtube:tab',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # Fungsi untuk mengonversi audio
    def convert_to_mp3():
        # Ambil semua file audio dalam format lain di folder 'downloads'
        # Ubah setiap file ke format MP3
        for file_path in Path("downloads").glob("*.webm"):
            audio = AudioSegment.from_file(file_path)
            mp3_path = file_path.with_suffix(".mp3")
            audio.export(mp3_path, format="mp3")

    # Fungsi untuk membuat folder 'downloads' jika belum ada
    def create_downloads_folder():
        downloads_path = Path("downloads")
        downloads_path.mkdir(exist_ok=True)

    # Membuat folder 'downloads' jika belum ada
    create_downloads_folder()

    # Mengunduh dan mengonversi playlist
    download_playlist(youtube_url)
    convert_to_mp3()

    st.write("Konversi selesai! MP3 tersimpan di folder 'downloads'.")

