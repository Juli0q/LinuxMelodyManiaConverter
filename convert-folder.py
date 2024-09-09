import argparse
import json
import logging
import os
import shlex
import subprocess
import time

from ffmpeg_progress_yield import FfmpegProgress

from tqdm import tqdm

# Set up logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# Check if ffmpeg is installed
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
except FileNotFoundError:
    print("ffmpeg is not installed")
    exit(1)

# Initialize the parser
parser = argparse.ArgumentParser(description="Convert a video file")

# Add the arguments
parser.add_argument("--input-folder", metavar="input", type=str, help="Input video file")
parser.add_argument("--width", type=int, help="Width of the output video", default=1920)
parser.add_argument("--height", type=int, help="Height of the output video", default=1080)
parser.add_argument("--bitrate", metavar="output", type=int,
                    help="Output video bitrate, uses the input videos default", default="-1")

# Parse the arguments
args = parser.parse_args()


def convert_video(input_file_path, output_file_path, song_name):
    # Get the bitrate of the input video
    if args.bitrate == -1:
        bitrate = get_bitrate(input_file_path)
    else:
        bitrate = args.bitrate

    # Initialize the progress bar
    pbar = tqdm(total=100, desc=f"Converting {song_name}", unit="%", unit_scale=True)

    # Convert the input_file_path mp4 to output_file_path webm with the specified width and height
    cmd = (f'ffmpeg -y -i "{input_file_path}" -c:v libvpx -b:v {bitrate} '
           f'-vf scale={args.width}:{args.height} "{output_file_path}"')
    cmd_args = shlex.split(cmd)

    # Convert the video
    for progress in FfmpegProgress(cmd_args).run_command_with_progress():
        pbar.update(progress - pbar.n)

    # Close the progress bar
    pbar.close()


# Get the bitrate of the input and output files
def get_bitrate(file_path):
    cmd = f"ffprobe -v quiet -print_format json -show_format -show_streams '{file_path}'"
    result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
    video_info = json.loads(result.stdout)
    bitrate = video_info['format']['bit_rate']
    return bitrate


# Replace the video line in the .txt file
def replace_video_line(song_name, root):
    # Define the path to the .txt file
    txt_file_path = os.path.join(root, f"{song_name}.txt")

    # Open the .txt file in read mode and read all lines
    with open(txt_file_path, "r") as file:
        lines = file.readlines()

    # Iterate over the lines
    for i, line in enumerate(lines):
        # Check if the line starts with #VIDEO
        if line.startswith("#VIDEO"):
            # Replace the .mp4 extension with .webm
            lines[i] = line.replace(".mp4", ".webm")

    # Open the .txt file in write mode and write the modified lines
    with open(txt_file_path, "w") as file:
        file.writelines(lines)


logging.info(f"Starting conversion of videos in {args.input_folder}")
start_time = time.time()

# Scan all folders in target folder
for root, dirs, files in os.walk(args.input_folder):
    for file in files:
        # Check if the file is a video file
        if file.endswith(".mp4"):
            # Get the full path of the file
            file_path = os.path.join(root, file)

            # Replace the filename with the new extension
            output_path = os.path.join(root, file.replace(".mp4", ".webm"))

            # Get the song name
            song_name = file.replace(".mp4", "")

            logging.info(f"Converting {song_name}")

            # Convert the video
            convert_video(file_path, output_path, song_name)

            # Replace the video line in the .txt file
            replace_video_line(song_name, root)

# Get the end time
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

# Calculate the number of days, hours, minutes and seconds
days, remainder = divmod(duration, 86400)
hours, remainder = divmod(remainder, 3600)
minutes, seconds = divmod(remainder, 60)

# Print the duration
logging.info(f"Conversion complete, took {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and "
             f"{int(seconds)} seconds")