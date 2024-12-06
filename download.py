import os
import requests
import zipfile
import tempfile
"""
wersje chrome i chromedrivera sa na razie hardcoded bo endpoint od chromedrivera z jakiegos powodu nie chcial wspolpracowac
"""
def create_project_folder(folder_name="downloads"):
    """
    Creates a folder in the project root directory.

    :param folder_name: Name of the folder to create.
    :return: Absolute path to the created folder.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(project_root, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def download_and_extract(download_url, extract_to):
    """
    Downloads and extracts a ZIP file from a specified URL.

    :param download_url: URL to the ZIP file.
    :param extract_to: Directory where the content should be extracted.
    """
    try:
        # Temporary file to store the downloaded ZIP
        zip_file_path = os.path.join(extract_to, os.path.basename(download_url))

        # Download the ZIP file
        print(f"Downloading from {download_url}...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with open(zip_file_path, 'wb') as zip_file:
            for chunk in response.iter_content(chunk_size=8192):
                zip_file.write(chunk)

        print("Download completed.")

        # Extract the ZIP file
        print(f"Extracting to {extract_to}...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # Clean up the downloaded ZIP file
        os.remove(zip_file_path)
        print("Extraction completed.")
    except Exception as e:
        print(f"Error: {e}")


def download_metamask(download_url, save_to=None):
    """
    Downloads the MetaMask extension ZIP file to the specified directory without extracting it.

    :param download_url: URL to the MetaMask ZIP file.
    :param save_to: Directory where the ZIP file should be saved.
    :return: Path to the saved MetaMask ZIP file.
    """
    try:
        # Create a temporary directory if no save directory is provided
        if not save_to:
            save_to = os.path.join(tempfile.gettempdir(), "metamask_downloads")

        # Ensure the save directory exists
        os.makedirs(save_to, exist_ok=True)

        # Determine the filename from the URL
        file_name = os.path.basename(download_url)
        zip_path = os.path.join(save_to, file_name)

        # Download the ZIP file
        print(f"Downloading MetaMask from {download_url} to {zip_path}...")
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(zip_path, 'wb') as zip_file:
                zip_file.write(response.content)
            print(f"Download completed: {zip_path}")
        else:
            raise Exception(f"Failed to download MetaMask. HTTP Status Code: {response.status_code}")

        return zip_path

    except Exception as e:
        print(f"Error: {e}")
        return None


def download_chromedriver(version=None, platform="win32"):
    """
    Downloads and extracts the ChromeDriver for the specified version.

    :param version: ChromeDriver version to download.
    :param platform: Platform identifier (e.g., win32, mac64, linux64).
    """
    base_url = "https://storage.googleapis.com/chrome-for-testing-public"
    download_url = f"https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/win64/chromedriver-win64.zip"
    downloads_folder = create_project_folder()
    chromedriver_folder = os.path.join(downloads_folder, "chromedriverp")
    os.makedirs(chromedriver_folder, exist_ok=True)
    download_and_extract(download_url, chromedriver_folder)
    print(f"ChromeDriver is available at: {chromedriver_folder}")


def download_chrome_for_testing(version=None, platform="win64"):
    """
    Downloads and extracts a specific version of Chrome for Testing.

    :param version: Chrome version to download (e.g., '114.0.5735.90').
    :param platform: Platform identifier (e.g., 'win64', 'mac-arm64', 'linux64').
    """
    base_url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing"
    download_url = f"https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/win64/chrome-win64.zip"
    downloads_folder = create_project_folder()
    chrome_folder = os.path.join(downloads_folder, "chromep")
    os.makedirs(chrome_folder, exist_ok=True)
    download_and_extract(download_url, chrome_folder)
    print(f"Chrome for Testing is available at: {chrome_folder}")
"""
metamask_zip_path = download_metamask(
    'https://github.com/MetaMask/metamask-extension/releases/download/v10.22.0/metamask-chrome-10.22.0.zip',
    save_to='downloads/metamask'
)
"""
download_chromedriver()

#download_chrome_for_testing()
