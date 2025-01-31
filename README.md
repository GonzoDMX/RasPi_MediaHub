# Intelligent Shelf Media Player

The Intelligent Shelf Media Player is a lightweight media server designed to run on a Raspberry Pi. It plays videos based on HTTP requests triggered when an object is placed on an intelligent shelf. When a valid request is received, the media player starts or stops video playback accordingly.

## Features
- Automatically plays a video when an object is detected on the intelligent shelf.
- Stops playback and returns to a splash screen when the object is removed.
- Runs as a media hub, processing commands via an HTTP server.
- Supports video playback from a structured directory system.
- Designed for Raspberry Pi with dependencies optimized for embedded systems.

## Installation
1. Clone the repository and `cd` into the root project directory.

2. Install the dependencies:

```sh
pip install -r requirements.txt
```

3. Prepare the media directories:
   - Store videos in `/media/<object_name>/` (e.g., `/media/book/video.mp4`).
   - Place a splash screen image in `/splash/` (e.g., `/splash/splash.jpg`).

## Usage
### Starting the Media Hub
Run the main script:
```sh
python main.py
```

### File Structure
```
/intelligent-shelf-media-player/
├── main.py                # Entry point
├── media_player.py        # Handles video playback
├── server.py              # HTTP server for receiving shelf events
├── utility.py             # Helper functions
├── config.py              # Configuration settings
├── /media/                # Directory for videos
│   ├── object1/           # Example object
│   │   ├── video.mp4
│   ├── object2/
│   │   ├── video.mp4
├── /splash/               # Directory for splash screen image
│   ├── splash.jpg
```

### How It Works
1. When an object is placed on the intelligent shelf, it sends an HTTP request.
2. The media server receives the request and checks if a corresponding directory exists in `/media/`.
3. If a valid video file is found, it starts playback.
4. When the object is removed (`state=false`), playback stops and the splash screen is displayed.

## API Requests
The server listens for HTTP POST requests containing JSON data with the following structure:
```json
{
  "state": "true",  # "true" to start video, "false" to stop
  "object": "book"  # Object name corresponding to a folder in /media
}
```

### Example Requests
#### Start Video Playback
```sh
curl -X POST http://<raspberry-pi-ip>:5000 -H "Content-Type: application/json" -d '{"state": "true", "object": "book"}'
```

#### Stop Video Playback
```sh
curl -X POST http://<raspberry-pi-ip>:5000 -H "Content-Type: application/json" -d '{"state": "false"}'
```

## Notes
- The media player requires valid video files in `/media/<object>/`.
- The splash screen must be an image file in `/splash/`.
- Designed to run on a Raspberry Pi, but can work on other Linux systems.

## Author
andrew.o-shei@sogeti.com


