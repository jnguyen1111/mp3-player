import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import random , os , threading , time , sys , pyglet

class Mp3_player:
    #formats the time of song depending by hours minutes and seconds
    def song_timeformat(self):
        # section below defines song time conversion
        length_song_hour = self.length // 3600
        self.length %= 3600
        length_song_minute = self.length // 60
        self.length %= 60
        length_song_second = self.length
        current_hour = self.current_time_converter // 3600
        self.current_time_converter %= 3600
        current_minute = self.current_time_converter // 60
        self.current_time_converter %= 60
        current_sec = self.current_time_converter

        # formating for songs less than an hour
        if length_song_hour == 0:
            if current_sec < 10:                            #handles the seconds current time of song displayed on the left hand side
                current_sec = str(current_sec).zfill(2)
                int(current_sec)
            if length_song_second < 10:                     #handles the second of the song length displayed on the right hand side
                length_song_second = str(length_song_second).zfill(2)
                int(length_song_second)
            self.time_playback.set(self.current_audio_time)
            self.song_time['text'] = "track  length    {}:{}/{}:{}".format(current_minute, current_sec,length_song_minute, length_song_second)

        # formating for songs that are an hour or greater
        elif length_song_hour > 0:
            if current_sec < 10:
                current_sec = str(current_sec).zfill(2)
                int(current_sec)
            if current_minute < 10:
                current_minute = str(current_minute).zfill(2)
                int(current_minute)
            if length_song_second < 10:
                length_song_second = str(length_song_second).zfill(2)
                int(length_song_second)
            if length_song_minute < 10:
                length_song_minute = str(length_song_second).zfill(2)
                int(length_song_minute)
            self.time_playback.set(self.current_audio_time)
            self.song_time['text'] = "track  length    {}:{}:{}/{}:{}:{}".format(current_hour, current_minute,current_sec, length_song_hour,length_song_minute, length_song_second)

    #Function is used when there is an error loading the song it reloads it and replays it
    def reload_song(self):
        self.terminate_thread = True                    # destroys the thread to be reseted
        self.media_player_object.delete()
        self.media_player_object = pyglet.media.Player()
        self.volume_scale.set(.10)
        self.media_player_object.volume = .10
        time.sleep(.03)  # make sures song plays properly without no hitches
        self.update_song()

    def no_playlist(self):
        tk.messagebox.showerror(title="Error", message="Error, please load a playlist first.")

    # loads/updates  song that is chosen or played next
    def update_song(self):
        try:
            self.parse_song_file = self.song_list[self.index]
            self.audio_source_object = pyglet.media.load(self.music_folder_directory + "/" + self.parse_song_file)          # defines the absolute path to the song
            self.media_player_object.next_source()                                                                          # clears current song if any
            self.media_player_object.queue(self.audio_source_object)                                                        # queues audio source file to be played

            # label below and place method clears title by updating with empty string which clears the previous song and load new song title
            self.song_title = tk.Label(text='                                                                                                                                                                                                                              ',background = self.background_color,width = 100,foreground =self.background_color)
            self.song_title.place(x=267, y=15, anchor="center")
            self.song_title = tk.Label(text=self.parse_song_file, background = self.background_color, width = 100, height = 2, foreground = self.text_color, font ="Arial 8 bold")
            self.song_title.place(x=267, y=15, anchor="center")
            self.play()
        except IndexError:
            pass

    #loops the current song when the user presses the key/button to loop song
    def loop_song(self):
        self.loop_state = True
        if not self.is_playlist_loaded:                                         #checks to see if the user even loaded the playlist first
            self.no_playlist()
        elif self.is_playlist_loaded:
            if self.loop_message:
                tk.messagebox.showinfo(title="Sucess", message="Song has been looped.")
                self.loop_message = False  # set to false so messagebox above does not appear after first click
            self.status_bar["text"] = "Status: Playing"
            self.update_song()

    #shuffles songs list and set index at 0
    def shuffle_music(self):
        self.loop_message = True                                                         # reset loop message so that when loop_song() called message appears
        self.loop_state = False                                                          # set false to not loop song
        if not self.is_playlist_loaded:                                                  # if playlist isnt loaded shows error message for all buttons
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.terminate_thread = True                                                 # terminate threads not in use
            random.shuffle(self.song_list)
            self.index = 0
            self.status_bar["text"] = "Status: Playing"
            self.update_song()

    # adjust  index by -1
    def previous_song(self):
        self.loop_message = True
        self.loop_state = False
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.terminate_thread = True                                                # clears previous threads that were created by returning none
            self.index -= 1
            if self.index == -(len(self.song_list) + 1):                                    # if index of song reaches more than its max index set index to -1
                self.index = -1
            self.status_bar["text"] = "Status: Playing"
            self.update_song()

    # adjust index  by +1
    def next_song(self):
            self.loop_message = True
            self.loop_state = False
            if not self.is_playlist_loaded:
                self.no_playlist()
            elif self.is_playlist_loaded:
                self.terminate_thread = True
                self.index += 1
                if self.index == len(self.song_list):                                 # if index of song reaches more than its max index set index to 0
                    self.index = 0
                self.status_bar["text"] = "Status: Playing"
                self.update_song()

    # loads playlist and sets shortcut keys to be functional and sets the default volume at 25
    def load_playlist(self):
        try:
            self.loop_message = True
            self.is_playlist_loaded = True
            self.index = 0
            self.song_list = []
            self.status_bar["text"] = "Status: Playing"
            if self.changing_playlist:  #if we are changing a new playlist, delete the music player object to reset it
                self.media_player_object.delete()
            self.music_folder_directory = tk.filedialog.askdirectory()    #asks for a playlist folder path
            self.song_list = os.listdir(self.music_folder_directory)      #obtains the folder path and makes a list for music files
            self.media_player_object = pyglet.media.Player()
            self.volume_scale.set(25)
            self.media_player_object.volume = .25
            self.changing_playlist = True  # when you change a playlist it deletes the player to make sure two songs do not play simultaneously
            self.update_song()
        #if file type is not valid dont update the title and dont make the key/button functionable
        except FileNotFoundError:
            self.loop_message = False
            self.is_playlist_loaded = False
            self.status_bar["text"] = "Status: None"

    # loads a specific song from playlist chosen cannot be another song file from another playlist throws error
    def load_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            try:
                self.loop_state = False
                self.loop_message = True
                self.open_file = tk.filedialog.askopenfile()
                self.parse_song_file = str(self.open_file.name)
                self.parse_song_file = self.parse_song_file.split("/")
                self.song_track = self.parse_song_file[-1]  # picks out title of song
                if self.song_track in self.song_list:
                    self.index = self.song_list.index(
                        self.song_track)  # if user picks specific song, index changes to specific index of list if exists in song list
                    self.status_bar["text"] = "Status: Playing"
                    self.update_song()
                elif self.song_track not in self.song_list:
                    tk.messagebox.showerror(title="Error",message="Error, file picked is invalid or not in playlist please try again.")
            except AttributeError:
                pass
            except PermissionError:
                tk.messagebox.showerror(title="Error",message="Error, file picked is invalid or not in playlist please try again.")

    def resume_song(self):
        if not self.is_playlist_loaded: # check if playlist is loaded
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.status_bar["text"] = "Status: Resumed"
            self.media_player_object.play()

    def pause_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.status_bar["text"] = "Status: Paused"
            self.media_player_object.pause()

    def play(self):
        try:
            self.media_player_object.play()
            self.thread_task = threading.Thread(target=self.check_end_of_song)  # start checking for end of song condition by initializing a thread
            self.thread_task.start()
            # whenever the player has problems remake the audio player code portion below
            if self.media_player_object.playing == False:
                self.reload_song()
        except ValueError:
            self.reload_song()

    def quit(self):
        self.quit_program = True  # "destroys" threads by returning in a function to end them in order to properly shutdown the application window
        self.window.destroy()

    # finds specific position of the  volume scale  , volume range is 0.0(mute) -> 1.0(max volume)
    def volume_adjust(self,delta):
        try:
            self.volume_level_delta = int(delta) / 100
            self.media_player_object.volume = self.volume_level_delta
        except AttributeError:
            pass

    # updates the song track time when user moves scales to a certain point of the song
    #event variable is needed here
    def update_song_time(self, event = None):
        try:
            self.song_time_bar_value = self.time_playback.get()     # obatins value of the scale when user releases scale
            self.time_playback.set(int(self.song_time_bar_value))
            self.media_player_object.seek(int(self.song_time_bar_value))
            self.media_player_object.pause()
            time.sleep(.06)
            self.media_player_object.play()
        except AttributeError:
            pass

    # when song has ended, if loop_state is false, the next song plays
    def auto_play_next(self):
        self.time_playback.set(0)
        self.terminate_thread = False
        self.status_bar["text"] = "Status: Playing"
        self.index += 1
        if self.index == len(self.song_list):  # when end index reached restart at index 0
            self.index = 0
        self.update_song()

    #this is the thread function which runs a loop to check for the end of the song
    def check_end_of_song(self):
        self.time_playback["to"] = int(self.audio_source_object.duration)  # defines scale of song length
        if self.terminate_thread or threading.active_count() > 2:  # terminate threads that are not in use when you shuffle,play next/previous etc
            self.terminate_thread = False
            return None
        elif not self.terminate_thread:
            while True:
                time.sleep(1)
                # length(defines song length)  current time(current time in song) below
                self.length = int(self.audio_source_object.duration)
                self.current_audio_time = int(self.media_player_object.time)
                self.current_time_converter = self.current_audio_time
                if self.quit_program:  # quits threads when quit condition is true and exits application
                    return None
                if self.current_time_converter == self.length + 1 or self.current_time_converter == self.length + 2:   #when the song reaches the end condition or past it
                    self.is_paused = False  #defines and interacts with pause button
                    break                   #break out of loop and determine what should be done next loop or play next song

                #obtain song time length format
                self.song_timeformat()

            if self.loop_state:
                self.loop_song()
            elif not self.loop_state:
                self.auto_play_next()

    #a function that is called to change theme color
    def change_button_color(self):
        self.load_song_button["bg"] = self.button_color
        self.load_playlist_button["bg"] = self.button_color
        self.pause_button["bg"] = self.button_color
        self.resume_button["bg"] = self.button_color
        self.shuffle_button["bg"] = self.button_color
        self.next_button["bg"] = self.button_color
        self.previous_button["bg"] = self.button_color
        self.loop_button["bg"] = self.button_color
        self.volume_scale["bg"] = self.background_color
        self.time_playback["bg"] = self.background_color
        self.song_title["bg"] = self.background_color
        self.load_song_button["foreground"] = self.text_color
        self.load_playlist_button["foreground"] = self.text_color
        self.pause_button["foreground"] = self.text_color
        self.resume_button["foreground"] = self.text_color
        self.shuffle_button["foreground"] = self.text_color
        self.next_button["foreground"] = self.text_color
        self.previous_button["foreground"] = self.text_color
        self.status_bar["foreground"] = self.text_color
        self.loop_button["foreground"] = self.text_color
        self.volume_text["foreground"] = self.text_color
        self.volume_scale["foreground"] = self.text_color
        self.time_playback["foreground"] = self.text_color
        self.song_time["foreground"] = self.text_color
        self.song_title["foreground"] = self.text_color
        self.status_bar["background"] = self.button_color
        self.song_time["background"] = self.background_color
        self.volume_text["background"] = self.background_color
        self.window['background'] = self.background_color
        self.volume_scale["troughcolor"] = self.trough_color
        self.time_playback["troughcolor"] = self.trough_color

    #changes the gui color scheme with a press of a shortcut key
    def dark_light_mode(self):
        if self.dark_mode == True:  # turns off dark mode
            self.button_color = "#F0F0F0"
            self.background_color = "#FFFFFF"
            self.trough_color = "#F5F5F5"
            self.text_color = "#000000"
            self.dark_mode = False
            self.change_button_color()

        elif self.dark_mode == False:   # turns on dark mode
            self.button_color = "#383838"
            self.background_color = "#282828"
            self.trough_color = "#808080"
            self.text_color = "#FFFFFF"
            self.dark_mode = True
            self.change_button_color()

    def key_press(self, event):
        self.key_event_listener = str(event.char)
        if self.key_event_listener == 'q':
            if tk.messagebox.askyesno(title="Quit", message="Do you wish to quit?"):
                self.quit()
        else:
            if not self.is_playlist_loaded:
                if self.key_event_listener == 'w':  # allows playlist to be loaded first
                    self.load_playlist()
                elif self.key_event_listener == 'd'  or self.key_event_listener == 'o' or self.key_event_listener == 'e' or self.key_event_listener == 's' or self.key_event_listener == 'i' or self.key_event_listener == '.' or self.key_event_listener == ',' or self.key_event_listener == "p":
                    self.no_playlist()   # if other keys are pressed and there no playlist pop up error message
                else:
                    pass                 #ignore all other keybinds that are not binded
            elif self.is_playlist_loaded:
                if self.key_event_listener == 'w':
                    self.load_playlist()
                elif self.key_event_listener == 'o':
                    self.next_song()
                elif self.key_event_listener == 'i':
                    self.previous_song()
                elif self.key_event_listener == 'e':
                    self.load_song()
                elif self.key_event_listener == 's':
                    self.shuffle_music()
                elif self.key_event_listener == "":        # key is crtl + z for changing dark/light modes
                    self.dark_light_mode()
                elif self.key_event_listener == 'd':
                    self.loop_song()
                # player volume below chunks increase/decrease volume by 5 and defines the range of vol scale
                elif self.key_event_listener == '.':
                    self.media_player_object.volume += (5 / 100)
                    self.volume_scale.set(self.media_player_object.volume * 100)
                    if self.media_player_object.volume >= 1.0:
                        self.media_player_object.volume = 1.0
                elif self.key_event_listener == ',':
                    self.media_player_object.volume -= (5 / 100)
                    self.volume_scale.set(self.media_player_object.volume * 100)
                    if self.media_player_object.volume <= 0.0:
                        self.media_player_object.volume = 0
                # play/pause chunk
                elif self.key_event_listener == "p" and self.is_paused == False:
                    self.is_paused = True
                    self.status_bar["text"] = "Status: Paused"
                    self.media_player_object.pause()
                elif self.key_event_listener == "p" and self.is_paused == True:
                    self.is_paused = False
                    self.status_bar["text"] = "Status: Playing"
                    self.media_player_object.play()
                else:
                    pass

    # defines the properties of application window
    def __init__(self,window):
        self.index = 0
        self.music_folder_directory = None  # grabs path of music folder/playlist containing songs
        self.song_file = None  # chooses mp3 file
        self.song_title = None  # Displays the song title to the GUI
        self.song_list = None  # contains all mp3 files in the music folder
        self.song_track = None  # Grabs name of the song when user requests to load a song from the current playlist
        self.parse_song_file = None  # When user requests to load a specific song, it takes the current song file and parses into a list so the title can be grabbed by song track

        self.length = None  # Grabs Song duration from audio source object variable
        self.current_audio_time = None  # Grabs the current time the audio is currently playing
        self.current_time_converter = None  # Copies from current audio time to be able to parse and convert time to be displayed to the gui

        self.open_file = None  # provides a gui window explorer to allow user to choose a specific song and access its info
        self.is_playlist_loaded = False  # boolean flag helps handles error handling such as pressing buttons/keyboard shortcuts before anything is loaded
        self.is_paused = False  # defines pause and play condition

        self.loop_state = False
        self.loop_message = True  # loop messagebox when true it shows info box when song is looped
        self.volume_level_delta = None  # controls the volume level for media player
        self.quit_program = False  # quit condition

        self.audio_source_object = None  # holds the information of  audio source/file loaded from pyglet media player
        self.media_player_object = None  # contains pyglet media player object
        self.key_event_listener = None  # Event listeners listens for specific key presses from user and acts accordingly to rules

        # threading variables
        self.thread_task = None  # contains reference to thread/task started
        self.terminate_thread = False  # when terminate_thread = True we get rid of threads we dont use

        self.song_time_bar_value = None                 #obtains the current time in audio from the time bar
        self.changing_playlist = False                  # when we change a new playlist, we delete the player and make a new one
        self.dark_mode = True                           # changes light/dark mode of mp3 player

        #defines the color and font that will be used for buttons and titles
        self.button_color = "#383838"
        self.background_color = "#282828"
        self.trough_color = "#808080"
        self.text_color = "#FFFFFF"
        self.font = "ProximaNova 9 bold"

        self.window = window
        self.window['background'] = self.background_color
        self.window.title("Vibe Player")
        self.window.iconbitmap("sadcat.ico")
        self.window.geometry("585x200")

        #asisgns the buttons properties and command funcitons
        self.load_song_button = tk.Button(window, text="Load specific song from playlist", height=1, width=30,command=self.load_song, borderwidth=1, bg=self.button_color,foreground=self.text_color, font=self.font, relief="solid")
        self.load_playlist_button = tk.Button(window, text="Load playlist", height=1, width=16,command=self.load_playlist, borderwidth=1, bg=self.button_color,foreground=self.text_color, font=self.font, relief="solid")
        self.pause_button = tk.Button(window, text="Pause", height=1, width=16, command=self.pause_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.resume_button = tk.Button(window, text="Resume", height=1, width=16, command=self.resume_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.shuffle_button = tk.Button(window, text="Shuffle", height=1, width=16, command=self.shuffle_music,borderwidth=1, bg=self.button_color, foreground=self.text_color, font=self.font,relief="solid")
        self.next_button = tk.Button(window, text="Next", height=1, width=15, command=self.next_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.previous_button = tk.Button(window, text="Previous", height=1, width=16, command=self.previous_song,borderwidth=1, bg=self.button_color, foreground=self.text_color, font=self.font,relief="solid")
        self.loop_button = tk.Button(window, text="Loop song", height=1, width=16, command=self.loop_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.song_time = tk.Label(window, text="track  length    0:00/0:00", background=self.background_color,width=100, foreground=self.text_color, font=self.font)
        self.volume_scale = tk.Scale(window, from_=100, to=0, orient=tk.VERTICAL, length=110, resolution=1,command=self.volume_adjust, bg=self.background_color, foreground="white",highlightthickness=0, troughcolor="#808080", font=self.font, sliderlength=10,width=10)
        self.volume_text = tk.Label(text="Volume", bg=self.background_color, foreground="white", font=self.font)
        self.time_playback = tk.Scale(window, from_=0, orient=tk.HORIZONTAL, length=400, resolution=1,bg=self.background_color, foreground="white", highlightthickness=0,troughcolor=self.trough_color, sliderlength=5, width=8, showvalue=0)
        self.status_bar = tk.Label(text="Status: None ", bg=self.button_color, foreground=self.text_color, font=self.font, width=200)

        #handles listening keyboard key presses follows rules implemented for specific key presses
        self.time_playback.bind("<ButtonRelease-1>",self.update_song_time)  # event occurs when scale bar of song length is released
        self.window.bind('<Key>', self.key_press)  # event occurs when buttons/keys are pressed

        #position where the buttons will be at
        self.song_time.place(x=260, y=40, anchor="center")
        self.time_playback.place(x=260, y=67, anchor="center")
        self.pause_button.place(x=78, y=95, anchor="center")
        self.resume_button.place(x=204, y=95, anchor="center")
        self.previous_button.place(x=330, y=95, anchor="center")
        self.next_button.place(x=452, y=95, anchor="center")
        self.shuffle_button.place(x=260, y=125, anchor="center")
        self.loop_button.place(x=385, y=125, anchor="center")
        self.load_playlist_button.place(x=135, y=125, anchor="center")
        self.load_song_button.place(x=260, y=155, anchor="center")
        self.volume_scale.place(x=535, y=90, anchor="center")
        self.volume_text.place(x=570, y=157, anchor="e")
        self.status_bar.place(x=50, y=180, anchor="n")

# Start of the program
if __name__ == "__main__":
    # creation of application window
    applic_window = tk.Tk()
    applic_window.resizable(width=False, height=False)
    mmedia = Mp3_player(applic_window)
    def on_exit():
        if tk.messagebox.askyesno(title="Quit", message="Do you wish to quit?"): # quit when clicking red x button and call protocal to sys.exit()
            mmedia.quit()  #destroys threads specific to the program and destroy the window
            exit()
    applic_window.protocol("WM_DELETE_WINDOW",on_exit)   #defines what happens when user closes window using window manager
    applic_window.mainloop()    # call mainloop of tk
    sys.exit()
