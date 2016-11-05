from tkinter import *
import os
import subprocess
#import vlc
import time
import platform


def refresh_playlist_list():
    # listbox should be refreshable if I add media or extend with a usb path
    playlist = []
    try:
        for file in os.listdir(os.path.expanduser("~") + "/Playlists"):
            if file.endswith(".xspf"):
                playlist.append(file)
    except FileNotFoundError:
        playlist = ['No Playlist Found']
    return playlist


class Player:
    def __init__(self):
        global path
        global i
        i = vlc.Instance()
        path = os.path.expanduser("~") + "/Playlists"


class PiCarApp:
    def __init__(self):
        # Setup Tkinter App for PyCar
        self.root = Tk()
        self.content = Frame(self.root)
        self.root.resizable(width=False, height=False)
        self.root.geometry('800x480')
        self.root.title("PyCar Startup Program")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create GUI Widgets
        self.play_pause_var = Button(self.content, text="Play/Pause (>/||)", height=10, width=14, font="-weight bold -size 20", command=lambda: self.play_pause())
        self.last_song_var = Button(self.content, text="Last Song (|<)", height=10, width=14, font="-weight bold -size 20", command=lambda: self.last_song())
        self.next_song_var = Button(self.content, text="Next Song (>|)", height=10, width=14, font="-weight bold -size 20", command=lambda: self.next_song())
        self.random_var = Button(self.content, text="Randomize Off", height=10, width=14, font="-weight bold -size 20", command=lambda: self.toggle_random())
        self.repeat_var = Button(self.content, text="Repeat Off", height=10, width=14, font="-weight bold -size 20", command=lambda: self.toggle_repeat())
        self.volume = Scale(self.content, from_=0, to=100, orient=HORIZONTAL)
        self.volume.set(50)
        self.playlist_box = Listbox(self.content)

        # Insert Playlists into listbox widget
        for item in refresh_playlist_list():
            self.playlist_box.insert(0, item)

        # Position Widgets on GUI
        self.content.grid()
        self.play_pause_var.grid(column=3, row=6, rowspan=1)
        self.last_song_var.grid(column=2, row=6, rowspan=1)
        self.next_song_var.grid(column=4, row=6, rowspan=1)
        self.random_var.grid(column=5, row=6, rowspan=1)
        self.repeat_var.grid(column=6, row=6, rowspan=1)
        self.volume.grid(column=1, row=6, rowspan=1)
        self.playlist_box.grid(column=1, row=0, columnspan=2, rowspan=1)
        self.playbool = False
        self.root.mainloop()

    def callback(self):
        print("click!")

    def toggle_random(self):
        if self.random_var.config('text')[-1] == "Randomize Off":
            # Set VLC Random ON
            self.random_var.config(text="Randomize On")
        else:
            # Set VLC Random OFF
            self.random_var.config(text="Randomize Off")

    def toggle_repeat(self):
        if self.repeat_var.config('text')[-1] == "Repeat Off":
            # Set VLC Random ON
            self.repeat_var.config(text="Repeat On")
            #vlc.libvlc_media_list_player_set_playback_mode(p, "libvlc_playback_mode_loop")
        else:
            # Set VLC Random OFF
            self.repeat_var.config(text="Repeat Off")
            #vlc.libvlc_media_list_player_set_playback_mode(p, "libvlc_playback_mode_default")

    def play_pause(self):
        print("Play Pause Button Clicked")
        self.playbool = not self.playbool
        print(self.playbool)
        if self.playbool:
            file = path + "/" + str(self.playlist_box.get(ACTIVE))
            global l
            global p
            global media_list_player
            l = i.media_list_new()
            l.insert_media(i.media_new(file), 0)
            p = i.media_list_player_new()
            p.set_media_list(l)
            vlc.libvlc_media_list_player_play(p)
            # print(file)
            # proc1=subprocess.Popen(("cvlc "+str(file)), shell=True)
            # VLC player controls

        else:
            vlc.libvlc_media_list_player_stop(p)


    def next_song(self):
        print("Next Song Clicked")
        vlc.libvlc_media_list_player_next(p)

    def last_song(self):
            print("Last Song Clicked")
            vlc.libvlc_media_list_player_previous(p)
            #os.popen('pkill -f vlc')

# Main Loop
playbool=False
Player()
playlist = refresh_playlist_list()
PiCarApp()
