# app.py
import os
import functions
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from google.cloud import texttospeech
import configparser
from werkzeug.utils import secure_filename
import combine_mp3
from create_mp4 import create_video  # new import
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Read config
config = configparser.ConfigParser()
config.read('variables.cfg', encoding='utf-8')

# Get directories from config
WORKDIR = config['DEFAULT']['workdir']
PICTURES_DIR = config['DEFAULT']['pictures']
OUTPUT_DIR = config['DEFAULT']['tts_output_dir']
COMBINED_AUDIO_DIR = config['DEFAULT']['combined_audio_dir']
VIDEOS_DIR = config['DEFAULT']['videos_dir']

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
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(('.mp3', '.wav', '.m4a'))]

    # Sort by Unix timestamp filename (chronological order)
    files.sort(key=lambda x: float(os.path.splitext(x)[0]))

    return jsonify({'files': files})

@app.route('/list_combined_files')
def list_combined_files():
    """List all combined MP3 and WAV files in the combined audio directory"""
    files = [f for f in os.listdir(COMBINED_AUDIO_DIR) if f.endswith(('.mp3', '.wav', '.m4a'))]
    files.sort()
    return jsonify({'files': files})

@app.route('/list_images')
def list_images():
    """List all image files in the pictures directory with common extensions"""
    valid_exts = ('.png', '.jpg', '.jpeg', '.gif')
    files = [f for f in os.listdir(PICTURES_DIR) if f.lower().endswith(valid_exts)]
    files.sort()
    return jsonify({'images': files})

@app.route('/list_videos')
def list_videos():
    """List all MP4 files in the videos directory"""
    files = [f for f in os.listdir(VIDEOS_DIR) if f.endswith('.mp4')]
    files.sort()
    return jsonify({'videos': files})

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve an audio file for playback"""
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/combined_audio/<filename>')
def serve_combined_audio(filename):
    """Serve a combined audio file for playback"""
    return send_from_directory(COMBINED_AUDIO_DIR, filename)


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
    m4a_count = sum(1 for f in sorted_files if f.lower().endswith('.m4a'))
    output_format = 'mp3'  # Default to mp3, could be enhanced to choose based on majority

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
        output_path = os.path.join(COMBINED_AUDIO_DIR, output_file)
        combined.export(output_path, format=output_format)

        return jsonify({
            'status': 'success',
            'message': 'Files combined successfully',
            'output_file': output_file
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error combining files: {str(e)}'})


@app.route('/combine_combined_files', methods=['POST'])
def combine_combined_files():
    """Combine selected files in COMBINED_AUDIO_DIR and save the result in COMBINED_AUDIO_DIR"""
    data = request.get_json()
    sorted_files = data.get('sorted_files', [])
    basename = data.get('basename', '')

    if len(sorted_files) < 2:
        return jsonify({'status': 'error', 'message': 'At least two files required'})
    if not basename:
        return jsonify({'status': 'error', 'message': 'Basename is required'})

    # Determine output format based on majority of input files
    mp3_count = sum(1 for f in sorted_files if f.lower().endswith('.mp3'))
    wav_count = sum(1 for f in sorted_files if f.lower().endswith('.wav'))
    m4a_count = sum(1 for f in sorted_files if f.lower().endswith('.m4a'))
    output_format = 'mp3'  # Default to mp3, could be enhanced to choose based on majority

    try:
        combined = AudioSegment.empty()
        for file in sorted_files:
            file_path = os.path.join(COMBINED_AUDIO_DIR, file)
            segment = AudioSegment.from_file(file_path)
            combined += segment
        output_file = f"{basename}.{output_format}"
        output_path = os.path.join(COMBINED_AUDIO_DIR, output_file)
        combined.export(output_path, format=output_format)
        return jsonify({'status': 'success', 'message': 'Files combined successfully', 'output_file': output_file})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error combining files: {str(e)}'})


@app.route('/create_video', methods=['POST'])
def create_video_route():
    """Create an MP4 file using a selected combined audio file and a selected image"""
    data = request.json
    audio_file = data.get('mp3_file')  # Can be MP3, WAV, or M4A file
    image_file = data.get('image_file')
    video_basename = data.get('video_basename', '').strip()
    
    if not audio_file or not image_file:
        return jsonify({'status': 'error', 'message': 'Both audio file and image file must be selected'})
    
    if not video_basename:
        return jsonify({'status': 'error', 'message': 'Please provide a basename for the video output file'})
    
    audio_path = os.path.join(COMBINED_AUDIO_DIR, audio_file)
    image_path = os.path.join(PICTURES_DIR, image_file)

    try:
        output_file = create_video(image_path=image_path, audio_path=audio_path, video_basename=video_basename, videos_dir=VIDEOS_DIR)
        return jsonify({'status': 'success', 'message': 'MP4 file created successfully', 'output_file': output_file})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve an image file from the pictures directory"""
    return send_from_directory(PICTURES_DIR, filename)

@app.route('/videos/<path:filename>')
def serve_video_file(filename):
    """Serve a video file"""
    return send_from_directory(VIDEOS_DIR, filename)

@app.route('/delete_files', methods=['POST'])
def delete_files():
    """Delete selected audio files from the output directory"""
    data = request.get_json()
    files = data.get('files', [])
    deleted = []
    errors = []
    for filename in files:
        # Only allow deletion of .mp3, .wav, or .m4a in OUTPUT_DIR
        if not (filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.m4a')):
            errors.append(f"Invalid file type: {filename}")
            continue
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                deleted.append(filename)
            except Exception as e:
                errors.append(f"Error deleting {filename}: {str(e)}")
        else:
            errors.append(f"File not found: {filename}")
    if errors:
        return jsonify({'status': 'error', 'message': '; '.join(errors), 'deleted': deleted})
    return jsonify({'status': 'success', 'message': f"Deleted {len(deleted)} file(s)", 'deleted': deleted})

@app.route('/delete_combined_files', methods=['POST'])
def delete_combined_files():
    """Delete selected combined audio files from the combined audio directory"""
    data = request.get_json()
    files = data.get('files', [])
    deleted = []
    errors = []
    for filename in files:
        # Only allow deletion of .mp3, .wav, or .m4a in COMBINED_AUDIO_DIR
        if not (filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.m4a')):
            errors.append(f"Invalid file type: {filename}")
            continue
        file_path = os.path.join(COMBINED_AUDIO_DIR, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                deleted.append(filename)
            except Exception as e:
                errors.append(f"Error deleting {filename}: {str(e)}")
        else:
            errors.append(f"File not found: {filename}")
    if errors:
        return jsonify({'status': 'error', 'message': '; '.join(errors), 'deleted': deleted})
    return jsonify({'status': 'success', 'message': f"Deleted {len(deleted)} file(s)", 'deleted': deleted})

@app.route('/delete_videos', methods=['POST'])
def delete_videos():
    """Delete selected video files from the videos directory"""
    data = request.get_json()
    files = data.get('files', [])
    deleted = []
    errors = []
    for filename in files:
        if not filename.endswith('.mp4'):
            errors.append(f"Invalid file type: {filename}")
            continue
        file_path = os.path.join(VIDEOS_DIR, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                deleted.append(filename)
            except Exception as e:
                errors.append(f"Error deleting {filename}: {str(e)}")
        else:
            errors.append(f"File not found: {filename}")
    if errors and not deleted:
        return jsonify({'status': 'error', 'message': '; '.join(errors)})
    elif errors:
        return jsonify({'status': 'success', 'message': f"Some videos deleted: {', '.join(deleted)}. Errors: {'; '.join(errors)}"})
    else:
        return jsonify({'status': 'success', 'message': f"Deleted {len(deleted)} video(s) successfully."})

@app.route('/upload_combined_files', methods=['POST'])
def upload_combined_files():
    """Handle upload of MP3/WAV/M4A files to COMBINED_AUDIO_DIR for Combined Audio Files section"""
    if 'files' not in request.files and not request.files:
        # For fetch+FormData, files may be in request.files as a MultiDict
        files = request.files.getlist('files')
    else:
        files = request.files.getlist('files')
    if not files:
        return jsonify({'status': 'error', 'message': 'No files uploaded.'})
    saved = []
    errors = []
    for file in files:
        filename = secure_filename(file.filename)
        if not (filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.m4a')):
            errors.append(f"Invalid file type: {filename}")
            continue
        save_path = os.path.join(COMBINED_AUDIO_DIR, filename)
        try:
            file.save(save_path)
            saved.append(filename)
        except Exception as e:
            errors.append(f"Error saving {filename}: {str(e)}")
    if errors and not saved:
        return jsonify({'status': 'error', 'message': '; '.join(errors)})
    elif errors:
        return jsonify({'status': 'success', 'message': f"Some files uploaded: {', '.join(saved)}. Errors: {'; '.join(errors)}"})
    else:
        return jsonify({'status': 'success', 'message': f"Uploaded {len(saved)} file(s) successfully."})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Handle upload of image files to PICTURES_DIR for Select Image for Video section"""
    if 'files' not in request.files and not request.files:
        files = request.files.getlist('files')
    else:
        files = request.files.getlist('files')
    if not files:
        return jsonify({'status': 'error', 'message': 'No files uploaded.'})
    saved = []
    errors = []
    valid_exts = ('.png', '.jpg', '.jpeg', '.gif')
    for file in files:
        filename = secure_filename(file.filename)
        if not filename.lower().endswith(valid_exts):
            errors.append(f"Invalid file type: {filename}")
            continue
        save_path = os.path.join(PICTURES_DIR, filename)
        try:
            file.save(save_path)
            saved.append(filename)
        except Exception as e:
            errors.append(f"Error saving {filename}: {str(e)}")
    if errors and not saved:
        return jsonify({'status': 'error', 'message': '; '.join(errors)})
    elif errors:
        return jsonify({'status': 'success', 'message': f"Some images uploaded: {', '.join(saved)}. Errors: {'; '.join(errors)}"})
    else:
        return jsonify({'status': 'success', 'message': f"Uploaded {len(saved)} image(s) successfully."})

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    
    # Ensure output directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(COMBINED_AUDIO_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    app.run(host=args.host, port=args.port, debug=True)
