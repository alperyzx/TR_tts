# app.py
import os
import functions
from flask import Flask, render_template, request, jsonify, send_from_directory
from google.cloud import texttospeech
import configparser
from werkzeug.utils import secure_filename
import combine_mp3
from create_mp4 import create_video  # new import

app = Flask(__name__)

# Read config
config = configparser.ConfigParser()
config.read('variables.cfg', encoding='utf-8')

# Get directories from config
OUTPUT_DIR = config['DEFAULT']['tts_output_dir']
WORKDIR = config['DEFAULT']['workdir']

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    """Process submitted text and generate speech"""
    from tts_handler import process_text_to_speech

    if 'text' in request.form:
        text = request.form['text']
    else:
        text = request.files['file'].read().decode('utf-8')

    try:
        files = process_text_to_speech(text)
        return jsonify({
            'status': 'success',
            'message': 'Text processed successfully',
            'files': files
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    # Process text using existing functions
    pfirstCheck = functions.firstCheck(text)
    prepParen = functions.repParen(pfirstCheck.lower())
    prepWords = functions.repWords(prepParen)
    pLastcheck = functions.lastCheck(prepWords)
    prepPunct = functions.fixPunct(pLastcheck)
    paddSsml = functions.addSsml(prepPunct)

    # Call TTS API (assuming your functions module handles this)
    # This should save files to OUTPUT_DIR

    return jsonify({'status': 'success', 'message': 'Text processed successfully'})

@app.route('/list_files')
def list_files():
    """List all MP3 files in the output directory"""
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp3')]
    return jsonify({'files': files})

@app.route('/list_combined_files')
def list_combined_files():
    """List all combined MP3 files in the work directory"""
    files = [f for f in os.listdir(WORKDIR) if f.endswith('.mp3')]
    files.sort()
    return jsonify({'files': files})

@app.route('/list_images')
def list_images():
    """List all image files in the work directory with common extensions"""
    valid_exts = ('.png', '.jpg', '.jpeg', '.gif')
    files = [f for f in os.listdir(WORKDIR) if f.lower().endswith(valid_exts)]
    files.sort()
    return jsonify({'images': files})

@app.route('/list_videos')
def list_videos():
    """List all MP4 files in the work directory"""
    files = [f for f in os.listdir(WORKDIR) if f.endswith('.mp4')]
    files.sort()
    return jsonify({'videos': files})

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve an audio file for playback"""
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/combined_audio/<filename>')
def serve_combined_audio(filename):
    """Serve a combined audio file for playback"""
    return send_from_directory(WORKDIR, filename)

@app.route('/combine', methods=['POST'])
def combine():
    """Combine selected MP3 files in the order provided by the user drag-sort"""
    # Expecting sorted list and basename from the UI
    sorted_files = request.json.get('sorted_files', [])
    basename = request.json.get('basename', '').strip()
    if not sorted_files:
        return jsonify({'status': 'error', 'message': 'No files selected'})
    if not basename:
        return jsonify({'status': 'error', 'message': 'Please provide a basename for the output file'})
    
    # Use values from config
    album_artist = config['DEFAULT']['album_artist']
    creator = config['DEFAULT']['creator']
    album = config['DEFAULT']['album']
    title = config['DEFAULT']['title']
    artist = config['DEFAULT']['artist']

    output_file = os.path.join(WORKDIR, f"{basename}.mp3")
    
    # Call the combine function with the user's sorted file order
    combine_mp3.combine_mp3_files_manual(OUTPUT_DIR, sorted_files, output_file, title, artist, album, album_artist, creator)

    return jsonify({
        'status': 'success',
        'message': 'Files combined successfully',
        'output_file': output_file
    })

@app.route('/create_video', methods=['POST'])
def create_video_route():
    """Create an MP4 file using a selected combined mp3 file and a selected image"""
    data = request.json
    mp3_file = data.get('mp3_file')
    image_file = data.get('image_file')
    video_basename = data.get('video_basename', '').strip()
    
    if not mp3_file or not image_file:
        return jsonify({'status': 'error', 'message': 'Both mp3 file and image file must be selected'})
    
    if not video_basename:
        return jsonify({'status': 'error', 'message': 'Please provide a basename for the video output file'})
    
    audio_path = os.path.join(WORKDIR, mp3_file)
    image_path = os.path.join(WORKDIR, image_file)
    
    try:
        output_file = create_video(image_path=image_path, audio_path=audio_path, video_basename=video_basename)
        return jsonify({'status': 'success', 'message': 'MP4 file created successfully', 'output_file': output_file})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve an image file"""
    return send_from_directory(WORKDIR, filename)

@app.route('/videos/<path:filename>')
def serve_video_file(filename):
    """Serve a video file"""
    return send_from_directory(WORKDIR, filename)

if __name__ == '__main__':
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    app.run(debug=True)

