from flask import Flask, request, redirect
import yt_dlp
import os

app = Flask(__name__)

# Letöltési mappa a C:\Users\Mate\Desktop\Zene
DOWNLOAD_FOLDER = r'C:\Users\Mate\Desktop\Zene'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/request", methods=["POST"])
def handle_request():
    url = request.form.get("url")
    if not url:
        return "Hiányzó URL", 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt', # Ha szükséges, cookie-kat is használhatunk
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
