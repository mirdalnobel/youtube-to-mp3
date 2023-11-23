from flask import Flask, request, jsonify
from pytube import YouTube
from moviepy.editor import VideoFileClip
from pathlib import Path

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    youtube_url = data['youtube_url']

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

    return jsonify({"message": "Conversion complete!"})

if __name__ == '__main__':
    app.run(debug=True)
