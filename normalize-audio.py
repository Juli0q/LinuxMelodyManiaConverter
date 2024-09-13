import argparse
import logging
import os
import time

from pydub import AudioSegment, effects

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="Convert a video file")
parser.add_argument("--input-folder", metavar="input", type=str, help="Input video file")

# Parse the arguments
args = parser.parse_args()

logging.info(f"Starting conversion of audios in {args.input_folder}")
start_time = time.time()

for root, dirs, files in os.walk(args.input_folder):
    for file in files:
        # Check if the file is a video file
        if file.endswith(".m4a"):
            logging.info(f"Normalizing {file}")
            # Get the full path of the file
            file_path = os.path.join(root, file)

            # Replace the filename with the new extension
            try:
                raw_sound = AudioSegment.from_file(file_path, "m4a")
                normalized_sound = effects.normalize(raw_sound)
                normalized_sound.export(file_path, format="mp4")
            except Exception as e:
                logging.error(f"Error normalizing {file}: {e}")
                continue
            logging.info(f"Normalized {file}")


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
