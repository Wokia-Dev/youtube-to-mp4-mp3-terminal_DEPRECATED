import logging
import shutil
import sys
import time
import os

from pytube import YouTube
from rich.console import Console
from rich.table import Table
from art import text2art
from rich.progress import track
from moviepy.editor import *

console = Console()
filePath = os.path.dirname(os.path.realpath(__file__))


def print_title():
    console.print(text2art('YOUTUBE     DL', font='standard'), style='bold green')
    console.print('By Wokia\n\n', style='bold italic green')


print_title()
console.print('Enter youtube urls (drag an drop): ', style='bold yellow')
urlsInput = str(input())

urls = urlsInput.replace(' ', '').split('https://')
del urls[0]
console.clear()
print_title()

# format table
formatTable = Table(show_header=True, header_style='bold red')
formatTable.add_column('Format', style='bold', width=12)
formatTable.add_column('Selector', style='bold', width=12)
formatTable.add_row('video/mp4', 'mp4')
formatTable.add_row('audio/mp3', 'mp3')
console.print(formatTable)

console.print('Choose format: ', style='bold yellow')
formatInput = str(input())
formatSelector = 'mp4', 'mp3'
audioSelector = 'mp3', ''
videoSelector = 'mp4', ''

while formatInput not in formatSelector:
    console.print('Choose format: ', style='bold yellow')
    formatInput = str(input())

console.clear()
print_title()

resumeTable = Table(show_header=True, header_style='bold green')
resumeTable.add_column('Title', style='dim', width=32)
resumeTable.add_column('Author', style='dim', width=12)
resumeTable.add_column('views', style='dim', width=14)
resumeTable.add_column('length', style='dim', width=12)
resumeTable.add_column('format', style='dim', width=9)

for url in urls:
    video = YouTube('https://' + url)
    resumeTable.add_row(
        '[cyan]' + video.title,
        '[magenta]' + video.author,
        '[red]' + f'{video.views:,}'.replace(',', ' '),
        '[yellow]' + time.strftime('%H:%M:%S', time.gmtime(video.length)),
        '[blue]' + formatInput,
        end_section=True
    )
console.print(resumeTable)

console.print('Press enter to download...\n', style='bold yellow')
input()


def show_progress_bar(stream, chunk: bytes, bytes_remaining: int):
    current = ((stream.filesize - bytes_remaining) / stream.filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


for url in urls:
    video = YouTube('https://' + url)
    video.register_on_progress_callback(show_progress_bar)
    if formatInput in audioSelector:
        console.print('Downloading: ' + video.title, style='bold yellow')
        video.streams.get_audio_only().download(output_path=filePath + '/tempDL', filename='video.mp4')
        console.print('\nDOWNLOAD COMPLETED\n', style='bold green')
        if formatInput == 'mp3':
            mp4File = filePath + '/tempDL/' + 'video.mp4'
            mp3File = filePath + '/tempDL/' + 'video.mp3'
            console.print('Converting file...', style='bold yellow')
            audioClip = AudioFileClip(mp4File)
            audioClip.write_audiofile(mp3File)
            audioClip.close()
            console.print('CONVERT COMPLETED\n', style='bold green')
            os.remove(mp4File)
            shutil.move(mp3File, filePath + '/VideosOutput')
            os.rename(filePath + '/VideosOutput/video.mp3', filePath + '/VideosOutput/' + video.title + '.mp3')
            console.print('-' * 80 + '\n', style='bold grey0')

    elif formatInput in videoSelector:
        console.print('Downloading: ' + video.title, style='bold yellow')
        video.streams.get_highest_resolution().download(output_path=filePath + '/tempDL', filename='video.mp4')
        console.print('\nDOWNLOAD COMPLETED\n', style='bold green')
        shutil.move(filePath + '/tempDL/video.mp4', filePath + '/VideosOutput/video.mp4')
        os.rename(filePath + '/VideosOutput/video.mp4', filePath + '/VideosOutput/' + video.title + '.mp4')
        console.print('-' * 80 + '\n', style='bold grey0')
