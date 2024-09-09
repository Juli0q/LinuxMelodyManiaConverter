# Melody Mania Song Converter
A small python script to convert existing mp4 video files to webm format using ffmpeg. When running the game on a
Linux Device like the Steam Deck or a Raspberry Pi, the game will loop the mp4 files every 5 seconds. A workaround is to
convert the mp4 files to webm format.

**The script has only been tested on Linux and may not work on Windows or MacOS.**

## Requirements
- Python 3.6 or higher
- ffmpeg

You can install all required python packages by running the following command:
```bash
pip install -r requirements.txt
```

## Usage
Please make a backup of your songs before running the script. 
```bash
python convert.py --input-folder <input-folder>
```

## Options
- `--input-folder` - The folder containing the mp4 files that you want to convert to webm format.
- `--width` - The width of the output video. Default is 1080.
- `--height` - The height of the output video. Default is 1920.
- `--bitrate` - The bitrate of the output video. Default is pulled from the input video.