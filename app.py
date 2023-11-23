import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip

st.title("YouTube Playlist to MP3 Converter")

# Formulir untuk URL playlist YouTube
youtube_url = st.text_input("Masukkan URL Playlist YouTube:")
if st.button("Konversi ke MP3"):
    # Fungsi konversi akan dipanggil di sini
    st.write("Memulai konversi...")

    # Fungsi untuk mengunduh playlist
    def download_playlist(url):
        playlist = YouTube(url)
        for video in playlist.video_urls:
            st.write(f"Downloading: {video}")
            yt = YouTube(video)
            ys = yt.streams.filter(only_audio=True).first()
            ys.download('downloads')

    # Fungsi untuk mengonversi video ke MP3
    def convert_to_mp3():
        for video_path in Path("downloads").glob("*.webm"):
            clip = VideoFileClip(video_path)
            mp3_path = video_path.with_suffix(".mp3")
            clip.audio.write_audiofile(mp3_path)
            clip.close()

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
