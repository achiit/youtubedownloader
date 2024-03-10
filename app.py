from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

app = Flask(__name__)

def download_video(url, output_path="."):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video
        video_path = os.path.join(output_path, f"{yt.title}.mp4")
        video_stream.download(output_path)

        return True, video_path

    except Exception as e:
        return False, f"An error occurred: {str(e)}"

@app.route('/download', methods=['POST'])
def download_endpoint():
    data = request.get_json()

    if 'link' not in data:
        return jsonify({"error": "Missing 'link' in the request body"}), 400

    video_url = data['link']

    success, response = download_video(video_url)

    if success:
        return send_file(response, as_attachment=True), 200
    else:
        return jsonify({"error": response}), 500

if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0", port=3000)
