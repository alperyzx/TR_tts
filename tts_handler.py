# tts_handler.py
import os
import functions
from google.cloud import texttospeech
import configparser

def process_text_to_speech(text):
    """Process text and generate speech files"""
    # Read config
    config = configparser.ConfigParser()
    config.read('variables.cfg', encoding='utf-8')

    # Get TTS parameters
    language_code = config['TTS']['language_code']
    voice_name = config['TTS']['voice_name']
    speaking_rate = float(config['TTS']['speaking_rate'])
    pitch = float(config['TTS']['pitch'])
    volume_gain_db = float(config['TTS']['volume_gain_db'])
    sample_rate_hertz = int(config['TTS']['sample_rate_hertz'])
    output_dir = config['DEFAULT']['tts_output_dir']

    # Process text
    pfirstCheck = functions.firstCheck(text)
    prepParen = functions.repParen(pfirstCheck.lower())
    prepWords = functions.repWords(prepParen)
    pLastcheck = functions.lastCheck(prepWords)
    prepPunct = functions.fixPunct(pLastcheck)
    paddSsml = functions.addSsml(prepPunct)

    # Use paddSsml to generate speech with Google Cloud TTS
    # This assumes your functions module already handles the TTS API calls
    # If not, you'll need to implement the TTS API call here

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Return list of generated files
    files = [f for f in os.listdir(output_dir) if f.endswith('.mp3')]
    files.sort()
    return files