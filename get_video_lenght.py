import subprocess
import os
import sys
import argparse
import moviepy.editor as mp
import datetime

parser = argparse.ArgumentParser(description="Total Length of available videos on a folder")
parser.add_argument(
    'path',
    metavar='path',
    type=str,
    help='The path to get vidoes from'
    )


class VideoTool:
    def __init__(self, path):
        self.path = path
        self.video_paths = list() 
        self.totalFiles = 0

    def get_length(self, input_video):
        return mp.VideoFileClip(input_video).duration
    
    def parseFiles(self):
        for path, root, files in os.walk(self.path):
            for file in files:
                if file.endswith(".mp4"):
                    self.video_paths.append(os.path.join(path, file)) 
                    self.totalFiles += 1
        self.video_paths.sort()

    def get_total_lenght(self):
        if len(self.video_paths) == 0:
            print(f"There are no videos in: '{os.getcwd()}'")
            print("Exiting....")
            sys.exit()
        lenght = 0
        print("Calculating Time, Please wait.......")
        for video in self.video_paths:
            lenght += self.get_length(video)
        print("Total Videos: ", self.totalFiles)
        print("Total Lenght: ", str(datetime.timedelta(seconds=lenght)))

if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path
    if not os.path.isdir(path):
        print(f'The path:"{path}" is not a directory!\nExiting...')
        sys.exit()

    vt = VideoTool(path)
    vt.parseFiles()
    vt.get_total_lenght()