from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
import time

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'

# Number of Chrome instances to open
target_open = 7

# Desired window size and initial position
window_width = 310
window_height = 550

# Time to wait (in seconds) between opening each window
delay_between_windows = 5

# Set up Chrome options
chrome_options = Options()

# Set user agent to a mobile device
mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={mobile_user_agent}")

# Open multiple instances of Chrome and arrange them from left to right
drivers = []
for i in range(target_open):
    # Add window size and position arguments
    chrome_options.add_argument(f"--window-size={window_width},{window_height}")
    chrome_options.add_argument(f"--window-position={i * window_width},0")
    
    # Optionally, open the URL in "app" mode (without address bar)
    chrome_options.add_argument("--app=https://m.facebook.com/reg")
    
    # Create a new instance of the Chrome driver
    service = Service(CHROMEDRIVER_PATH)
    driver: WebDriver = webdriver.Chrome(service=service, options=chrome_options)
 
    # Add the driver to the list
    drivers.append(driver)
    
    # Wait before opening the next window
    if i < target_open - 1:  # No need to wait after the last window
        time.sleep(delay_between_windows)

# Optional: wait for the user to interact with the browsers
input("Press Enter to close all browsers...")

# Close all browsers
for driver in drivers:
    driver.quit()
