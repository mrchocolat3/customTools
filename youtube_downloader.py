import os
import math
import sys
import argparse
import youtube_dl

BEST_FORMAT = "bestvideo+bestaudio/best"
PARSER = argparse.ArgumentParser(description="Youtube Video Downloader")
PARSER.add_argument(
    '--Url', 
    '-u', 
    type=str, 
    help='YouTube video or playlist url')
PARSER.add_argument(
    "--Download", 
    '-d',
    type=bool,
    nargs='?',
    const=True, default=False,
)
PARSER.add_argument(
    "--Verbose",
    '-v',
    type=bool, 
    nargs='?',
    const=True, default=False
)

class ResourceNotFoundError(Exception):
    pass

class NoFilesizeError(Exception):
    pass

class TotalSize:
    def __init__(self, url):
        self._ydl = youtube_dl.YoutubeDL({"quiet": True, "no_warnings": True})
        self._selector = self._ydl.build_format_selector(BEST_FORMAT)
        try:
            preinfo = self._ydl.extract_info(url, process=False)
        except youtube_dl.utils.DownloadError:
            raise ResourceNotFoundError
        if 'entries' in preinfo:
            self._videos = list(preinfo['entries'])
        else:
            self._videos = [preinfo]
        self.number_of_videos = len(self._videos)

    def _get_size(self, info):
        try:
            video = self._ydl.process_ie_result(info, download=False)
        except youtube_dl.utils.DownloadError:
            raise NoFilesizeError
        try:
            best = next(self._selector(video))
        except KeyError:
            best = video
        try:
            if 'requested_formats' in best:
                size = sum(int(f['filesize'])
                           for f in best['requested_formats'])
            else:
                size = int(best['filesize'])
        except (TypeError, KeyError):
            raise NoFilesizeError
        return size

    def _readable_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_totalsize(self):
        totalsize = 0
        for video in self._videos:
            try:
                size = self._get_size(video)
            except NoFilesizeError:
                print('Filesize of "%s" is unavailable.' %
                      video['title'], file=sys.stderr)
            else:
                print('"%s": %s' % (video['title'], self._readable_size(size)))
                totalsize += size
        return self._readable_size(totalsize)

def main(url, get_lenght, download):
    if get_lenght:
        total = TotalSize(url)
        print('Total size of all videos with reported filesize: ' + total.get_totalsize())
        print('Total number of videos: %s' % total.number_of_videos)
        
    if download:
        os.system("youtube-dl -f best "+url)

    print("Exiting")
    sys.exit()

if __name__ == '__main__':
    args = PARSER.parse_args()
    try:
        get_lenght = args.Verbose
        download = args.Download
        url = args.Url
        main(url, get_lenght, download)
    except IndexError:
        sys.exit('Please supply an url.')
    except ResourceNotFoundError:
        sys.exit('Resource not found.')
