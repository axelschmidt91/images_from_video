# images_from_video

This command line tool extracts a defined number of images from a video at a constant interval. The number of images to extract can be defined. The total frame count of the video is divided by the number of images defined and rounded down. This lead to sometimes more images than asked for to acheve a constant periodic interval. 

## Install requirements

```
pip install -r requirements.txt
```

## Usage

Refering to the cli help provided by argparse, open help:
```
python vid2imgs -h
```
