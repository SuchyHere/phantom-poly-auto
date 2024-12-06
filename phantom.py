import secrets
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
from pywinauto import Desktop
import pyautogui
import time
"""
Dziala tylko na windowsie, musisz najpierw zrunowac download.py to pobierze chrome for testing i chrome drivera zgodne wersjami

Co do phantoma to trzeba wejsc tutaj: https://extensiondock.com/en i wkleic 
https://chromewebstore.google.com/detail/phantom/bfnaelmomeimhlpmgjnjophhpkkoljpa,
pobierze sie bfnaelmomeimhlpmgjnjophhpkkoljpa.crx, Musisz zmienic rozszerzenie na zip i wypakowac, 
potem zamien nizej path do folderu w ktorym go wypakowales (PHANTOM_PATH), 
niestety path z roota nie dziala z jakiegos powodu (przynajmniej mi)

Musisz miec USDC (musi byc na polygonie inaczej program nie znajdzie i sie wysypie) na phantomie, 
polymarket chyba tylko w tym przyjmuje depozyty

private_key na razie trzeba wprowadzic do kodu

jak chcesz to mozna zmienic amount, teraz jest 0.1 bo testowalem kilka razy, a obok random ilosc od 1-5
zamien sobie jesli chcesz 

haslo robi sie losowe i tak sesja jest zawsze nowa wiec nie ma co zapisywac

username (random_name w first_time_poly()) na polymarkecie tez sie robi losowo
mozna go ustawic jakas petla jak chcesz np: Konto1, Konto2 itd. 

Czasem program sie wysypywal jak funkcja open_phantom probowala uaktywnic okno zeby uzyc skrotu klawiszowego
zazwyczaj wystarczy puscic program jeszcze raz

Jesli by sie wysypywal czesto, mozliwe ze cos u ciebie sie wolniej laduje, mozna zwiekszyc lub dodac time.sleep()
w momentach gdzie sie tak dzieje
"""
amount = "0.1" # random amount str(random.randint(1, 5))
private_key = ""
password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
CHROME_DRIVER_PATH = r"downloads/chromedriverp/chromedriver-win64/chromedriver.exe"
CHROME_PATH = r"downloads/chromep/chrome-win64/chrome.exe"
PHANTOM_PATH = r""
EXTENSION_ID = "bfnaelmomeimhlpmgjnjophhpkkoljpa"


def setup_webdriver():
    """Set up the WebDriver with MetaMask extension."""
    global main_window
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--load-extension={PHANTOM_PATH}")
    options.add_argument("--lang=en")  # Force English language
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    main_window = driver.current_window_handle

    return driver


def setup_phantom(driver):
    """Set up the MetaMask wallet."""
    print("Setting up MetaMask wallet...")

    time.sleep(5)
    for handle in driver.window_handles:
        print(handle)
        driver.switch_to.window(handle)
        if "Phantom" in driver.title:
            print("Switched to Phantom tab")
            break
    else:
        raise Exception("Phantom tab not found")

        # Click "I already have a wallet"
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="I already have a wallet"]'))
    ).click()
    # Click "Import secret recovery phrase"
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//div[text()="Import Private Key"]'))
    ).click()

    dropdown = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-fotOHu"))
    )

    # Click the dropdown to open it
    dropdown.click()

    # Wait for the "Solana" option to be visible
    solana_option = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//p[text()="Polygon"]'))
    )
    solana_option.click()

    name_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Name"]'))
    )
    name_input.send_keys("account 1")

    # Interact with the "Private key" textarea
    private_key_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Private key"]'))
    )
    private_key_input.send_keys(private_key)  # Input random text

    # Click "Import secret recovery phrase"
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Import"]'))
    ).click()
    password_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.click()  # Click to focus
    password_input.send_keys(password)  # Enter password

    # Interact with the "Confirm Password" input field
    confirm_password_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "confirmPassword"))
    )
    confirm_password_input.click()  # Click to focus
    confirm_password_input.send_keys(password)  # Enter the same password

    checkbox = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="onboarding-form-terms-of-service-checkbox"]'))
    )
    checkbox.click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))
    ).click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Get Started"]'))
    ).click()
    return

def navigate_to_polymarket(driver):
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    driver.get("https://polymarket.com")
    print("polymarket opened")
    driver.set_window_size(1200, 800)


def login_to_polymarket(driver):

    login_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Log In"]'))
    )
    driver.execute_script("arguments[0].click();", login_button)
    print("Successfully clicked the 'Log In' button using JavaScript!")

    phantom_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//span[contains(text(),"Phantom")]]'))
    )
    phantom_button.click()


def select_popup(driver):

    WebDriverWait(driver, 10).until(lambda d: len(driver.window_handles) > 1)

    # Get the new window handle
    new_window = [handle for handle in driver.window_handles if handle != main_window][0]

    driver.switch_to.window(new_window)
    print("Switched to the popup window")


def connect_wallet(driver):
    select_popup(driver)

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Connect"]'))
    ).click()

    driver.switch_to.window(main_window)
    print("connected and Switched back to the main window")

def confirm_signature(driver):
    time.sleep(1)
    select_popup(driver)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm"]'))
    ).click()

    driver.switch_to.window(main_window)
    print("confirmed and Switched back to the main window")
def first_time_poly(driver):
    try:
        # Check if the input field is present
        name_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        print("Name input found!")
    except Exception:
        print("Name input not found. Redirecting in a second.")
        return False

    while True:
        try:
            random_name = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            name_input.clear()
            name_input.send_keys(random_name)
            print(f"Generated and entered name: {random_name}")

            # Click the checkbox
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "termsOptIn"))
            )
            checkbox.click()
            print("Checkbox clicked!")

            # Attempt to click the Continue button
            continue_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Continue"]'))
            )

            # Check if the Continue button is enabled
            if continue_button.is_enabled():
                continue_button.click()
                print("Continue button clicked!")
                break
            else:
                print("Continue button is still disabled. Retrying with a new name...")

        except Exception as e:
            print(f"Error during the process: {e}")
            print("Retrying...")

    # Click Skip for now
    try:
        skip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Skip for now"]'))
        )
        skip_button.click()
        print("Skip for now button clicked!")
    except Exception:
        print("Skip for now button not found. Exiting gracefully.")

    # Click Start Trading
    try:
        start_trading_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Start trading"]'))
        )
        start_trading_button.click()
        print("Start trading button clicked!")
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))
        ).click()
        confirm_signature(driver)
    except Exception:
        print("Start trading button not found. Exiting gracefully.")

    return True





def open_phantom():
    # Initialize the desktop object
    desktop = Desktop(backend="uia")

    # Debug: Print all available window titles
    print("Available windows:")
    for win in desktop.windows():
        print(f"- {win.window_text()}")

    try:
        # Find the window containing "Google Chrome for Testing"
        window = desktop.window(title_re=".*Google Chrome for Testing.*")
        print(f"Found window: {window.window_text()}")

        # Bring the window to the foreground
        window.set_focus()
        print("Window activated.")

        # Simulate Phantom shortcut
        pyautogui.hotkey('alt', 'shift', 'p')
        print("Phantom shortcut triggered.")

    except Exception as e:
        print(f"Failed to activate the window using pywinauto: {e}")


def deposit_funds(driver, amount):
    driver.get("https://polymarket.com/wallet")
    copy_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[text()="Copy"]'))
    )
    copy_button.click()
    print("Copy button clicked!")

    # Retrieve the copied value from the clipboard
    copied_value = pyperclip.paste()
    print(f"Copied value: {copied_value}")

    send_funds(driver, copied_value)


def send_funds(driver, address, coin="USDC"):
    open_phantom()
    time.sleep(1)
    select_popup(driver)
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//div[text()="Send"]]'))
    )
    send_button.click()

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search..."]'))
    )
    search_input.click()  # Focus the input field
    search_input.send_keys("USDC")  # Enter search text

    try:
        time.sleep(2)
        # Locate all elements with the same `data-testid`
        usdc_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="fungible-token-row-polygon-USDC"]')

        # Filter for visible elements
        visible_usdc_elements = [el for el in usdc_elements if el.is_displayed()]

        # If there are no visible elements, raise an error
        if not visible_usdc_elements:
            print("No visible Polygon-USDC elements found.")
            raise Exception("No visible Polygon-USDC elements found.")

        # Click the visible element
        visible_usdc_elements[1].click()
        print("Clicked on the visible Polygon-USDC element.")

    except Exception as e:
        print(f"Error: {e}")
        return
    # Enter the recipient's address
    recipient_textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "recipient"))
    )
    recipient_textarea.click()  # Focus the textarea
    recipient_textarea.send_keys(address)  # Example address

    # Enter the amount
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "amount"))
    )
    amount_input.click()  # Focus the input
    amount_input.send_keys('0.1')  # Example amount str(random.randint(1, 5))

    # Wait for the "Next" button to become enabled
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="primary-button"]'))
    )
    # Click the "Next" button
    next_button.click()

    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="primary-button" and text()="Send"]'))
    )
    # Click the "Send" button
    send_button.click()

    pyautogui.hotkey('alt', 'shift', 'p')
    time.sleep(2)
    driver.switch_to.window(main_window)
    print("switched to main window")
    time.sleep(2)
    # Click the "Got it" button
    got_it_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Got it"]'))
    )
    got_it_button.click()


driver=setup_webdriver()
setup_phantom(driver)
navigate_to_polymarket(driver)
login_to_polymarket(driver)
connect_wallet(driver)
confirm_signature(driver)
if first_time_poly(driver):
    time.sleep(15)
    navigate_to_polymarket(driver)
deposit_funds(driver, amount)

time.sleep(20)
driver.quit()



