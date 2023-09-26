import os
from flask import Flask, request, render_template
from pytube import YouTube
import moviepy.editor as mp

app = Flask(__name__)

# Configuração do caminho para salvar os vídeos
app.config['CAMINHO_PADRAO'] = "A:/Usuário/Gerson Junior/Downloads"

@app.route('/')
def index():
    return render_template('index.html', caminho_padrao=app.config['CAMINHO_PADRAO'])

@app.route('/download', methods=['POST'])
def download():
    url = request.form['link']
    baixar_hd = 'download_hd' in request.form
    baixar_audio = 'baixar_audio' in request.form

    try:
        youtube = YouTube(url)
        destino = os.path.join(app.config['CAMINHO_PADRAO'], youtube.title)
        os.makedirs(destino, exist_ok=True)

        if baixar_hd:
            youtube.streams.get_highest_resolution().download(destino)
        else:
            youtube.streams.get_lowest_resolution().download(destino)

        if baixar_audio:
            video_clip = mp.VideoFileClip(os.path.join(destino, youtube.title + ".mp4"))
            video_clip.audio.write_audiofile(os.path.join(destino, youtube.title + ".mp3"))
            video_clip.close()
            
        return f"Download concluído! Arquivo salvo em {destino}"
    except Exception as e:
        return f"Erro durante o download: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
