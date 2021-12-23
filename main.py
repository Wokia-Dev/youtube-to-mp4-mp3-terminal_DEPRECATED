import logging
from pytube import YouTube
from rich.console import Console
from rich.table import Table
from art import text2art

console = Console()


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
console.print('Choose format: ', style='bold yellow')
console.print(formatTable, '\n')

formatInput = str(input())



