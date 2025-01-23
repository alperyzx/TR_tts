import os
from moviepy import ImageClip, AudioFileClip

# Set the working directory
os.chdir(r'D:\books\ders')

# File paths
image_path = 'p1.jpg'
audio_path = 'Yeni Çağ Felsefesi.mp3'
output_path = 'Yeni Çağ Felsefesi.mp4'

# Load the image and audio
image_clip = ImageClip(image_path)
audio_clip = AudioFileClip(audio_path)

# Resize the image to fill the screen (e.g., 1920x1080 resolution)
image_clip = image_clip.resized(new_size=(1920, 1080))

# Set the duration of the image clip to match the audio clip's duration
image_clip = image_clip.with_duration(audio_clip.duration)

# Set the audio to the image
video_clip = image_clip.with_audio(audio_clip)

# Write the result to a file with high-quality settings
video_clip.write_videofile(
    output_path,
    codec="libx264",
    fps=1,  # Using 1 frame per second because we only have one static image
    bitrate="256k",  # High bitrate to preserve quality
    preset="fast",  # Adjust for balance between quality and speed
    ffmpeg_params=["-crf", "18", "-qscale", "0"]  # CRF for high-quality output
)
