![image](https://rule34.xxx/images/headerru.png)
# Fast Parallel Media Downloader for Rule34.xxx (2026 Edition)

Advanced Python script to bulk download media (images, videos, GIFs) from Rule34.xxx using the official API.  
Improved fork of [visiuun/PyR34-Downloader](https://github.com/visiuun/PyR34-Downloader) with modern features for 2026 API requirements.

## Features

- **Authenticated access** (user_id + api_key required)
- **Secure credential storage** in `r34_config.json`
- **Bulk download by tags** with 'all' limit support
- **Media type filtering** (all / images / videos / gifs)
- **Blacklist tags** — exclude unwanted tags (e.g., furry, scat)
- **AI-generated content filter** — option to exclude AI posts (adds -ai_generated -ai-assisted -stable_diffusion)
- **Parallel downloads** (6 concurrent by default, adjustable)
- **Descriptive filenames**: `character1_character2_(series)_tag1_tag2_tag3_id.extension`
- **Full post metadata** saved as JSON (tags, source, rating, score, artist, views, etc.)
- **Resume support** — skips existing files and metadata
- **Colored output & progress bars**

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


## Usage
Bashpython pyr34.py
Example: Download by tags with filters
text1 = Download by tags | 3 = Exit → 1
Tags principales (space-separated, ej: beat_banger sonic): beat_banger
Blacklist tags (space-separated, ej: furry scat OR leave empty): lowres bad_anatomy
Allow AI-generated content? (yes/no): no
Media type (all / images / videos / gifs): videos
Limit (number or 'all'): all
Output directory: Z:\Downloads\r34
Final search will include: beat_banger -lowres -bad_anatomy -ai_generated -ai-assisted -stable_diffusion

Create folder structure: Z:\Beatbanger\videos\beat_banger\videos\
Download only videos in parallel
Save metadata as videos/metadata/{post_id}_filename.json
Show progress and colored status messages

Directory Structure Example
output_folder/tag_identifier/
├── videos/
│   ├── character_(series)_tag_tag_id.mp4
│   └── ...
└── videos/metadata/
    ├── id_filename.mp4.json  ← full post data JSON
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
