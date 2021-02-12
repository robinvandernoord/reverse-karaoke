import sys
from icecream import ic
import moviepy.editor

MP4_PATH = './temp/out.mp4'
MP3_PATH = './temp/out.mp3'
VOCALS = 'out/vocals.mp3'


# step 1: download mp4
# step 2: split mp3
# step 3: split streams
# step 4: remove audio from mp4
# step 5: add voice to mp4

# async/threads?

def split(in_path):
    from spleeter.separator import Separator  # apt install ffmpeg
    print('### Splitting mp3')
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(in_path, './', codec='mp3')


# def download_mp4_pytube(url):
#     print('### Downloading mp4 - pytube')
#     ic(url)
#     yt = YouTube(url)
#     stream = yt.streams.filter(
#         file_extension='mp4',
#         res='720p',
#         audio_codec='mp4a.40.2',
#     ).first()
#     stream.download('./temp')
#     ic(stream)
#     return f'./temp/{stream.default_filename}'

def download_mp4(url):
    import youtube_dl
    print('### Downloading mp4 - youtube_dl')
    ic(url)
    ydl_opts = {
        'outtmpl': './temp/out.mp4',  # ./temp/out.mp4
        # 'format': '136'  # 720p mp4
        'format': '22/18'  # 720p mp4 with audio, 360p if 720p not available
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def extract_mp3(path):
    print('### Extracting mp3')
    newpath = path.rsplit('.', 1)[0] + '.mp3'
    ic(path, newpath)
    vid = moviepy.editor.VideoFileClip(path)
    ic(vid, vid.audio)
    vid.audio.write_audiofile(newpath)
    return newpath


def rejoin(vid_path, aud_path):
    print('### Merging vocals and video')
    ic(vid_path, aud_path)
    vid = moviepy.editor.VideoFileClip(vid_path)
    aud = moviepy.editor.AudioFileClip(aud_path)
    ic(vid, aud)
    vid.audio = aud

    vid.write_videofile("final.mp4")


def cleanup():
    import shutil
    print('### Cleaning up')
    shutil.rmtree('./out')
    shutil.rmtree('./temp')


def main():
    download_mp4(*sys.argv[1:])
    extract_mp3(MP4_PATH)
    split(MP3_PATH)
    rejoin(MP4_PATH, VOCALS)
    cleanup()
    print('### DONE ###')


if __name__ == '__main__':
    main()
