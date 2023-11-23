import streamlit as st
import subprocess
from pathlib import Path
from pydub import AudioSegment

st.title("YouTube Playlist to MP3 Converter")

# Formulir untuk URL playlist YouTube
youtube_url = st.text_input("Masukkan URL Playlist YouTube:")
if st.button("Konversi ke MP3"):
    # Fungsi konversi akan dipanggil di sini
    st.write("Memulai konversi...")

    # Menjalankan skrip setup.sh untuk instalasi dependensi
    subprocess.call('./setup.sh', shell=True)

    # Fungsi untuk mengunduh playlist
    def download_playlist(url):
        import youtube_dl
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
        from pydub import AudioSegment
        # Ambil semua file audio dalam format lain di folder 'downloads'
        # Ubah setiap file ke format MP3
        for file_path in Path("downloads").glob("*.webm"):
            audio = AudioSegment.from_file(file_path)
            mp3_path = file_path.with_suffix(".mp3")
            audio.export(mp3_path, format="mp3")

    # Fungsi untuk membuat folder 'downloads' jika belum ada
    def create_downloads_folder():
        downloads_path = Path("downloads")

        # Pastikan folder 'downloads' sudah ada
        if not downloads_path.exists():
            downloads_path.mkdir()

    # Membuat folder 'downloads' jika belum ada
    create_downloads_folder()

    # Mengunduh dan mengonversi playlist
    download_playlist(youtube_url)
    convert_to_mp3()

    st.write("Konversi selesai! MP3 tersimpan di folder 'downloads'.")

    # Menampilkan tautan untuk mengunduh setiap file MP3
    st.write("Unduh file MP3:")
    for mp3_file in Path("downloads").glob("*.mp3"):
        st.markdown(f"[{mp3_file.name}]({mp3_file.as_uri()})", unsafe_allow_html=True)
