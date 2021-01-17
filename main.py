import os
import re
import random
from tkinter import *
import tkinter as tk
# import playsound
from playsound import playsound
import multiprocessing

PATH = "./music"


class Player:
    def __init__(self):
        self.playlist = []
        self.file_names = []
        self.current_song = -1
        self.library_size = 0

        self.get_music_library()

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
        
        # get the total amount of items in the library
        self.library_size = len(self.playlist)

    # fet the playlist variable
    def get_playlist(self):
        return self.playlist
    
    def get_song(self, index):
        return self.playlist[index]

    def get_file_name(self, index):
        return self.file_names[index]

    def get_current_song(self):
        return self.current_song
    
    def get_random_song(self):
        random.seed()
        index = random.randint(0, self.library_size-1)
        return index

    def set_current_song(self, num):
        self.current_song = num

    def get_library_size(self):
        return self.library_size



class GUI:
    def __init__(self):
        self.player = Player()
        # self.stop_play_thread=False

        # threads
        self.play_background = multiprocessing.Process(target=playsound, daemon=True)

        # making the window
        self.root = tk.Tk()
        self.root.geometry("300x500")
        self.root.title("Music Player")

        # create the music name label
        self.frm_song_name = tk.Frame(master=self.root, bg="#c2fff1", bd=3, height=250, width=300)

        # text in the label
        self.song_name = StringVar()
        self.song_name.set("Welcome!")

        self.lbl_song = tk.Label(master=self.frm_song_name, textvariable=self.song_name, bd=3 ,font="Arial 12")

        self.lbl_song.pack(fill=tk.BOTH, pady=3)

        self.frm_song_name.pack(expand=True, fill=tk.BOTH)

        # create a playlist list
        self.my_scroll = tk.Scrollbar(master=self.frm_song_name)
        self.my_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=2)

        self.scr_playlist = tk.Listbox(master=self.frm_song_name, yscrollcommand=self.my_scroll.set, width=40, bd=4, relief=tk.FLAT)
        for line in self.player.get_playlist():
            self.scr_playlist.insert(tk.END, str(line))
        self.scr_playlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=2)

        self.my_scroll.config(command=self.scr_playlist.yview)

        #  create the buttons
        self.frm_buttons = tk.Frame(master=self.root, bg="#c2fff1", bd = 3, width=300, height=250)   # the main frame

        self.frm_grid = tk.Frame(master=self.frm_buttons, bg="#c2fff1")    # the grid frame that holds the buttons

        self.btn_play = tk.Button(master=self.frm_grid, text="Play", font="Arial 12", width=8, command=self.play, relief=tk.RAISED)
        self.btn_stop = tk.Button(master=self.frm_grid, text="Stop", font="Arial 12", width=8, command=self.stop, relief=tk.RAISED)
        self.btn_next = tk.Button(master=self.frm_grid, text="Next", font="Arial 12", width=8, command=self.forward, relief=tk.RAISED)
        self.btn_back = tk.Button(master=self.frm_grid, text="Back", font="Arial 12", width=8, command=self.backward, relief=tk.RAISED)
        self.btn_shufful = tk.Button(master=self.frm_grid, text="Shufful", font="Arial 12", width=8, command=self.shuffle, relief=tk.RAISED)

        self.btn_play.grid(row=1, column=2)
        self.btn_stop.grid(row=3, column=2)
        self.btn_next.grid(row=2, column=3)
        self.btn_back.grid(row=2, column=1)
        self.btn_shufful.grid(row=2, column=2, padx=3, pady=3)

        self.frm_grid.pack(expand=True)
        self.frm_buttons.pack(expand=True, fill=tk.BOTH)
        

        self.root.mainloop()

    def play(self):

        result = self.scr_playlist.curselection()   # get the selection that the user picked

        # if the user picked something then play the music
        if result != ():

            # get the file path for the audio file
            file_path = "./music/" + self.player.get_file_name(result[0])

            # checks if there is a song already playing, stop it
            if self.play_background.is_alive():
                self.play_background.terminate()
                            
            # set the selected song as the current song
            self.player.set_current_song(result[0])

            # get song name
            name = self.player.get_song(self.player.get_current_song())
            self.song_name.set(name)

            # play the audio file
            self.play_background = multiprocessing.Process(target=playsound, args=(file_path,), daemon=True)
            self.play_background.start()

        else:
            print("nothing was selected!")

    def stop(self):
        if self.play_background.is_alive():
            self.play_background.terminate()
            self.song_name.set("Music Stopped")

    # plays a random song
    def shuffle(self):
        self.play_song(self.player.get_random_song())

    # plays the next song listed
    def forward(self):
        if self.player.get_current_song() != self.player.get_library_size()-1:
            self.play_song(self.player.get_current_song()+1)
        else:
            self.play_song(0)

    # plays the last song listed
    def backward(self):
        if self.player.get_current_song() != 0: # if the current song isn't the first one in the list
            self.play_song(self.player.get_current_song()-1)
        else:   # if the current song is the first one in the list
            self.play_song(self.player.get_library_size()-1)

    # helper song
    def play_song(self, index):
        song_index = index

        # get the file path for the audio file
        file_path = "./music/" + self.player.get_file_name(song_index)

        # set this song as the current song
        self.player.set_current_song(song_index)

        # checks if there is a song already playing, stop it
        if self.play_background.is_alive():
            self.play_background.terminate()
                        
        # get song name
        name = self.player.get_song(song_index)
        self.song_name.set(name)

        # play the audio file
        self.play_background = multiprocessing.Process(target=playsound, args=(file_path,), daemon=True)
        self.play_background.start()


if __name__ == "__main__":
    graphic = GUI()
