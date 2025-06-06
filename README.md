# Spotify Artwork Display

A Python application that displays real-time album artwork from your currently playing Spotify track using a simple Tkinter GUI.

## Features

- Real-time display of current Spotify track artwork
- Automatic updates when track changes
- Simple, clean interface
- Runs locally with your Spotify account

## Prerequisites

- Python 3.7+
- Spotify Premium account (required for real-time track info)
- Spotify Developer App credentials

## Setup

### 1. Spotify Developer Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note your `Client ID` and `Client Secret`
4. Add `http://localhost:8888/callback` as a redirect URI in your app settings

### 2. Installation

1. Clone this repository:
```bash
git clone https://github.com/greek891/spotiPI-artwork-display.git
cd spotiPI-artwork-display
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Spotify credentials:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## Usage

1. Make sure Spotify is running and playing music
2. Run the application:
```bash
python3 main.py
```
3. The first time you run it, you'll need to authorize the app in your browser
4. The artwork window will display your current track's album art

## Dependencies

- `spotipy` - Spotify Web API wrapper
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests for image downloading
- `Pillow` - Image processing
- `tkinter` - GUI (included with Python)

## Troubleshooting

- **"No client_id" error**: Make sure your `.env` file has the correct variable names
- **Authorization issues**: Check that your redirect URI matches exactly in both your Spotify app and `.env` file
- **No artwork displaying**: Ensure Spotify is actively playing music (not paused)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
