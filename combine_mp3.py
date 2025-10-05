import os
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TXXX
import configparser

def combine_mp3_files(directory, output_file, title, artist, album, album_artist, creator):
    # Get a list of all MP3 files in the directory
    mp3_files = [file for file in os.listdir(directory) if file.endswith(".mp3")]

    if not mp3_files:
        print("No MP3 files found in the directory.")
        return

    mp3_files.sort()  # Sort the list of MP3 files

    # Initialize an empty AudioSegment
    combined = AudioSegment.empty()

    # Iterate over MP3 files and append them to the combined AudioSegment
    for mp3_file in mp3_files:
        audio = AudioSegment.from_mp3(os.path.join(directory, mp3_file))
        combined += audio

    # Export the combined AudioSegment as an MP3 file
    combined.export(output_file, format="mp3")
    print(f"Combined MP3 file created: {output_file}")

    # Set ID3 tags for the combined file
    audio_file = EasyID3(output_file)
    audio_file['title'] = title
    audio_file['artist'] = artist
    audio_file['album'] = album
    audio_file['albumartist'] = album_artist
    audio_file.save()

    # Set custom author tag
    id3 = ID3(output_file)
    id3.add(TXXX(encoding=3, desc='creator', text=creator))
    id3.save()

    print("MP3 files combined and tagged successfully!")

def combine_mp3_files_manual(directory, selected_files, output_file, title, artist, album, album_artist, creator):
    # Initialize an empty AudioSegment
    combined = AudioSegment.empty()
    for filename in selected_files:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            audio = AudioSegment.from_mp3(path)
            combined += audio
        else:
            print(f"Warning: {filename} not found in {directory}. Skipped.")
    combined.export(output_file, format="mp3")
    print(f"Combined MP3 file created manually: {output_file}")
    # Set ID3 tags
    audio_file = EasyID3(output_file)
    audio_file['title'] = title
    audio_file['artist'] = artist
    audio_file['album'] = album
    audio_file['albumartist'] = album_artist
    audio_file.save()
    id3 = ID3(output_file)
    id3.add(TXXX(encoding=3, desc='creator', text=creator))
    id3.save()
    print("MP3 files combined manually and tagged successfully!")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('variables.cfg', encoding='utf-8')

    input_directory = config['DEFAULT']['tts_output_dir']
    album_artist = config['DEFAULT']['album_artist']
    creator = config['DEFAULT']['creator']
    album = config['DEFAULT']['album']
    title = config['DEFAULT']['title']
    artist = config['DEFAULT']['artist']
    combined_audio_dir = config['DEFAULT']['combined_audio_dir']
    output_file = os.path.join(combined_audio_dir, f"{artist}_{title}.mp3")

    combine_mp3_files(input_directory, output_file, title, artist, album, album_artist, creator)
    print(f"Output MP3 file: {output_file}")

