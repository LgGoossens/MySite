from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
import yt_dlp

views = Blueprint('views', __name__)


def download_youtube(data):
    link = data['link']
    print(data)
    index = 0
    if 'watch' in link.lower():
        ydl_opts_video = {
            'format': 'best',
            'ignoreerrors': 'only_download',

            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],

            'outtmpl': r'temp\video\%(title)s' + '.mp4'
        }

        ydl_opts_audio = {
            'format': 'bestaudio',
            'ignoreerrors': 'only_download',

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],

            'outtmpl': r'temp\audio\%(title)s'
        }
        if data.get('doVideo'):
            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                ydl.download(link)
        if data.get('doAudio'):
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download(link)
    elif 'playlist' in link.lower():
        ydl_opts_video = {
            'format': 'best',
            'ignoreerrors': 'only_download',
            'playliststart': 0,

            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],

            'outtmpl': r'temp\video\%(title)s' + '.mp4'
        }

        ydl_opts_audio = {
            'format': 'bestaudio',
            'ignoreerrors': 'only_download',
            'playliststart': 0,

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],

            'outtmpl': r'temp\audio\%(title)s'
        }


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        download_youtube(request.form)
        return redirect('/')
    return render_template("home.html", user=current_user, form=None)
