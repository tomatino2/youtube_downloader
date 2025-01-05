import os
import customtkinter as ctk
from tkinter import filedialog
from yt_dlp import YoutubeDL
import threading
import re
import tkinter.messagebox as messagebox

# Initialisation de l'application avec customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Téléchargeur YouTube MP4/MP3")
app.geometry("500x400")
app.resizable(False, False)

# Fonction pour valider l'URL YouTube
def is_valid_youtube_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'  
    return re.match(youtube_regex, url) is not None

# Fonction pour obtenir le répertoire de sauvegarde
def get_save_path():
    save_path = filedialog.askdirectory()
    if not save_path:
        status_label.configure(text="Aucun répertoire sélectionné. Téléchargement annulé.", text_color="red")
    return save_path

# Fonction pour préparer les options de téléchargement
def prepare_download_options(format_choice, resolution_choice, save_path):
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
    }

    if format_choice == "MP4":
        ydl_opts['format'] = f'bestvideo[height<={resolution_choice}]+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'
    elif format_choice == "MP3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    return ydl_opts

# Fonction de téléchargement vidéo
def download_video():
    url = url_entry.get()
    format_choice = format_var.get()
    resolution_choice = resolution_var.get()

    if not url or not is_valid_youtube_url(url):
        status_label.configure(text="URL invalide. Veuillez entrer une URL YouTube valide.", text_color="red")
        return

    # Demander où sauvegarder le fichier
    save_path = get_save_path()
    if not save_path:
        return

    # Préparer les options de téléchargement
    ydl_opts = prepare_download_options(format_choice, resolution_choice, save_path)

    try:
        # Afficher un message de téléchargement en cours
        status_label.configure(text="Téléchargement en cours...", text_color="orange")
        download_button.configure(state="disabled")

        # Démarrer le téléchargement
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Réinitialiser l'interface après le téléchargement
        url_entry.delete(0, 'end')
        format_var.set("MP4")
        resolution_var.set("1080")
        status_label.configure(text="Téléchargement terminé avec succès !", text_color="green")
        download_button.configure(state="normal")

        # Demander si l'utilisateur souhaite ouvrir le répertoire
        if messagebox.askyesno("Téléchargement terminé", "Téléchargement terminé avec succès. Voulez-vous ouvrir le dossier ?"):
            os.startfile(save_path)

    except Exception as e:
        status_label.configure(text=f"Erreur : {str(e)}", text_color="red")
        download_button.configure(state="normal")

# Fonction pour exécuter le téléchargement dans un thread séparé
def start_download():
    download_thread = threading.Thread(target=download_video)
    download_thread.start()

# Interface utilisateur
title_label = ctk.CTkLabel(app, text="Téléchargeur YouTube MP4/MP3", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Champ pour l'URL
url_label = ctk.CTkLabel(app, text="Entrez l'URL YouTube :", font=("Arial", 14))
url_label.pack(pady=5)
url_entry = ctk.CTkEntry(app, width=400, placeholder_text="https://www.youtube.com/...") 
url_entry.pack(pady=5)

# Choix du format (MP4 ou MP3)
format_var = ctk.StringVar(value="MP4")
format_label = ctk.CTkLabel(app, text="Choisissez le format :", font=("Arial", 14))
format_label.pack(pady=5)
format_menu = ctk.CTkOptionMenu(app, variable=format_var, values=["MP4", "MP3"])
format_menu.pack(pady=5)

# Choix de la résolution
resolution_var = ctk.StringVar(value="1080")
resolution_label = ctk.CTkLabel(app, text="Choisissez la résolution (pour MP4) :", font=("Arial", 14))
resolution_label.pack(pady=5)
resolution_menu = ctk.CTkOptionMenu(app, variable=resolution_var, values=["360", "720", "1080"])
resolution_menu.pack(pady=5)

# Label pour afficher les messages de statut
status_label = ctk.CTkLabel(app, text="", font=("Arial", 12), text_color="red")
status_label.pack(pady=5)

# Bouton de téléchargement
download_button = ctk.CTkButton(app, text="Télécharger", command=start_download, font=("Arial", 14))
download_button.pack(pady=20)

# Lancer l'application
app.mainloop()