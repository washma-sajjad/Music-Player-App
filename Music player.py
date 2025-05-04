import os
import pygame
from tkinter import Tk, Button, filedialog, Label, Listbox, Menu, Canvas
from PIL import Image, ImageTk  # For image handling

# Initialize Pygame's mixer for audio playback
pygame.mixer.init()

# Class representing a Song
class Song:
    def __init__(self, file_path):
        self.file_path = file_path
        self.title = os.path.basename(file_path)
        self.duration = "Unknown"  # Placeholder for duration (can use mutagen for real metadata)

    def get_details(self):
        return f"Title: {self.title}, Duration: {self.duration}"

# Class representing the Music Player
class MusicPlayer:
    def __init__(self):
        self.current_song = None
        self.is_playing = False
        self.is_paused = False

    def play_song(self, song):
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.is_playing = True
                print(f"Resumed: {song.title}")
            else:
                self.current_song = song
                pygame.mixer.music.load(song.file_path)
                pygame.mixer.music.play()
                self.is_playing = True
                print(f"Playing: {song.title}")
        except pygame.error as e:
            print(f"Error playing song: {e}")

    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            print("Paused song.")

    def stop_song(self):
        if self.current_song:
            pygame.mixer.music.stop()
            self.is_paused = False
            self.is_playing = False
            print("Stopped song.")

    def rewind_song(self):
        if self.current_song:
            pygame.mixer.music.rewind()
            print("Rewound song.")

    def forward_song(self, seconds=10):
        if self.current_song:
            current_pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.play(start=current_pos + seconds)
            print(f"Forwarded song by {seconds} seconds.")

# Class representing the GUI
class GUI:
    def __init__(self, music_player):
        self.music_player = music_player
        self.app = Tk()
        self.app.title("Music Player")
        self.app.geometry("600x500")

        self.song_objects = []
        self.current_album_art = None  # To keep track of album art for the current song

        # Paths for box backgrounds
        self.boxes_folder = r"C:\Users\Maheen\Desktop\Music Player Application\Boxes"
        self.now_playing_bg_path = os.path.join(self.boxes_folder, "nowplaying_display .png")  # Fixed path
        self.songs_list_bg_path = os.path.join(self.boxes_folder, "songs_display.png")
        self.icons_bg_path = os.path.join(self.boxes_folder, "icons_display.png")

        # Setup background and UI components
        self.setup_ui()

    def load_image(self, path, size):
        """Helper function to load and resize images."""
        if os.path.exists(path):
            image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        else:
            print(f"Error: File not found - {path}")
            return None

    def setup_ui(self):
        # Load the main background image
        background_image_path = os.path.join(os.path.dirname(__file__), 'Background', 'background.png')
        self.bg_image = self.load_image(background_image_path, (600, 500))
        if self.bg_image:
            self.canvas = Canvas(self.app, width=600, height=500)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Add "Now Playing" box with background
        self.now_playing_bg = self.load_image(self.now_playing_bg_path, (400, 80))
        if self.now_playing_bg:
            self.canvas.create_image(300, 60, image=self.now_playing_bg)

        self.song_title_label = Label(self.app, text="No Song Loaded", font=("Calibri", 16), bg="white")
        self.canvas.create_window(300, 60, window=self.song_title_label)

        # Add "Songs List" box with background
        self.songs_list_bg = self.load_image(self.songs_list_bg_path, (500, 200))
        if self.songs_list_bg:
            self.canvas.create_image(300, 220, image=self.songs_list_bg)

        self.song_listbox = Listbox(self.app, bg="lightgray", fg="black", width=50, height=12)
        self.canvas.create_window(300, 220, window=self.song_listbox)

        # Add "Icons" box with background
        self.icons_bg = self.load_image(self.icons_bg_path, (500, 80))
        if self.icons_bg:
            self.canvas.create_image(300, 420, image=self.icons_bg)

        # Load control buttons
        self.load_buttons()

    def load_buttons(self):
        icons_folder = r"C:\Users\Dell\Downloads\python\Music Player Application\Icons"

        # Paths to icons
        play_icon_path = os.path.join(icons_folder, 'play_transparent.png')
        pause_icon_path = os.path.join(icons_folder, 'pause_transparent.png')
        rewind_icon_path = os.path.join(icons_folder, 'rewind_transparent.png')
        forward_icon_path = os.path.join(icons_folder, 'forward_transparent.png')

        try:
            # Load and resize icons
            play_icon = self.load_image(play_icon_path, (50, 50))
            pause_icon = self.load_image(pause_icon_path, (50, 50))
            rewind_icon = self.load_image(rewind_icon_path, (50, 50))
            forward_icon = self.load_image(forward_icon_path, (50, 50))

            # Buttons
            if play_icon:
                play_button = Button(self.app, image=play_icon, command=self.play_selected_song, bd=0, bg="white")
                play_button.image = play_icon
                self.canvas.create_window(150, 420, window=play_button)
            if pause_icon:
                pause_button = Button(self.app, image=pause_icon, command=self.pause_song, bd=0, bg="white")
                pause_button.image = pause_icon
                self.canvas.create_window(250, 420, window=pause_button)
            if rewind_icon:
                rewind_button = Button(self.app, image=rewind_icon, command=self.rewind_song, bd=0, bg="white")
                rewind_button.image = rewind_icon
                self.canvas.create_window(350, 420, window=rewind_button)
            if forward_icon:
                forward_button = Button(self.app, image=forward_icon, command=lambda: self.music_player.forward_song(10), bd=0, bg="white")
                forward_button.image = forward_icon
                self.canvas.create_window(450, 420, window=forward_button)

        except Exception as e:
            print(f"Error loading icons: {e}")

    def load_songs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        for file_path in file_paths:
            song = Song(file_path)
            self.song_objects.append(song)
            self.song_listbox.insert("end", song.title)
        print(f"Loaded {len(file_paths)} songs.")

    def play_selected_song(self):
        selected_index = self.song_listbox.curselection()
        if selected_index:
            selected_song = self.song_objects[selected_index[0]]
            self.music_player.play_song(selected_song)
            self.song_title_label.config(text=f"Playing: {selected_song.title}")

    def pause_song(self):
        self.music_player.pause_song()

    def rewind_song(self):
        self.music_player.rewind_song()

    def run(self):
        menu_bar = Menu(self.app)
        self.app.config(menu=menu_bar)

        add_songs_menu = Menu(menu_bar, tearoff=False)
        add_songs_menu.add_command(label="Add Songs", command=self.load_songs)
        menu_bar.add_cascade(label="File", menu=add_songs_menu)

        self.app.mainloop()

# Run the application
if __name__ == "__main__":
    music_player = MusicPlayer()
    gui = GUI(music_player)
    gui.run()





import pygame 
class player(pygame.sprite.Sprite):
    rect = None
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -=5
        if keys[pygame.K_RIGHT]:
            self.rect.x +=5
        if keys[pygame.K_UP]:
            self.rect.y -=5
        if keys[pygame.K_DOWN]:
            self.rect.y +=5 

class game:
    screen = None
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("OOP PYGAME") 
        self.clock = pygame.time.Clock()
        self.running = True

        self.plyr  = player(400,300)
        self.all_sprites = pygame.sprite.Group(self.plyr)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.all_sprites.update(keys)

            self.screen.fill((255,255,255)) 
            self.all_sprites.draw(self.screen)       
            pygame.display.flip()

            self.clock.tick(60)

    pygame.quit()

game1 = game()
game1.run()                



