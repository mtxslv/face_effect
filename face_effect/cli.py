import argparse
from pathlib import Path

from face_effect.process import process_video


parser = argparse.ArgumentParser(description='Face blur effect.')
parser.add_argument("--e",
                    "--effects", 
                    required=False,
                    type=list,
                    help="List of effects to be applied. Default: greyscale and face blur.",
                    nargs='+',
                    default = ['blur', 'greyscale'],
                    choices=['blur','Blur','greyscale','Greyscale'])

sources = ['Camera','Path','camera','path']
parser.add_argument("--s",
                    "--source",
                    required=False,
                    type=str,
                    help = "Image source. Default: camera.",
                    nargs=1,
                    default = 'Camera',
                    choices=sources
                    )

args = vars(parser.parse_args())

if args['s'] == "Camera" or args['s'][0] in ['camera','Camera']:
    print('Type Esc or q to quit')
    process_video()
else:
    print('local path of files')