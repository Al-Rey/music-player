import os
import re
# from tkinter import *
import tkinter as tk
# import playsound
from playsound import playsound
# import threading
import multiprocessing

PATH = "./music"


class Player:
    def __init__(self):
        self.playlist = []
        self.file_names = []
        self.get_music_library()
        self.current_song = -1

        print(self.playlist)
        print(self.file_names)

    # get the names of the songs in the music folder
    def get_music_library(self):
        self.file_names = os.listdir(PATH)
        hold = []

        # seperate the file names from the file types
        for name in self.file_names:
            temp = re.split("\.", name)
            print("seperated: ", temp)

            build = ""
            if len(temp) > 2:
                for i in range(0, len(temp)-1):
                    build += temp[i]
                hold.append(build)
            else:
                hold.append(temp[0])
            
        # get only the song name into the playlist
        for song in hold:
            result = re.match("[0-9]", song)

            if result:
                self.playlist.append(song[result.span()[1]+1:].strip())
            else:
                self.playlist.append(song.strip())

    # fet the playlist variable
    def get_playlist(self):
        return self.playlist
    
    def get_song(self, index):
        return self.playlist[index]

    def get_file_name(self, index):
        return self.file_names[index]

    def get_current_song(self):
        return self.current_song



class GUI:
    def __init__(self):
        self.player = Player()
        # self.stop_play_thread=False

        # threads
        self.play_background = multiprocessing.Process(target=playsound, daemon=True)

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
        for line in self.player.get_playlist():
            self.scr_playlist.insert(tk.END, str(line))
        self.scr_playlist.pack(side=tk.LEFT, fill=tk.BOTH)

        self.my_scroll.config(command=self.scr_playlist.yview)

        #  create the buttons
        self.frm_buttons = tk.Frame(master=self.root, bg="green", bd = 3, width=300, height=250)   # the main frame

        self.frm_grid = tk.Frame(master=self.frm_buttons, bg="blue")    # the grid frame that holds the buttons

        self.btn_play = tk.Button(master=self.frm_grid, text="play", font="80", width=8, command=self.play)
        self.btn_pause = tk.Button(master=self.frm_grid, text="pause", font="80", width=8, command=self.pause)
        self.btn_next = tk.Button(master=self.frm_grid, text="next", font="80", width=8, command=self.forward)
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

        print("hello world")


    # def play_song(self):
    #     # if self.player.get_current_song() != -1:
    #     result = self.scr_playlist.curselection()
    #     file_path = "./music/" + self.player.get_file_name(result[0])
    #     playsound(file_path)
    #     # print(self.player.get_song(result[0]))

    def play(self):
        if self.player.get_current_song() != -1:
            result = self.scr_playlist.curselection()   # get the selection that the user picked
            print("User option:", result)

            # if the user picked something then play the music
            if result != ():
                # checks if there is a song already playing
                if self.play_background.is_alive():
                    self.play_background.terminate()
                    # result = self.scr_playlist.curselection()
                    file_path = "./music/" + self.player.get_file_name(result[0])
                    
                    self.play_background = multiprocessing.Process(target=playsound, args=(file_path,), daemon=True)

                    self.play_background.start()

                # if there isn't a song currently playing
                else:
                    # result = self.scr_playlist.curselection()
                    file_path = "./music/" + self.player.get_file_name(result[0])
                    
                    self.play_background = multiprocessing.Process(target=playsound, args=(file_path,), daemon=True)

                    self.play_background.start()
            else:
                print("nothing was selected!")
                
        else:
            self.player.current_song=0
            print("Play button pressed")
        # print(self.player.get_song(result[0]))

    def pause(self):
        print("Pause button pressed")

    def shuffle(self):
        print("Shuffle button pressed")

    def forward(self):
        print("Forward button pressed")

    def backward(self):
        print("Backward button pressed")


if __name__ == "__main__":
    graphic = GUI()
