from youtube_dl import YoutubeDL

import threading

from tkinter import (
    Tk,
    Label,
    Button,
    Menu,
    PanedWindow,
    Entry,
    HORIZONTAL,
    X,
    Y,
    BOTH,
    END,
    LEFT,
    RIGHT,
    DISABLED,
    NORMAL,
)


class Youtube_To_MP3_Converter:
    def __init__(self):

        self.main_windows = Tk()

        # ====================== init main windows ======================

        # self.main_windows.protocol("WM_DELETE_WINDOW", self.close_app)
        self.main_windows.title("YOUTUBE TO MP3 CONVERTER")
        self.main_windows.minsize(300, 80)
        self.main_windows.geometry("300x100")
        # self.main_windows.iconbitmap("xxx.ico")

        # ====================== menu top bar ======================

        self.menubar = Menu(self.main_windows)
        self.main_windows.config(menu=self.menubar)

        # ====================== Entry ======================

        self.youtube_url_Entry = Entry(self.main_windows)

        self.youtube_url_Entry.pack(fill=X, padx=5, pady=5)

        # ====================== panelwindow + buttons ======================

        self.panelwindow = PanedWindow(
            self.main_windows, orient=HORIZONTAL, width=self.main_windows.winfo_width()
        )
        self.panelwindow.pack(fill=BOTH)

        self.bouton_exit = Button(self.panelwindow, text="EXIT", command=self.close_app)
        self.bouton_exit.pack(side=LEFT, padx=5, pady=5)

        self.bouton_start_convert = Button(
            self.panelwindow,
            text="Convert",
            command=lambda: threading.Thread(
                name="yt_mp3_convert_thread",
                target=lambda: self.convert_to_MP3({self.youtube_url_Entry.get()}),
            ).start(),
        )
        self.bouton_start_convert.pack(side=RIGHT, padx=5, pady=5)

        # ====================== Label ======================

        self.Label_avancement = Label(
            self.main_windows, text="place your URL and click on Convert"
        )
        self.Label_avancement.pack(fill=X, padx=5, pady=5)

        self.Label_music_name = Label(self.main_windows, text="music :")
        self.Label_music_name.pack(fill=X, padx=5, pady=5)

        # ====================== Label ======================

        self.main_windows.mainloop()

    def close_app(self):
        self.main_windows.quit()

    def my_hook(self, d):
        if d["status"] == "downloading":
            self.Label_avancement.config(text="downloading")
            self.Label_music_name.config(text="")

        elif d["status"] == "error":
            self.Label_avancement.config(text="!!!!ERROR!!!!")

        elif d["status"] == "finished":
            self.Label_avancement.config(text="Done downloading, now converting ...")

    def convert_to_MP3(self, YT_link):
        self.bouton_start_convert.config(state=DISABLED)
        self.youtube_url_Entry.config(state=DISABLED)
        self.Label_avancement.config(text="Start download")
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "progress_hooks": [self.my_hook],
                "outtmpl": "MP3_files/%(title)s.%(ext)s",
                "ffmpeg_location": "ff/",
            }

            with YoutubeDL(ydl_opts) as youtube_dl:
                youtube_dl.download(YT_link)

        except Exception as ex:
            print(ex)

        self.Label_avancement.config(
            text="convertion finished, file is now in MP3_file folder"
        )
        self.Label_music_name.config(text="")
        self.youtube_url_Entry.config(state=NORMAL)
        self.youtube_url_Entry.delete(0, END)
        self.bouton_start_convert.config(state=NORMAL)
