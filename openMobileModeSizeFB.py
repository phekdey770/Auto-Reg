from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from screeninfo import get_monitors
import time

# Corrected path to the ChromeDriver executable
CHROMEDRIVER_PATH = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'  # Update this path

# Number of Chrome instances to open
target_open = 7

# Desired maximum window width and height
max_window_width = 516
window_height = 708  # Fixed window height

# Time to wait (in seconds) between opening each window
delay_between_windows = 2

# Get the screen dimensions
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Calculate the number of windows that can fit in the screen width
if max_window_width * target_open > screen_width:
    window_width = screen_width // target_open
    if window_width > max_window_width:
        window_width = max_window_width
else:
    window_width = max_window_width

# Adjust window height if necessary
window_height = min(window_height, screen_height)

# Horizontal space between windows
spacing = 1

# Set up Chrome options to emulate a generic mobile browser
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36")
chrome_options.add_argument("--window-size=360,640")  # Typical mobile screen size
# Remove the '--headless' option to ensure the browser is visible

# Open multiple instances of Chrome and arrange them from left to right
drivers = []
for i in range(target_open):
    # Create a new instance of the Chrome driver
    service = Service(CHROMEDRIVER_PATH)
    driver: WebDriver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set the window size
    driver.set_window_size(window_width, window_height)
    
    # Calculate the position for each window
    x_position = i * (window_width + spacing)
    y_position = 0  # You can adjust this if you want to arrange vertically as well
    
    # Set the window position
    driver.set_window_position(x_position, y_position)
    
    # Open the Facebook registration page
    driver.get("https://m.facebook.com/reg")
    
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
