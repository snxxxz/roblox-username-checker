import os
import requests
import pyperclip
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def validate_tiktok_username(username):
    url = f"https://www.tiktok.com/@{username}"
    response = requests.get(url)
    if response.status_code == 404:
        print(f"{Fore.GREEN}The TikTok username '{username}' is available{Style.RESET_ALL}")
        with open('valid_tiktok.txt', 'a') as file:
            file.write(username + '\n')
        copy_choice = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Do you want to copy the username to clipboard? (y/n): ").strip().lower()
        if copy_choice == 'y':
            pyperclip.copy(username)
            print(f"{Fore.GREEN}The username '{username}' has been copied to the clipboard.{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}The TikTok username '{username}' is already taken{Style.RESET_ALL}")
    return False

def validate_xbox_username(username):
    # Placeholder URL or method. Simulating all usernames as available.
    print(f"{Fore.YELLOW}Xbox username validation is currently unavailable. This option is for demonstration purposes only.{Style.RESET_ALL}")
    with open('valid_xbox.txt', 'a') as file:
        file.write(username + '\n')
    copy_choice = input(f"{Fore.YELLOW}[{Fore.RESET}+{Fore.YELLOW}]{Fore.RESET} Do you want to copy the username to clipboard? (y/n): ").strip().lower()
    if copy_choice == 'y':
        pyperclip.copy(username)
        print(f"{Fore.YELLOW}The username '{username}' has been copied to the clipboard.{Style.RESET_ALL}")
    return True

def validate_username(username, platform):
    if platform == 'roblox':
        url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                print(f"{Fore.GREEN}The Roblox username '{username}' is valid and available{Style.RESET_ALL}")
                with open('valid.txt', 'a') as file:
                    file.write(username + '\n')
                copy_choice = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Do you want to copy the username to clipboard? (y/n): ").strip().lower()
                if copy_choice == 'y':
                    pyperclip.copy(username)
                    print(f"{Fore.GREEN}The username '{username}' has been copied to the clipboard.{Style.RESET_ALL}")
                return True
            elif data['code'] == 1:
                print(f"{Fore.RED}The Roblox username '{username}' is already in use{Style.RESET_ALL}")
            elif data['code'] == 2:
                print(f"{Fore.RED}The Roblox username '{username}' is not appropriate for Roblox{Style.RESET_ALL}")
            elif data['code'] == 10:
                print(f"{Fore.YELLOW}The Roblox username '{username}' might contain private information{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Unable to access Roblox API{Style.RESET_ALL}")
    elif platform == 'tiktok':
        return validate_tiktok_username(username)
    elif platform == 'xbox':
        return validate_xbox_username(username)
    return False

def validate_usernames_from_file(filename, platform):
    with open(filename, "r") as file:
        usernames = file.read().splitlines()
    for username in usernames:
        if validate_username(username, platform):
            break  # Stop if a valid username is found

def generate_and_check_username(platform):
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
            driver.get(f"file:///{html_file_path.replace('\\', '/')}")
            wait = WebDriverWait(driver, 10)
            generate_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Generate 4-Letter Name"]')))
            generate_button.click()
            generated_name = wait.until(EC.visibility_of_element_located((By.ID, 'name'))).text

            if validate_username(generated_name, platform):
                break  # Exit the loop if a valid username is found

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def print_banner():
    print(f"{Fore.GREEN}█████  █████  █████████  ██████████ ███████████   ██████   █████   █████████   ██████   ██████ ██████████")
    print(f"░░███  ░░███  ███░░░░░███░░███░░░░░█░░███░░░░░███ ░░██████ ░░███   ███░░░░░███ ░░██████ ██████ ░░███░░░░░█")
    print(f" ░███   ░███ ░███    ░░░  ░███  █ ░  ░███    ░███  ░███░███ ░███  ░███    ░███  ░███░█████░███  ░███  █ ░ ")
    print(f" ░███   ░███ ░░█████████  ░██████    ░██████████   ░███░░███░███  ░███████████  ░███░░███ ░███  ░██████   ")
    print(f" ░███   ░███  ░░░░░░░░███ ░███░░█    ░███░░░░░███  ░███ ░░██████  ░███░░░░░███  ░███ ░░░  ░███  ░███░░█   ")
    print(f" ░███   ░███  ███    ░███ ░███ ░   █ ░███    ░███  ░███  ░░█████  ░███    ░███  ░███      ░███  ░███ ░   █")
    print(f" ░░████████  ░░█████████  ██████████ █████   █████ █████  ░░█████ █████   █████ █████     █████ ██████████")
    print(f"  ░░░░░░░░    ░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░ ░░░░░   ░░░░░ ░░░░░     ░░░░░ ░░░░░░░░░░{Style.RESET_ALL}")

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Choose a platform:")
    print(f"{Fore.GREEN}[{Fore.RESET}1{Fore.GREEN}]{Fore.RESET} Roblox")
    print(f"{Fore.GREEN}[{Fore.RESET}2{Fore.GREEN}]{Fore.RESET} TikTok")
    print(f"{Fore.GREEN}[{Fore.RESET}3{Fore.GREEN}]{Fore.RESET} Xbox (Unavailable)")
    print(f"{Fore.GREEN}[{Fore.RESET}0{Fore.GREEN}]{Fore.RESET} Exit")
    
    platform_choice = input(f"{Fore.GREEN}[{Fore.RESET}>{Fore.GREEN}]{Fore.RESET} ").strip()

    if platform_choice == '1':
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            print(f"{Fore.GREEN}You have selected Roblox.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[{Fore.RESET}1{Fore.GREEN}]{Fore.RESET} Manually enter a username")
            print(f"{Fore.GREEN}[{Fore.RESET}2{Fore.GREEN}]{Fore.RESET} Check a list of usernames from a file")
            print(f"{Fore.GREEN}[{Fore.RESET}3{Fore.GREEN}]{Fore.RESET} Use local HTML to generate and check usernames")
            print(f"{Fore.GREEN}[{Fore.RESET}0{Fore.GREEN}]{Fore.RESET} Back to platform selection")
            
            choice = input(f"{Fore.GREEN}[{Fore.RESET}>{Fore.GREEN}]{Fore.RESET} ").strip()

            if choice == '1':
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                    username = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter a username: ")
                    if validate_username(username, 'roblox'):
                        break
            elif choice == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                filename = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter the filename of the usernames file (must include .txt): ")
                validate_usernames_from_file(filename, 'roblox')
                print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Finished checking all usernames in the file.")
            elif choice == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                generate_and_check_username('roblox')
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

    elif platform_choice == '2':
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            print(f"{Fore.GREEN}You have selected TikTok.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[{Fore.RESET}1{Fore.GREEN}]{Fore.RESET} Manually enter a username")
            print(f"{Fore.GREEN}[{Fore.RESET}2{Fore.GREEN}]{Fore.RESET} Check a list of usernames from a file")
            print(f"{Fore.GREEN}[{Fore.RESET}3{Fore.GREEN}]{Fore.RESET} Use local HTML to generate and check usernames")
            print(f"{Fore.GREEN}[{Fore.RESET}0{Fore.GREEN}]{Fore.RESET} Back to platform selection")
            
            choice = input(f"{Fore.GREEN}[{Fore.RESET}>{Fore.GREEN}]{Fore.RESET} ").strip()

            if choice == '1':
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                    username = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter a username: ")
                    if validate_username(username, 'tiktok'):
                        break
            elif choice == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                filename = input(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter the filename of the usernames file (must include .txt): ")
                validate_usernames_from_file(filename, 'tiktok')
                print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Finished checking all usernames in the file.")
            elif choice == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                generate_and_check_username('tiktok')
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

    elif platform_choice == '3':
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            print(f"{Fore.YELLOW}You have selected Xbox (Unavailable).{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}This option is currently unavailable. Please choose another platform.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}[{Fore.RESET}Press Enter to return to platform selection{Fore.YELLOW}]")
            break

    elif platform_choice == '0':
        break
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
