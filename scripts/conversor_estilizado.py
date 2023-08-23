import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import ffmpeg
import os

# Função para apresentação inicial


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

    # Botão para iniciar a conversão
    def iniciar_conversao():
        apresentacao_window.destroy()
        converter_arquivos()

    button = tk.Button(apresentacao_window, text='Iniciar Conversão', font=(
        'Arial', 12), padx=10, pady=10, bg='#FFB6C1', fg='white', command=iniciar_conversao)
    button.pack(pady=10)

    # Iniciar a interface de apresentação
    apresentacao_window.mainloop()


# Função para a janela de conversão
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
        exibir_conclusao(conversao_window)

    else:
        messagebox.showwarning(
            'Erro', 'Selecione pelo menos um arquivo MP4 para conversão.')

        # Fechar a janela de conversão e retornar à janela de apresentação
        conversao_window.destroy()
        apresentacao()


# Função para exibir a janela de conclusão
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

    # Botão para converter mais arquivos
    def converter_mais_arquivos():
        conclusao_window.destroy()
        converter_arquivos()

    button_converte_mais = tk.Button(conclusao_window, text='Converter Mais Arquivos', font=(
        'Arial', 12), padx=10, pady=10, bg='#ADD8E6', fg='white', command=converter_mais_arquivos)
    button_converte_mais.pack(pady=10)

    # Botão para fechar a janela
    def fechar_janela():
        conclusao_window.destroy()

    button_fechar = tk.Button(conclusao_window, text='Fechar', font=(
        'Arial', 12), padx=10, pady=10, bg='#FFB6C1', fg='white', command=fechar_janela)
    button_fechar.pack(pady=10)

    # Iniciar a interface de conclusão
    conclusao_window.mainloop()


# Iniciar a apresentação
apresentacao()
