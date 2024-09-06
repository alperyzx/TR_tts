import os
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TXXX

def combine_mp3_files(directory, output_file, title, artist, album):
    # Get a list of all MP3 files in the directory
    mp3_files = [file for file in os.listdir(directory) if file.endswith(".mp3")]
    mp3_files.sort()  # Sort the list of MP3 files

    # Initialize an empty AudioSegment
    combined = AudioSegment.empty()

    # Iterate over MP3 files and append them to the combined AudioSegment
    for mp3_file in mp3_files:
        audio = AudioSegment.from_mp3(os.path.join(directory, mp3_file))
        combined += audio

    # Export the combined AudioSegment as an MP3 file
    combined.export(output_file, format="mp3")

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

if __name__ == "__main__":
    # Input directory containing MP3 files
    input_directory = "d:/books/ders/output"
    album_artist = "alperyz"
    creator = "alperyz"
    album = "auzef"

    # Define the tags
    artist = "Sosyoloji Tarihi 1"
    title = "Sesli Kitap"

    # Output file name with path
    output_file = f"d:/books/ders/{artist}_{title}.mp3"
    # Combine MP3 files in the input directory and set tags
    combine_mp3_files(input_directory, output_file, title, artist, album)
    print("MP3 files combined and tagged successfully!")
