# app.py
import os
import functions
from flask import Flask, render_template, request, jsonify, send_from_directory
from google.cloud import texttospeech
import configparser
from werkzeug.utils import secure_filename
import combine_mp3
from create_mp4 import create_video  # new import
from pydub import AudioSegment

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
    """List all audio files in the TTS output directory sorted by timestamp"""
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(('.mp3', '.wav'))]

    # Sort by Unix timestamp filename (chronological order)
    files.sort(key=lambda x: float(os.path.splitext(x)[0]))

    return jsonify({'files': files})

@app.route('/list_combined_files')
def list_combined_files():
    """List all combined MP3 and WAV files in the work directory"""
    files = [f for f in os.listdir(WORKDIR) if f.endswith(('.mp3', '.wav'))]
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
def combine_files():
    data = request.json
    sorted_files = data.get('sorted_files', [])
    basename = data.get('basename', '')

    if len(sorted_files) < 2:
        return jsonify({'status': 'error', 'message': 'At least two files required'})

    if not basename:
        return jsonify({'status': 'error', 'message': 'Basename is required'})

    # Determine output format based on majority of input files
    mp3_count = sum(1 for f in sorted_files if f.lower().endswith('.mp3'))
    wav_count = sum(1 for f in sorted_files if f.lower().endswith('.wav'))
    output_format = 'mp3'  # if mp3_count >= wav_count else 'wav'

    try:
        # Create an empty audio segment
        combined = AudioSegment.empty()

        # Append each file to the combined segment
        for file in sorted_files:
            file_path = os.path.join(OUTPUT_DIR, file)
            # AudioSegment automatically detects format from file extension
            segment = AudioSegment.from_file(file_path)
            combined += segment

        # Export with chosen format
        output_file = f"{basename}.{output_format}"
        output_path = os.path.join(WORKDIR, output_file)
        combined.export(output_path, format=output_format)

        return jsonify({
            'status': 'success',
            'message': 'Files combined successfully',
            'output_file': output_file
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error combining files: {str(e)}'})


@app.route('/create_video', methods=['POST'])
def create_video_route():
    """Create an MP4 file using a selected combined mp3/wav file and a selected image"""
    data = request.json
    audio_file = data.get('mp3_file')  # Can be either MP3 or WAV file
    image_file = data.get('image_file')
    video_basename = data.get('video_basename', '').strip()
    
    if not audio_file or not image_file:
        return jsonify({'status': 'error', 'message': 'Both audio file and image file must be selected'})
    
    if not video_basename:
        return jsonify({'status': 'error', 'message': 'Please provide a basename for the video output file'})
    
    audio_path = os.path.join(WORKDIR, audio_file)
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
