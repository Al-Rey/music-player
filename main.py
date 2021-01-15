import os
# from tkinter import *
import tkinter as tk

PATH = "./music"

class Player:
    def __init__(self):
        self.playlist = []
        self.get_music_library()

    # get the names of the songs in the music folder
    def get_music_library(self):
        self.playlist = os.listdir(PATH)

    def get_playlist(self):
        return self.play



class GUI:
    def __init__(self):
        # making the window
        self.root = tk.Tk()
        self.root.geometry("300x500")

        # create the music name label
        self.frm_song_name = tk.Frame(master=self.root, bg="red", bd=3, height=250, width=300)
        self.lbl_song = tk.Label(master=self.frm_song_name, text="[enter song here]", bd=3)

        self.lbl_song.pack(fill=tk.BOTH)

        self.frm_song_name.pack(expand=True, fill=tk.BOTH)

        # create a playlist list
        self.my_scroll = tk.Scrollbar(master=self.frm_song_name)
        self.my_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.scr_playlist = tk.Listbox(master=self.frm_song_name, yscrollcommand=self.my_scroll.set, width=40, bd=4)
        for line in range(1, 100):
            self.scr_playlist.insert(tk.END, str(line))
        self.scr_playlist.pack(side=tk.LEFT, fill=tk.BOTH)

        self.my_scroll.config(command=self.scr_playlist.yview)


        #  create the buttons
        self.frm_buttons = tk.Frame(master=self.root, bg="green", bd = 3, width=300, height=250)   # the main frame

        self.frm_grid = tk.Frame(master=self.frm_buttons, bg="blue")    # the grid frame that holds the buttons

        self.btn_play = tk.Button(master=self.frm_grid, text="play", font="80", width=8)
        self.btn_pause = tk.Button(master=self.frm_grid, text="pause", font="80", width=8)
        self.btn_next = tk.Button(master=self.frm_grid, text="next", font="80", width=8)
        self.btn_back = tk.Button(master=self.frm_grid, text="back", font="80", width=8)
        self.btn_shufful = tk.Button(master=self.frm_grid, text="shufful", font="80", width=8)

        self.btn_play.grid(row=1, column=2)
        self.btn_pause.grid(row=3, column=2)
        self.btn_next.grid(row=2, column=3)
        self.btn_back.grid(row=2, column=1)
        self.btn_shufful.grid(row=2, column=2)

        self.frm_grid.pack(expand=True)
        self.frm_buttons.pack(expand=True, fill=tk.BOTH)
        

        self.root.mainloop()


if __name__ == "__main__":
    graphic = GUI()