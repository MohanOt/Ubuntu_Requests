import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def fetch_image(url, saved_hashes):
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Content-Type check
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"✗ Skipped: URL does not point to an image ({url})")
            return

        filename = get_filename_from_url(url)

        content = response.content
        file_hash = get_file_hash(content)

        if file_hash in saved_hashes:
            print(f"✗ Duplicate image detected, skipping: {filename}")
            return
        saved_hashes.add(file_hash)

        filepath = os.path.join("Fetched_Images", filename)
        counter = 1
        # Avoid filename collisions
        while os.path.exists(filepath):
            filename_parts = os.path.splitext(filename)
            filepath = os.path.join("Fetched_Images", f"{filename_parts[0]}_{counter}{filename_parts[1]}")
            counter += 1

        with open(filepath, 'wb') as f:
            f.write(content)

        print(f"✓ Successfully fetched: {os.path.basename(filepath)}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error while fetching {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred while processing {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Please enter image URLs (separated by commas): ").split(',')

    # Create directory
    os.makedirs("Fetched_Images", exist_ok=True)

    # Track hashes of downloaded images to prevent duplicates
    saved_hashes = set()

    for url in map(str.strip, urls):
        if url:
            fetch_image(url, saved_hashes)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
