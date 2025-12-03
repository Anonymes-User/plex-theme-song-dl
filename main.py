import os
import re
import yt_dlp
from pathlib import Path

# --- CONFIGURATION READ FROM ENVIRONMENT VARIABLES ---

# 1. Base Directory: Reads SERIES_DIR environment variable. Defaults to "series".
BASE_DIR = Path(os.getenv("SERIES_DIR", "series")) 

# 2. Max Duration: Reads MAX_DURATION_SEC. Defaults to 240 seconds (4 minutes).
try:
    MAX_DURATION = int(os.getenv("MAX_DURATION_SEC", "240"))
except ValueError:
    MAX_DURATION = 240
    print(f"Warning: MAX_DURATION_SEC is not a valid number. Using default value ({MAX_DURATION}s).")

def get_clean_show_name(folder_name):
    """
    Cleans the folder name to extract the series title.
    Handles formats: "Name (Year) {id}", "Name (Year)", and "Name".
    """
    # Regex pattern: Captures everything before " (YYYY)" and ignores the rest ({id} or nothing).
    # ^(.*?)\s -> Captures the title lazily until a space
    # \(\d{4}\) -> Followed by a 4-digit year in parentheses
    pattern = r"^(.*?)\s\(\d{4}\).*"
    
    match = re.match(pattern, folder_name)
    if match:
        return match.group(1) 
    return folder_name # Returns the original name if no year is found

def download_theme(show_name, output_path):
    """
    Searches and downloads the audio theme from YouTube with a dynamic duration filter.
    """
    # Optimized search query to target intro themes
    search_query = f"{show_name} tv show opening theme audio"
    print(f"   ⬇️ Searching: '{show_name}' (max {MAX_DURATION}s)...")

    ydl_opts = {
        'format': 'bestaudio/best',
        # yt-dlp automatically adds the .mp3 extension during post-processing
        'outtmpl': str(output_path).replace('.mp3', ''),
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
        # Duration filter using the dynamic MAX_DURATION variable
        'match_filter': yt_dlp.utils.match_filter_func(f"duration < {MAX_DURATION}"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        
        # Final check to ensure a file was actually created (in case filters rejected all results)
        if output_path.exists():
            print(f"   ✅ Success: theme.mp3 created.")
        else:
            print(f"   ⚠️ No valid result found (too long or unavailable).")
            
    except Exception as e:
        print(f"   ❌ Error during download: {e}")

def main():
    print(f"--- Starting Theme Downloader ---")
    print(f"Configuration: Base Directory: {BASE_DIR.resolve()}, Max Duration: {MAX_DURATION}s")

    if not BASE_DIR.exists():
        print(f"Error: Base directory '{BASE_DIR}' does not exist.")
        print("Please check the volume mount (-v) and/or the SERIES_DIR environment variable (-e).")
        return

    print(f"🔍 Scanning directory: {BASE_DIR.resolve()}\n")

    # Iterate over all immediate subdirectories of the base path
    for show_folder in BASE_DIR.iterdir():
        if show_folder.is_dir():
            theme_file = show_folder / "theme.mp3"
            
            print(f"📁 Folder: {show_folder.name}")

            if theme_file.exists():
                print("   ⏭️ theme.mp3 already exists. Skipping.")
            else:
                # 1. Clean the folder name
                clean_name = get_clean_show_name(show_folder.name)
                
                # Fallback to the full folder name if cleaning fails
                if not clean_name.strip():
                    clean_name = show_folder.name

                # Show the clean name if it differs from the folder name
                if clean_name != show_folder.name:
                    print(f"   ✨ Cleaned name identified: '{clean_name}'")
                
                # 2. Initiate download
                download_theme(clean_name, theme_file)
            
            print("-" * 40)

if __name__ == "__main__":
    main()
