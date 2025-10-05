import os
from moviepy import ImageClip, AudioFileClip
import configparser

def create_video(image_path=None, audio_path=None, video_basename=None, videos_dir=None):
    # Read variables from the configuration file if paths are not provided
    config = configparser.ConfigParser()
    config.read('variables.cfg', encoding='utf-8')
    workdir = config['DEFAULT']['workdir']  # use workdir from config

    if not image_path:
        image_path = config['DEFAULT']['video_image_path']
    if not audio_path:
        # Use the relative video_audio_path which is under workdir
        audio_path = config['DEFAULT']['video_audio_path']

    # Normalize paths to be under workdir if they are not absolute
    if not os.path.isabs(image_path):
        image_path = os.path.join(workdir, image_path)
    if not os.path.isabs(audio_path):
        audio_path = os.path.join(workdir, audio_path)

    # Use the videos_dir if provided, otherwise use the directory of audio_path
    if videos_dir:
        output_dir = videos_dir
    else:
        output_dir = os.path.dirname(audio_path)
    if video_basename:
        base_filename = video_basename
    else:
        base_filename = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(output_dir, base_filename + '.mp4')

    # Check if files exist
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file '{audio_path}' not found.")

    # Load the image and audio
    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)

    image_clip = image_clip.resized(new_size=(1920, 1080))
    image_clip = image_clip.with_duration(audio_clip.duration)
    video_clip = image_clip.with_audio(audio_clip)

    video_clip.write_videofile(
        output_path,
        codec="libx264",
        fps=1,
        bitrate="256k",
        preset="fast",
        ffmpeg_params=["-crf", "18", "-qscale", "0"]
    )
    # Clean up clips
    video_clip.close()
    audio_clip.close()
    image_clip.close()
    print(f"MP4 file created: {output_path}")
    return output_path

if __name__ == '__main__':
    create_video()

