// Adicionar eventos aos botões
document.getElementById("botao-youtube-downloader").addEventListener("click", abrirLinkYoutubeDownloader);
document.getElementById("botao-conversor-mp4-para-mp3").addEventListener("click", abrirLinkConversorMp4ParaMp3);

// Função para abrir o link do YouTube Downloader
function abrirLinkYoutubeDownloader() {
    window.open('/youtube-downloader');
}

// Função para abrir o link do Conversor MP4 para MP3
function abrirLinkConversorMp4ParaMp3() {
    window.open('/conversor-mp4-para-mp3');
}
