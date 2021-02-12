from spleeter.separator import Separator  # apt install ffmpeg
from pytube import YouTube
import sys
from icecream import ic
import moviepy.editor


# step 1: download mp4
# step 2: split mp3
# step 3: split streams
# step 4: remove audio from mp4
# step 5: add voice to mp4

# async/threads?

def split(in_path):
    print('### Splitting mp3')
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(in_path, './output')


def download_mp4(url):
    print('### Downloading mp4')
    ic(url)
    yt = YouTube(url)
    stream = yt.streams

    ic(stream)
    exit()

    stream = yt.streams.filter(
        file_extension='mp4',
        res='720p',
        audio_codec='mp4a.40.2',
    ).first()
    stream.download('./temp')
    ic(stream)
    return f'./temp/{stream.default_filename}'


def extract_mp3(path):
    print('### Extracting mp3')
    newpath = path.rsplit('.', 1)[0] + '.mp3'
    ic(path, newpath)
    vid = moviepy.editor.VideoFileClip(path)
    ic(vid, vid.audio)
    vid.audio.write_audiofile(newpath)
    return newpath


if __name__ == '__main__':
    path = download_mp4(*sys.argv[1:])
    path = './temp/Wally Mckey Ga Niet Weg.mp4'
    path = extract_mp3(path)
    ic(path)
    # split(*sys.argv[1:])
    # https://www.youtube.com/watch?v=N_gWEoCg5o4
