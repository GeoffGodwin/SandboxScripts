from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import requests
import time
import os

# Paths
driver_path = "C:/Users/Geoff/workspace/geoffgodwin/SandboxScripts/chromedriver-win64/chromedriver.exe"
download_folder = "C:/Users/Geoff/workspace/geoffgodwin/SandboxScripts/downloaded/"
brave_binary_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# Configure Brave
options = Options()
options.binary_location = brave_binary_path

# Initialize WebDriver with Brave
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Ensure download folder exists
os.makedirs(download_folder, exist_ok=True)

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

def download_album(album_url):
    driver.get(album_url)
    time.sleep(5)  # Allow time for the album page to load
    
    # Locate all track links in the table
    track_links = driver.find_elements(By.CSS_SELECTOR, "td.playlistDownloadSong a")
    
    for index in range(len(track_links)):
        try:
            # Refresh the track links to avoid stale references
            track_links = driver.find_elements(By.CSS_SELECTOR, "td.playlistDownloadSong a")
            link = track_links[index]
            
            print(f"Processing track {index + 1} of {len(track_links)}...")
            link.click()  # Open the track page
            time.sleep(5)  # Allow the track page to load
            
            # Locate the download link by finding the parent <a> of the <span> with class "songDownloadLink"
            download_link = driver.find_element(By.CSS_SELECTOR, "a[href] span.songDownloadLink").find_element(By.XPATH, "..")
            
            # Retrieve the href and filename
            mp3_url = download_link.get_attribute("href")
            filename = mp3_url.split("/")[-1]  # Extract filename from URL
            
            # Download the MP3 directly
            download_mp3(mp3_url, filename)
            
            time.sleep(5)  # Wait a bit before processing the next track
            driver.back()  # Return to the album page
        except Exception as e:
            print(f"Error processing track {index + 1}: {e}")
            driver.back()  # Ensure the script goes back even if an error occurs
            continue


# Replace with the URL of the album page you want to process
album_page_url = "https://downloads.khinsider.com/game-soundtracks/album/animal-crossing-new-horizons-2020-switch-gamerip"
download_album(album_page_url)

driver.quit()