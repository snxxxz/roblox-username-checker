import os
import requests
import pyperclip  # For copying to clipboard
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def validate_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            print(f"{Fore.GREEN}The username '{username}' is valid and available{Style.RESET_ALL}")
            with open('valid.txt', 'a') as file:
                file.write(username + '\n')
            return True
        elif data['code'] == 1:
            print(f"{Fore.RED}The username '{username}' is already in use{Style.RESET_ALL}")
        elif data['code'] == 2:
            print(f"{Fore.RED}The username '{username}' is not appropriate for Roblox{Style.RESET_ALL}")
        elif data['code'] == 10:
            print(f"{Fore.YELLOW}The username '{username}' might contain private information{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Unable to access Roblox API{Style.RESET_ALL}")
    return False

def validate_usernames_from_file(filename):
    with open(filename, "r") as file:
        usernames = file.read().splitlines()
    for username in usernames:
        if validate_username(username):
            break  # Stop if a valid username is found

def generate_and_check_username():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(script_dir, "chromedriver")
    html_file_path = os.path.join(script_dir, "username_generator.html")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        while True:
            # Load the local HTML file
            driver.get(f"file:///{html_file_path.replace('\\', '/')}")
            
            # Wait until the "Generate 4-Letter Name" button is clickable
            wait = WebDriverWait(driver, 10)  # 10-second timeout
            generate_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Generate 4-Letter Name"]')))
            generate_button.click()
            
            # Wait until the generated name appears
            generated_name = wait.until(EC.visibility_of_element_located((By.ID, 'name'))).text
            print(f"{Fore.BLUE}Generated name: {generated_name}{Style.RESET_ALL}")

            # Validate the username on Roblox
            if validate_username(generated_name):
                # Ask user if they want to copy the name
                copy_choice = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Do you want to copy the username to clipboard? (yes/no): ").strip().lower()
                if copy_choice == 'yes':
                    pyperclip.copy(generated_name)
                    print(f"{Fore.GREEN}The username '{generated_name}' has been copied to the clipboard.{Style.RESET_ALL}")
                break  # Exit the loop if a valid username is found
            
            # Sleep or wait for a short period if necessary
            # time.sleep(2)  # Optional: Add a delay if you want to throttle the generation

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

while True:
    print()
    os.system('cls' if os.name == 'nt' else 'clear')
    # Updated banner with color green
    print(f"{Fore.GREEN}█████  █████  █████████  ██████████ ███████████   ██████   █████   █████████   ██████   ██████ ██████████")
    print(f"░░███  ░░███  ███░░░░░███░░███░░░░░█░░███░░░░░███ ░░██████ ░░███   ███░░░░░███ ░░██████ ██████ ░░███░░░░░█")
    print(f" ░███   ░███ ░███    ░░░  ░███  █ ░  ░███    ░███  ░███░███ ░███  ░███    ░███  ░███░█████░███  ░███  █ ░ ")
    print(f" ░███   ░███ ░░█████████  ░██████    ░██████████   ░███░░███░███  ░███████████  ░███░░███ ░███  ░██████   ")
    print(f" ░███   ░███  ░░░░░░░░███ ░███░░█    ░███░░░░░███  ░███ ░░██████  ░███░░░░░███  ░███ ░░░  ░███  ░███░░█   ")
    print(f" ░███   ░███  ███    ░███ ░███ ░   █ ░███    ░███  ░███  ░░█████  ░███    ░███  ░███      ░███  ░███ ░   █")
    print(f" ░░████████  ░░█████████  ██████████ █████   █████ █████  ░░█████ █████   █████ █████     █████ ██████████")
    print(f"  ░░░░░░░░    ░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░ ░░░░░   ░░░░░ ░░░░░     ░░░░░ ░░░░░░░░░░{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Choose an option:")
    print(f"{Fore.GREEN}[{Fore.RESET}1{Fore.GREEN}]{Fore.RESET} Manually enter a username")
    print(f"{Fore.GREEN}[{Fore.RESET}2{Fore.GREEN}]{Fore.RESET} Check a list of usernames from a file")
    print(f"{Fore.GREEN}[{Fore.RESET}3{Fore.GREEN}]{Fore.RESET} Use local HTML to generate and check usernames")
    print(f"{Fore.GREEN}[{Fore.RESET}0{Fore.GREEN}]{Fore.RESET} Exit")
    
    choice = input(f"{Fore.GREEN}[{Fore.RESET}>{Fore.GREEN}]{Fore.RESET} ")
    
    if choice == '1':
        while True:
            username = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter a username: ")
            validate_username(username)
            # The loop runs indefinitely; no prompt to continue
    elif choice == '2':
        filename = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter the filename of the usernames file (must include .txt): ")
        validate_usernames_from_file(filename)
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Finished checking all usernames in the file.")
    elif choice == '3':
        generate_and_check_username()
    elif choice == '0':
        break
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
