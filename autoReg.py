import json
import logging
import random
import re
import string
import time
import bs4
import requests
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import colorama

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# Emulate a mobile device with screen size 319x659
mobile_emulation = {
    "deviceMetrics": {"width": 319, "height": 659, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1"
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# Set the window size to match the mobile emulation
chrome_options.add_argument("--window-size=319,659")
chrome_options.add_argument("--window-position=0,0")  # Optional: to set window position at the top-left of the screen
# Service object pointing to your ChromeDriver
service_obj = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
driver = webdriver.Chrome(service=service_obj, options=chrome_options)

# List of XPaths to click on
xpaths = [
    "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div[1]/div[1]",
    "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div[1]"
]

# Configure logging to save to a file
log_file = r"C:\Code Workpace\VS Code\Reg FB Acc\Data\Logs\account_creation.log"
format = "[" + colorama.Fore.LIGHTBLUE_EX + "%(asctime)s" + colorama.Fore.RESET + "] " + colorama.Fore.LIGHTGREEN_EX + "%(message)s" + colorama.Fore.RESET
logging.basicConfig(filename=log_file, format=format, level=logging.INFO, datefmt="%H:%M:%S")

def random_click_elements(xpath_list):
    selected_xpaths = random.sample(xpath_list, 2)
    for xpath in selected_xpaths:
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(2)
        gender = determine_gender_from_xpaths(selected_xpaths)
        logging.info(f"-----------------Gender: {gender}-----------------")
        
def writen_to_file(first_name, last_name, age, phone_number, email, password):
    filename = f"{first_name}_{last_name}.txt"
    filepath = rf"C:\Code Workpace\VS Code\Reg FB Acc\Account\{filename}"
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a") as f:
        f.write(f"=== Account - {first_name} {last_name} ===\nFirst Name: {first_name}\nLast Name: {last_name}\nAge: {age} (till to {current_datetime})\nPhone: {phone_number}\nEmail: {email}\nPassword: {password}\n\n----------------\nCreated On: {current_datetime}\n\n")

def generate_random_email(first_name):
    base_email = "phekdey@yandex.com"
    mail_digit = ''.join(random.choices(string.digits, k=3))  # Generate 3 random digits
    generated_email = base_email.split('@')[0] + f'+{first_name.lower()}{mail_digit}@' + base_email.split('@')[1]
    return generated_email

def generate_random_age():
    age = random.randint(18, 85)
    return age

def generate_strong_password():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%&"
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols)
    ]
    all_characters = lower + upper + digits + symbols
    length = random.randint(8, 14)
    password += random.choices(all_characters, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

def generate_random_phone_number():
    phone_file_path = r"C:\Code Workpace\VS Code\Reg FB Acc\Data\Phone Number\usa_phone_number.txt"
    with open(phone_file_path, "r") as file:
        phone_numbers = [line.strip() for line in file if line.strip()]
    random_phone_number = random.choice(phone_numbers)
    return random_phone_number

def load_names_from_file(file_path):
    with open(file_path, 'r') as file:
        names = [line.strip() for line in file if line.strip()]
    return names

def generate_random_first_name(gender):
    if gender.lower() == "female":
        file_path = r"C:\Code Workpace\VS Code\Reg FB Acc\Data\Name\USA\usa_first_name_female.txt"
    elif gender.lower() == "male":
        file_path = r"C:\Code Workpace\VS Code\Reg FB Acc\Data\Name\USA\usa_first_name_male.txt"
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    first_names = load_names_from_file(file_path)
    return random.choice(first_names)

def generate_random_last_name():
    file_path = r"C:\Code Workpace\VS Code\Reg FB Acc\Data\Name\USA\usa_last_name.txt"
    last_names = load_names_from_file(file_path)
    return random.choice(last_names)

def determine_gender_from_xpaths(clicked_xpaths):
    gender_map = {
        "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div[1]/div[1]": 'Female',
        "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div[1]": 'Male'
    }
    for xpath in clicked_xpaths:
        if xpath in gender_map:
            return gender_map[xpath]
    raise ValueError("Selected XPaths did not match any gender.")




#Get
gender = determine_gender_from_xpaths(xpaths)
first_name = generate_random_first_name(gender)
last_name = generate_random_last_name()
email = generate_random_email(first_name)
age = generate_random_age()
password = generate_strong_password()
phone_number = generate_random_phone_number()


def start_v2():
    driver.get("https://m.facebook.com/reg")
    driver.implicitly_wait(5)
    time.sleep(3)
    
    logging.info("-----------------Create new account-----------------")

    
    logging.info("Email: " + colorama.Fore.BLUE + f" {email}")
    logging.info("First Name: " + colorama.Fore.BLUE + f" {first_name}")
    logging.info("Last Name: " + colorama.Fore.BLUE + f" {last_name}")
    logging.info("DOB: " + colorama.Fore.BLUE + f" {age}")
    logging.info("Password: " + colorama.Fore.BLUE + f" {password}")
    
    logging.info("-----------------Get Started-----------------")
    #Get Starte
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div[3]/div/div/div").click()
    time.sleep(3)
    #Firstname
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]/input").send_keys(first_name)
    time.sleep(3)
    #Lastname
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/input").send_keys(last_name)
    time.sleep(3)
    #Next
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[3]/div/div/div/div").click()
    time.sleep(3)
    #Next
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[3]/div/div/div/div").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[3]/div/div/div/div").click()
    time.sleep(2)
    #Age
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/input").send_keys(age)
    time.sleep(3)
    #Next Age
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[3]/div/div/div[1]/div/div/div").click()
    time.sleep(2)
    #Confirm Age
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]").click()
    time.sleep(2)
    #Gender
    random_click_elements(xpaths)
    #Next Gender
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[3]/div/div/div/div").click()
    time.sleep(4)
    #Add Phone Number
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/input").send_keys(phone_number)
    time.sleep(3)
    #Next Phone
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[3]/div/div[1]/div/div/div").click()
    time.sleep(5)
    #Add Password
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/input").send_keys(password)
    time.sleep(5)
    
    
    
    
    logging.info("-----------------Save Account-----------------")
    writen_to_file(first_name, last_name, age, phone_number, email, password)
    
    #Exit
    finish()
    

def finish():
    driver.quit()
    # time.sleep(60)
    # start_v2()

if __name__ == "__main__":
    logging.info(colorama.Fore.GREEN + "Starting the script....")
    start_v2()


