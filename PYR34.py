import os
import json
import time
import requests
from tqdm import tqdm
from colorama import Fore, Style, init
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

CONFIG_FILE = "r34_config.json"
HEADERS = {
    "User-Agent": "Rule34Downloader/2.2 (compatible; Windows NT 10.0)"
}

session = requests.Session()
session.headers.update(HEADERS)

def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("user_id", ""), config.get("api_key", "")
    else:
        print(f"{Fore.MAGENTA}First-time setup: Saving credentials to {CONFIG_FILE}{Style.RESET_ALL}")
        user_id = input("Rule34.xxx user_id: ").strip()
        api_key = input("Rule34.xxx api_key: ").strip()
        with open(CONFIG_FILE, "w") as f:
            json.dump({"user_id": user_id, "api_key": api_key}, f, indent=4)
        print(f"{Fore.GREEN}Credentials saved.{Style.RESET_ALL}")
        return user_id, api_key

def get_media_type(file_url: str) -> str:
    ext = file_url.lower().rsplit('.', 1)[-1]
    if ext in ("mp4", "webm", "mkv", "avi"):
        return "videos"
    elif ext == "gif":
        return "gifs"
    elif ext in ("jpg", "jpeg", "png"):
        return "images"
    return "other"

def download_file(file_url: str, full_path: str) -> bool:
    try:
        with session.get(file_url, stream=True, timeout=15) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            with open(full_path, "wb") as file, tqdm(
                total=total_size, unit="B", unit_scale=True,
                desc=os.path.basename(full_path), leave=False
            ) as progress:
                for chunk in response.iter_content(chunk_size=32768):
                    file.write(chunk)
                    progress.update(len(chunk))
        return True
    except Exception as e:
        print(f"{Fore.RED}Download failed: {os.path.basename(full_path)} - {e}{Style.RESET_ALL}")
        return False

def save_metadata(post: dict, metadata_path: str):
    """Save full post info as JSON metadata."""
    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(post, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"{Fore.RED}Metadata save failed: {e}{Style.RESET_ALL}")
        return False

def clean_tag(tag: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', tag.strip()).strip('_')

def generate_filename(post: dict, post_id: str, extension: str) -> str:
    characters = post.get("tag_string_character", "").split()
    copyright_tag = post.get("tag_string_copyright", "") or post.get("tag_string_meta", "")
    copyright_tag = copyright_tag.split()[0] if copyright_tag else ""

    all_tags = post.get("tags", "").split()
    used = set(characters)
    if copyright_tag:
        used.add(copyright_tag)
    extra_tags = [t for t in all_tags if t not in used][:3]

    parts = []
    if characters:
        parts.append("_".join(clean_tag(c) for c in characters[:2]))
    if copyright_tag:
        parts.append(f"({clean_tag(copyright_tag)})")
    if extra_tags:
        parts.append("_".join(clean_tag(t) for t in extra_tags))

    base_name = "_".join(p for p in parts if p).replace("__", "_")
    if not base_name:
        base_name = f"post_{post_id}"
    else:
        base_name += f"_{post_id}"

    filename = re.sub(r'_+', '_', base_name).strip('_') + f".{extension}"
    if len(filename) > 200:
        filename = filename[:180] + f"_{post_id}.{extension}"
    return filename

def search_posts(tags: list[str], page: int, user_id: str, api_key: str, limit_per_page: int = 100):
    params = {
        "page": "dapi",
        "s": "post",
        "q": "index",
        "json": "1",
        "tags": " ".join(tags),
        "pid": str(page),
        "limit": str(limit_per_page),
        "api_key": api_key,
        "user_id": user_id
    }
    url = "https://api.rule34.xxx/index.php"
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "post" in data:
            posts = data["post"]
            if not isinstance(posts, list):
                posts = [posts] if posts else []
        elif isinstance(data, list):
            posts = data
        else:
            posts = []
        return posts
    except Exception as e:
        print(f"{Fore.RED}Search error (page {page}): {e}{Style.RESET_ALL}")
        return []

def download_by_tags(user_id: str, api_key: str, tags: list[str], media_type: str, limit_str: str, output_folder: str):
    tag_identifier = "_".join(tags).replace(" ", "_")
    base_dir = os.path.join(output_folder, tag_identifier)
    os.makedirs(base_dir, exist_ok=True)

    downloaded_count = 0
    page_number = 0
    start_time = time.time()
    max_items = 999999 if limit_str.lower() == "all" else int(limit_str)

    max_workers = 6

    while downloaded_count < max_items:
        posts = search_posts(tags, page_number, user_id, api_key)
        if not posts:
            print(f"{Fore.YELLOW}No more results (page {page_number} empty).{Style.RESET_ALL}")
            break

        print(f"{Fore.CYAN}Page {page_number}: {len(posts)} posts found. Starting parallel downloads...{Style.RESET_ALL}")

        def download_task(post):
            file_url = post.get("file_url") or post.get("sample_url") or post.get("preview_url") or ""
            if not file_url:
                return None, None, "no_url"

            current_type = get_media_type(file_url)
            if media_type != "all" and current_type != media_type:
                return None, None, "filtered"

            target_dir = os.path.join(base_dir, current_type)
            os.makedirs(target_dir, exist_ok=True)

            metadata_dir = os.path.join(target_dir, "metadata")
            os.makedirs(metadata_dir, exist_ok=True)

            ext = file_url.rsplit('.', 1)[-1].lower()
            filename = generate_filename(post, str(post.get("id", "unknown")), ext)
            full_path = os.path.join(target_dir, filename)

            post_id = str(post.get("id", "unknown"))
            metadata_filename = f"{post_id}_{filename}.json" if "." in filename else f"{post_id}_{filename}.json"
            metadata_path = os.path.join(metadata_dir, metadata_filename)

            if os.path.exists(full_path):
                if not os.path.exists(metadata_path):
                    save_metadata(post, metadata_path)
                return filename, full_path, "exists"

            success = download_file(file_url, full_path)
            if success:
                save_metadata(post, metadata_path)
            return filename, full_path, "success" if success else "failed"

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(download_task, post) for post in posts]

            for future in tqdm(as_completed(futures), total=len(posts), desc=f"Page {page_number} (parallel)", unit="file"):
                filename, _, status = future.result()
                if status == "success":
                    downloaded_count += 1
                    print(f"{Fore.GREEN}✓ Downloaded: {filename} + metadata{Style.RESET_ALL}")
                elif status == "exists":
                    print(f"{Fore.YELLOW}Already exists: {filename} (metadata checked){Style.RESET_ALL}")
                elif status == "failed":
                    print(f"{Fore.RED}✗ Failed: {filename}{Style.RESET_ALL}")

                if downloaded_count >= max_items:
                    break

        page_number += 1
        time.sleep(0.8)

    elapsed = time.time() - start_time
    print(f"\n{Fore.GREEN}Completed: {downloaded_count} {media_type} files + metadata in {elapsed:.2f} seconds.{Style.RESET_ALL}")

def main():
    user_id, api_key = load_or_create_config()
    if not user_id or not api_key:
        print(f"{Fore.RED}Invalid credentials. Delete {CONFIG_FILE} and restart.{Style.RESET_ALL}")
        return

    while True:
        choice = input("\n1 = Download by tags | 2 = Exit → ").strip()
        if choice == "2":
            print(f"{Fore.MAGENTA}Exiting. Goodbye!{Style.RESET_ALL}")
            break
        if choice == "1":
            tags_input = input("Tags (space-separated): ").strip()
            tags_list = [t for t in tags_input.split() if t]
            if not tags_list:
                continue
            media_choice = input("Media type (all / images / videos / gifs): ").lower().strip()
            limit_input = input("Limit (number or 'all'): ").strip()
            output_path = input("Output directory: ").strip()
            download_by_tags(user_id, api_key, tags_list, media_choice, limit_input, output_path)
        else:
            print("Please enter 1 or 2.")

if __name__ == "__main__":
    main()