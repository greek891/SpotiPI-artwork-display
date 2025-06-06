import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image, ImageTk
import io
import tkinter as tk
import threading
import time
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials - you'll need to set these up
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Scopes needed to read currently playing track
SCOPE = "user-read-currently-playing user-read-playback-state"


def setup_spotify_client():
    """Initialize and return Spotify client with OAuth"""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    ))


def get_current_track_artwork(sp):
    """Get the artwork URL of the currently playing track"""
    try:
        # Get currently playing track
        current_track = sp.current_user_playing_track()

        if current_track is None:
            return None

        if current_track['item'] is None:
            return None

        # Extract track information
        track = current_track['item']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        # Get album artwork (images are sorted by size, largest first)
        images = track['album']['images']
        if not images:
            return None

        # Get the largest image (first in the list)
        artwork_url = images[0]['url']

        return {
            'url': artwork_url,
            'track_name': track_name,
            'artist_name': artist_name
        }

    except Exception as e:
        print(f"Error getting current track: {e}")
        return None


class SpotifyArtworkDisplay:
    def __init__(self):
        self.sp = None
        self.current_artwork_url = None
        self.setup_gui()
        self.setup_spotify()

    def setup_gui(self):
        """Initialize the tkinter GUI for full artwork display"""
        self.root = tk.Tk()
        self.root.title("Spotify Artwork")
        self.root.geometry("720x720")
        self.root.resizable(False, False)
        self.root.configure(bg='black')

        # Remove window decorations for a cleaner look (optional)
        # self.root.overrideredirect(True)

        # Artwork display - fill the entire window
        self.artwork_label = tk.Label(self.root, bg='black')
        self.artwork_label.pack(fill='both', expand=True)

        # Set up key bindings for control
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.bind('<space>', lambda e: self.refresh_artwork())
        self.root.focus_set()

    def setup_spotify(self):
        """Initialize Spotify client in a separate thread"""
        def init_spotify():
            try:
                self.sp = setup_spotify_client()
                self.refresh_artwork()
                self.start_auto_refresh()
            except Exception as e:
                print(f"Spotify connection error: {e}")

        threading.Thread(target=init_spotify, daemon=True).start()

    def refresh_artwork(self):
        """Refresh the current track artwork"""
        if not self.sp:
            return

        def fetch_artwork():
            try:
                artwork_info = get_current_track_artwork(self.sp)

                if artwork_info:
                    # Only update if it's a different track
                    if self.current_artwork_url != artwork_info['url']:
                        self.current_artwork_url = artwork_info['url']
                        self.display_artwork(artwork_info)
                        print(f"Now playing: {artwork_info['track_name']} by {artwork_info['artist_name']}")

            except Exception as e:
                print(f"Error fetching artwork: {e}")

        threading.Thread(target=fetch_artwork, daemon=True).start()

    def display_artwork(self, artwork_info):
        """Download and display artwork at full 720x720 size"""
        try:
            # Download image
            response = requests.get(artwork_info['url'])
            response.raise_for_status()

            # Open image with PIL
            image = Image.open(io.BytesIO(response.content))

            # Resize to exactly 720x720 (stretching if necessary to fill window)
            image = image.resize((720, 720), Image.Resampling.LANCZOS)

            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(image)

            # Update GUI in main thread
            self.root.after(0, lambda: self.artwork_label.config(image=photo))
            self.root.after(0, lambda: setattr(self.artwork_label, 'image', photo))  # Keep reference

        except Exception as e:
            print(f"Error displaying artwork: {e}")

    def start_auto_refresh(self):
        """Start auto-refresh in background thread"""
        def auto_refresh_loop():
            while True:
                time.sleep(.6)
                self.refresh_artwork()

        threading.Thread(target=auto_refresh_loop, daemon=True).start()

    def run(self):
        """Start the GUI application"""
        print("Spotify Artwork Display started")
        print("Press SPACE to manually refresh")
        print("Press ESCAPE to quit")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


if __name__ == "__main__":
    app = SpotifyArtworkDisplay()
    app.run()