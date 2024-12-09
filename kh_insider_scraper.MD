# **KH Insider Scraper**

A Python script that automates the download of music tracks from KH Insider album pages. This tool uses Selenium for browser automation and `requests` for direct MP3 file downloads.  

⚠️ **Disclaimer**: Please ensure you have permission to download files from KH Insider and that your use complies with their terms of service.

---

## **Features**
- Automatically downloads MP3 tracks from a specified KH Insider album page.
- Handles URL-encoded filenames by decoding them to human-readable names.
- Uses a `.env` file for configuration to keep sensitive paths private.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.7+
- Google Chrome or Brave Browser installed.
- Matching `ChromeDriver` version for your browser:
  - Check your browser version:
    - Brave: Visit `brave://settings/help`
    - Chrome: Visit `chrome://settings/help`
  - Download the corresponding `ChromeDriver` version [here](https://chromedriver.chromium.org/downloads).

### **2. Clone the Repository**
```bash
git clone https://github.com/geoffgodwin/kh-insider-scraper.git  
cd kh-insider-scraper
```

### **3. Install Required Packages**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the project root (not included in version control) and specify the following paths:

```bash
DRIVER_PATH=path/to/chromedriver  
DOWNLOAD_FOLDER=path/to/your/download/folder  
BRAVE_BINARY_PATH=path/to/brave/browser
```

#### **Example**
```bash
DRIVER_PATH=C:/Users/YOUR_USERNAME/chromedriver-win64/chromedriver.exe  
DOWNLOAD_FOLDER=C:/Users/YOUR_USERNAME/downloads/  
BRAVE_BINARY_PATH=C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe  
```

> ⚠️ **Note**: If you want to use Chrome instead of Brave, simply remove or comment out the `BRAVE_BINARY_PATH` entry and use the default Chrome installation.

---

## **How to Run**

1. **Edit the Script**:
   - Replace the `album_page_url` variable in the script with the URL of the album you want to download:
     album_page_url = "https://downloads.khinsider.com/album-page-url"

2. **Run the Script**:
```bash
   python kh_insider_scraper.py
```

3. **Tracks Downloaded**:
   - MP3 files will be downloaded to the folder specified in your `.env` file.

---

## **Switching to Chrome**
To use Chrome instead of Brave:
1. Update your `.env` file:
```bash
   DRIVER_PATH=path/to/chromedriver  
   DOWNLOAD_FOLDER=path/to/your/download/folder  
```

2. Comment out or remove the `BRAVE_BINARY_PATH` variable.

3. The script will default to Chrome for browser automation.

---

## **Troubleshooting**

### **Common Issues**

1. **`ChromeDriver` Version Mismatch**:
   - Ensure your `ChromeDriver` version matches your browser version.  
   - Re-download the correct `ChromeDriver` [here](https://chromedriver.chromium.org/downloads).

2. **Stale Element Reference**:
   - If the script stops due to a "stale element" error, try rerunning it. The script dynamically re-fetches elements, but occasional failures might occur. If you are on a slower internet connection you can play with the sleep delays that wait for page load.

3. **Cookie Banner Blocking Clicks**:
   - If a cookie banner interferes, the script automatically dismisses it. If the issue persists, check the site manually.

---

## **Contributing**
Feel free to fork this repository and submit pull requests for improvements or fixes. Suggestions and feedback are welcome!

---

## **License**
This project is licensed under the MIT License.
