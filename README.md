## 🎵 ThemeDownloader-Docker

A containerized Python script (Docker/Alpine) designed for media server administrators (Plex, Jellyfin, Emby). It scans your TV series folders, identifies missing theme songs, and automatically downloads them from YouTube.
The script is lightweight, flexible via environment variables, and uses **yt-dlp** and **FFmpeg** to ensure clean, compliant `theme.mp3` files.

-----

### ✨ Key Features

  * **Automatic Check:** Recursive scan of subfolders to check for the presence of the `theme.mp3` file.
  * **Smart Naming Cleanup:** Automatic extraction of the clean series name from common naming formats (with or without year, with or without TVDB ID).
  * **Audio Download:** Uses `yt-dlp` to search YouTube for the series theme song.
  * **Duration Control:** Configurable limit to avoid downloading long audio compilations or full videos.
  * **Isolated Deployment:** Runs via Docker on an ultra-lightweight **Alpine** base, integrating all dependencies (Python, `yt-dlp`, FFmpeg).

### 🛠️ Prerequisites

To use this project, you need:

1.  **Docker** installed on your host server.
2.  The `main.py` script (environment variable version) and the `Dockerfile` at the root of your GitHub repository.

### ⚙️ Supported Naming Conventions

The script uses a regular expression (`regex`) to clean the folder name and use it as a search query. The following formats are supported:

  * `Series Name` (Example: `Friends`)
  * `Series Name (year)` (Example: `The Mandalorian (2019)`)
  * `Series Name (year) {tvdb id}` (Example: `Game of Thrones (2011) {tvdb-121361}`)

-----

## 🚀 Docker Usage and Deployment

### 1\. Repository Structure

Ensure the following files are present at the root of your repository:

  * `main.py` (The Python script)
  * `requirements.txt` (Containing `yt-dlp`)
  * `Dockerfile` (The build recipe)

### 2\. Building the Docker Image

You can build the image directly from your GitHub URL. Replace `YOUR_USER` and `YOUR_REPO` with your information:

```bash
docker build -t theme-downloader https://github.com/YOUR_USER/YOUR_REPO.git
```

### 3\. Running the Script

Execution requires mounting a **Volume** (`-v`) so the container can access your series folders on the host server.

#### Basic Command (Using Default Values)

In this example, your series folder on the server is located at `/mnt/media/series`.

```bash
docker run --rm \
  -v /mnt/media/series:/app/series \
  theme-downloader
```

| Parameter | Explanation |
| :--- | :--- |
| `--rm` | Removes the container after execution (recommended for cleanup). |
| `-v /mnt/media/series:/app/series` | **Volume Mount:** Links the `/mnt/media/series` folder on the host to the `/app/series` path inside the container. |

#### Advanced Command (Customization via Environment Variables)

Use the `-e` flag to modify behavior without changing the code.

```bash
docker run --rm \
  -v /mnt/media/series/TV:/app/TVShows \
  -e SERIES_DIR="TVShows" \
  -e MAX_DURATION_SEC="60" \
  theme-downloader
```

### 📋 Environment Variables

| Variable | Description | Default Value | Example Value |
| :--- | :--- | :--- | :--- |
| `SERIES_DIR` | The name of the subfolder to scan **inside** the container. Must match the path mounted by `-v`. | `series` | `TVShows` |
| `MAX_DURATION_SEC` | The maximum accepted duration for an audio theme (in seconds). | `240` (4 minutes) | `60` (1 minute) |

### 🗓️ Automation (Cron)

To run the script daily (e.g., at 4:00 AM) and keep your folders updated, add a Cron job on your server:

```bash
# Open the crontab editor
crontab -e
```

Then add the following line (adjust the path and command if you are using `-e` variables):

```bash
0 4 * * * docker run --rm -v /mnt/media/series:/app/series theme-downloader
```

-----
