import argparse
from pathlib import Path

from face_effect.process import process_files, process_video


parser = argparse.ArgumentParser(description='Face blur effect.')
parser.add_argument("--e",
                    "--effects", 
                    required=False,
                    type=str,
                    help="List of effects to be applied. Default: greyscale and face blur.",
                    nargs='+',
                    default = ['greyscale'],
                    choices=['greyscale','Greyscale','none','None'])

sources = ['camera','Camera','path','Path']
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
    process_video(args['e'])
else:
    
    input_path = Path('/kaldhaslkfhafklhf') # random string to make it unreal
    while not input_path.exists():
        input_str = input('Please, type input folder path: ')
        input_path = Path(input_str)

    output_str = input('Please, enter output path (type . to save in input folder):')
    output_path = Path(output_str)
    if not output_path.exists() or str(output_path) == '.':
        print('Output path not found. Saving in input folder')
        output_path = input_path
    process_files(input_path, output_path, args['e'])