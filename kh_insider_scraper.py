import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import unquote
from dotenv import load_dotenv
import os
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Get paths from environment variables
driver_path = os.getenv("DRIVER_PATH")
download_folder = os.getenv("DOWNLOAD_FOLDER")
brave_binary_path = os.getenv("BRAVE_BINARY_PATH")

# Ensure download folder exists
os.makedirs(download_folder, exist_ok=True)

# Configure Brave
options = Options()
options.binary_location = brave_binary_path

# Initialize WebDriver with Brave
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def download_mp3(url, filename):
    """Download an MP3 file from the given URL and decode the filename."""
    try:
        # Decode URL-encoded filename
        decoded_filename = unquote(filename)
        print(f"Downloading: {decoded_filename}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        with open(os.path.join(download_folder, decoded_filename), "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {decoded_filename}")
    except Exception as e:
        print(f"Failed to download {decoded_filename}: {e}")

def dismiss_overlays():
    """Dismiss cookie banners or other overlays."""
    try:
        cookie_banner = driver.find_element(By.CSS_SELECTOR, "div.cookieinfo")
        if cookie_banner.is_displayed():
            driver.execute_script("arguments[0].style.visibility = 'hidden';", cookie_banner)
            print("Cookie banner dismissed.")
    except Exception:
        # No overlay to dismiss
        pass

def safe_click(element, retries=3):
    """Click an element with retry logic."""
    for attempt in range(retries):
        try:
            element.click()
            return
        except Exception as e:
            print(f"Click failed: {e}. Retrying... ({attempt + 1}/{retries})")
            time.sleep(1)
    raise Exception("Failed to click the element after multiple attempts.")

def download_album(album_url, delay):
    driver.get(album_url)
    time.sleep(delay)  # Allow time for the album page to load
    
    # Locate all track links in the table
    track_links = driver.find_elements(By.CSS_SELECTOR, "td.playlistDownloadSong a")
    
    for index in range(len(track_links)):
        try:
            # Refresh the track links to avoid stale references
            track_links = driver.find_elements(By.CSS_SELECTOR, "td.playlistDownloadSong a")
            link = track_links[index]
            
            print(f"Processing track {index + 1} of {len(track_links)}...")
            
            # Dismiss overlays
            dismiss_overlays()
            
            # Click the link safely
            safe_click(link)
            time.sleep(delay)  # Allow the track page to load
            
            # Locate the download link by finding the parent <a> of the <span> with class "songDownloadLink"
            download_link = driver.find_element(By.CSS_SELECTOR, "a[href] span.songDownloadLink").find_element(By.XPATH, "..")
            
            # Retrieve the href and filename
            mp3_url = download_link.get_attribute("href")
            filename = mp3_url.split("/")[-1]  # Extract filename from URL
            
            # Download the MP3 directly
            download_mp3(mp3_url, filename)
            
            time.sleep(delay)  # Wait before processing the next track
            driver.back()  # Return to the album page
        except Exception as e:
            print(f"Error processing track {index + 1}: {e}")
            driver.back()  # Ensure the script goes back even if an error occurs
            continue

# Main entry point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python kh_insider_scraper.py <album_url> [delay_in_seconds]")
        sys.exit(1)
    
    album_url = sys.argv[1]
    delay = float(sys.argv[2]) if len(sys.argv) > 4 else 4.0  # Default delay is 4 seconds

    try:
        download_album(album_url, delay)
    finally:
        driver.quit()
