import PySimpleGUI as sg
from pytube import Playlist, YouTube
from tqdm import tqdm


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


tela = TelaDownloader()
tela.download_videos()
