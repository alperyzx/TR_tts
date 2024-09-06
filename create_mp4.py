import os
from moviepy.editor import ImageClip, AudioFileClip

# Set the working directory
os.chdir(r'D:\books\ders\output')

# File paths
image_path = 'o1080081015059876986.jpg'
audio_path = 'Felsefenin Temel Kavramları_Sesli Kitap P2.mp3'
output_path = 'ftkP2_high_quality.mp4'

# Load the image and audio
image_clip = ImageClip(image_path)
audio_clip = AudioFileClip(audio_path)

# Set the duration of the image clip to match the audio clip's duration
image_clip = image_clip.set_duration(audio_clip.duration)

# Set the audio to the image
video_clip = image_clip.set_audio(audio_clip)

# Write the result to a file with high-quality settings
video_clip.write_videofile(
    output_path,
    codec="libx264",
    fps=1,  # Using 1 frame per second because we only have one static image
    bitrate="5000k",  # High bitrate to preserve quality
    preset="veryslow",  # Very slow preset for the best quality compression
    ffmpeg_params=["-crf", "18", "-qscale", "0"]  # CRF for high-quality output
)
