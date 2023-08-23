import PySimpleGUI as sg
from pytube import Playlist, YouTube
from tqdm import tqdm
from flask import Flask, render_template, send_from_directory
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import ffmpeg
import os

class TelaDownloader:
    def __init__(self):
        # layout
        layout = [
            [sg.Text("Cole a URL do seu vídeo ou da playlist:")],
            [sg.Input(key="link")],
            [sg.Checkbox("Download em HD", key="download_hd")],
            [sg.Checkbox("Download somente áudio", key="baixar_audio")],
            [sg.Button("Download")]
        ]

        # instanciar a janela
        self.janela = sg.Window("Python Youtube Downloader").layout(layout)

    def download_videos(self):
        while True:
            evento, valores = self.janela.Read()

            if evento == sg.WINDOW_CLOSED:
                break

            url = valores['link']
            if "playlist?list=" in url:
                self.download_playlist(url)
            else:
                self.download_video(url)

            resposta = sg.popup_yes_no('Deseja baixar mais vídeos?')
            if resposta == 'No':
                break

    def download_video(self, url):
        print("Baixando vídeo...")
        youtube = YouTube(url)
        print('Título do vídeo:', youtube.title)

        res_youtube = youtube.streams.get_lowest_resolution()

        if self.janela['baixar_audio'].get():
            res_youtube = youtube.streams.get_audio_only()
            print("Baixando áudio...")
        else:
            if self.janela['download_hd'].get():
                res_youtube = youtube.streams.get_highest_resolution()
                print("Baixando em HD")

        res_youtube.download("A:\\Gerson Junior\\Downloads")

        print("Download finalizado!")

    def download_playlist(self, url):
        print("Baixando playlist...")
        yt_playlist = Playlist(url)
        videos = yt_playlist.videos

        progress_bar = tqdm(total=len(videos))

        for video in videos:
            video_url = 'https://www.youtube.com' + video.watch_url

            youtube = YouTube(video_url)

            res_youtube = youtube.streams.get_lowest_resolution()

            if self.janela['baixar_audio'].get():
                res_youtube = youtube.streams.get_audio_only()
                print("Baixando áudio...")
            else:
                if self.janela['download_hd'].get():
                    res_youtube = youtube.streams.get_highest_resolution()
                    print("Baixando em HD")

            res_youtube.download("A:\\Gerson Junior\\Downloads")
            progress_bar.update(1)

        progress_bar.close()

        print("Download finalizado!")


class TelaConversor:
    @staticmethod
    def apresentacao():
        # Criar a janela de apresentação
        apresentacao_window = tk.Tk()
        apresentacao_window.title('Apresentação')
        apresentacao_window.geometry('400x300')

        # Estilizar a janela
        style = ThemedStyle(apresentacao_window)
        style.set_theme('arc')

        label = tk.Label(apresentacao_window, text='Bem-vindo ao Conversor de MP4 para MP3!',
                          font=('Arial', 16), padx=20, pady=20)
        label.pack()

        def iniciar_conversao():
            apresentacao_window.destroy()
            TelaConversor.converter_arquivos()

        button = tk.Button(apresentacao_window, text='Iniciar Conversão', font=(
            'Arial', 12), padx=10, pady=10, bg='#FFB6C1', fg='white', command=iniciar_conversao)
        button.pack(pady=10)

        # Iniciar a interface de apresentação
        apresentacao_window.mainloop()

    @staticmethod
    def converter_arquivos():
        # Criar a janela de conversão
        conversao_window = tk.Tk()
        conversao_window.title('Conversão')
        conversao_window.geometry('400x300')

        # Estilizar a janela
        style = ThemedStyle(conversao_window)
        style.set_theme('plastik')

        label = tk.Label(conversao_window, text='A conversão está em andamento...', font=(
            'Arial', 16), padx=20, pady=20)
        label.pack()

        # Adicionar a barra de progresso
        progress_bar = ttk.Progressbar(conversao_window, mode='determinate')
        progress_bar.pack(pady=10)

        # Obter os arquivos MP4 selecionados
        arquivos_mp4 = filedialog.askopenfilenames(
            filetypes=[('Arquivos MP4', '*.mp4')])

        if arquivos_mp4:
            total_arquivos = len(arquivos_mp4)
            for index, arquivo in enumerate(arquivos_mp4, start=1):
                try:
                    # Definir o caminho de saída para o arquivo MP3
                    output_path = os.path.splitext(arquivo)[0] + '.mp3'

                    # Verificar se o arquivo MP3 já existe
                    if os.path.exists(output_path):
                        os.remove(output_path)

                    # Atualizar o valor da barra de progresso
                    progress = (index / total_arquivos) * 100
                    progress_bar['value'] = progress
                    conversao_window.update_idletasks()

                    # Converter MP4 para MP3 usando ffmpeg
                    ffmpeg.input(arquivo).output(
                        output_path, format='mp3').run(overwrite_output=True)

                except Exception as e:
                    messagebox.showerror(
                        'Erro na Conversão', f'Erro ao converter o arquivo "{arquivo}": {str(e)}')

            # Exibir a janela de conclusão
            TelaConversor.exibir_conclusao(conversao_window)

        else:
            messagebox.showwarning(
                'Erro', 'Selecione pelo menos um arquivo MP4 para conversão.')

        # Fechar a janela de conversão e retornar à janela de apresentação
        conversao_window.destroy()
        TelaConversor.apresentacao()

    @staticmethod
    def exibir_conclusao(conversao_window):
        # Fechar a janela de conversão
        conversao_window.destroy()

        # Criar a janela de conclusão
        conclusao_window = tk.Tk()
        conclusao_window.title('Conversão Concluída')
        conclusao_window.geometry('400x200')

        # Estilizar a janela
        style = ThemedStyle(conclusao_window)
        style.set_theme('equilux')

        label = tk.Label(conclusao_window, text='A conversão foi concluída com sucesso!', font=(
            'Arial', 16), padx=20, pady=20)
        label.pack(pady=50)

        def converter_mais_arquivos():
            conclusao_window.destroy()
            TelaConversor.converter_arquivos()

        button_converte_mais = tk.Button(conclusao_window, text='Converter Mais Arquivos', font=(
            'Arial', 12), padx=10, pady=10, command=converter_mais_arquivos)
        button_converte_mais.pack(pady=10)

        def fechar_janela():
            conclusao_window.destroy()

        button_fechar = tk.Button(conclusao_window, text='Fechar', font=(
            'Arial', 12), padx=10, pady=10, bg='#FFB6C1', fg='white', command=fechar_janela)
        button_fechar.pack(pady=10)

        # Iniciar a interface de conclusão
        conclusao_window.mainloop()


# Iniciar a apresentação
app = Flask(__name__)
app.static_folder = 'static'
tela = TelaDownloader()
conversor = TelaConversor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/youtube-downloader')
def youtube_downloader():
    # Lógica para executar o script Python do YouTube Downloader
    tela.download_videos()
    return 'YouTube Downloader'

@app.route('/conversor-mp4-para-mp3')
def conversor_mp4_para_mp3():
    # Lógica para executar o script Python do Conversor MP4 para MP3
    return 'Conversor MP4 para MP3'

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, app.static_folder), filename)

if __name__ == '__main__':
    app.run()
