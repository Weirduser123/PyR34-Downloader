![image](https://rule34.xxx/images/headerru.png)
# Fast Parallel Media Downloader for Rule34.xxx (2026 Edition)

Advanced Python script to bulk download media (images, videos, GIFs) from Rule34.xxx using the official API.  
This is a heavily improved and modernized fork of the original [visiuun/PyR34-Downloader](https://github.com/visiuun/PyR34-Downloader), with support for current API requirements (authentication), parallel downloads, descriptive filenames, full metadata saving, and more.

## Features

- **Authenticated API access** (required since mid-2025)
- **Credentials stored securely** in `r34_config.json` (created automatically on first run)
- **Bulk download by tags** with optional limit (`all` = everything available)
- **Media type filter** — download only `images`, `videos`, `gifs`, or `all`
- **Parallel downloads** using threads (up to 6 concurrent by default — much faster!)
- **Descriptive filenames**: `character1_character2_(series)_tag1_tag2_tag3_id.extension`
- **Full metadata saved** as JSON next to each file (all tags, source, rating, score, artist, copyright, meta tags, views, etc.)
- **Colored terminal output** and progress bars with `tqdm`
- **Rate-limit friendly** with configurable delay between pages
- **Resume support** — skips already downloaded files (including metadata)

## Requirements

- Python 3.8+
- Internet connection

Required libraries (installed automatically on first run if missing):

- `requests`
- `tqdm`
- `colorama`
- `concurrent.futures` (built-in)

## Installation

1. **Download or clone** the script:
   ```bash
   git clone https://github.com/Weirduser123/PYR34-Fast-Downloader.git
   cd PYR34-Fast-Downloader
(or just save it like pyr34.py)

Run once to create config and install dependencies:Bashpython pyr34.pyThe script will:
Ask for your user_id and api_key from https://rule34.xxx (Account → Options)
Save them in r34_config.json
Install missing libraries if needed


Usage
Bashpython pyr34.py
Menu Options
text1 = Download by tags
3 = Exit
Download by Tags Example:
textTags (space-separated): beat_banger
Media type (all / images / videos / gifs): videos
Limit (number or 'all'): all
Output directory: Z:\Beatbanger\videos
The script will:

Create folder structure: Z:\Beatbanger\videos\beat_banger\videos\
Download only videos in parallel
Save metadata as videos/metadata/{post_id}_filename.json
Show progress and colored status messages

Directory Structure Example
textZ:\Beatbanger\videos\beat_banger\
├── videos\
│   ├── sonic_the_hedgehog_(sonic_the_hedgehog)_beat_banger_animated_123456.mp4
│   ├── sonic_the_hedgehog_(sonic_the_hedgehog)_beat_banger_loop_789012.mp4
│   └── ...
└── videos\metadata\
    ├── 123456_sonic_the_hedgehog_(sonic_the_hedgehog)_beat_banger_animated_123456.json
    └── ...
Each .json contains the full post data from the API, including:

tags, tag_string_artist, tag_string_character, tag_string_copyright, tag_string_general, tag_string_meta
source (external link if present)
rating (explicit / questionable / safe)
score, up_score, down_score
views, fav_count
uploader, created_at, file_url, width, height, etc.

Configuration & Tuning

Max concurrent downloads: Edit max_workers = 6 in the script
→ Lower to 4 if you get HTTP 429 errors (rate limit)
→ Increase to 8–12 if you have fast fiber and a good API key
Delay between pages: time.sleep(0.8) — increase to 1.5–2.0 if banned
Chunk size: Already optimized at 32768 bytes

Troubleshooting

HTTP 401 / Invalid credentials → Check your user_id and api_key at https://rule34.xxx/index.php?page=account&s=options
HTTP 429 Too Many Requests → Lower max_workers or increase sleep time
No posts found → Try simpler tags or remove rating:explicit if testing
Metadata not saving → Check write permissions in output folder

Important Notes

Respect Rule34.xxx rate limits and ToS. Heavy usage may result in temporary IP bans.
This tool is for personal, educational use only.
The API may change; check https://rule34.xxx for updates.

Credits

Original concept & base: visiuun/PyR34-Downloader
2026 updates, parallel downloads, metadata, descriptive names: Enhanced version

Enjoy responsibly~ ♡
