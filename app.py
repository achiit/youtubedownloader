from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

def download_video(url, output_path="."):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video
        video_stream.download(output_path)

        return True, "Download complete!"

    except Exception as e:
        return False, f"An error occurred: {str(e)}"

@app.route('/download', methods=['POST'])
def download_endpoint():
    data = request.get_json()

    if 'link' not in data:
        return jsonify({"error": "Missing 'link' in the request body"}), 400

    video_url = data['link']

    success, message = download_video(video_url)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 500

if __name__ == "__main__":
    app.run(debug=True)
