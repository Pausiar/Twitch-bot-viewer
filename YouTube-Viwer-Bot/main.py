import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

def check_for_updates():
    try:
        print("[INFO] Checking for updates...")
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/version.txt")
        remote_version = r.content.decode('utf-8').strip()
        local_version = open('version.txt', 'r').read().strip()
        if remote_version != local_version:
            print("[WARNING] A new version is available. Please update.")
            time.sleep(3)
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Could not check for updates: {e}")
        return True


def main():
    try:
        if not check_for_updates():
            return

        # Lista de proxys
        proxy_servers = {
            1: "https://www.blockaway.net",
            2: "https://www.croxyproxy.com",
            3: "https://www.croxyproxy.rocks",
            4: "https://www.croxy.network",
            5: "https://www.croxy.org",
            6: "https://www.youtubeunblocked.live",
            7: "https://www.croxyproxy.net",
        }

        print("[INFO] Proxy Server 1 is recommended.")
        for i in range(1, 7):
            print(f"[{i}] {proxy_servers[i]}")

        proxy_choice = int(input("> Select a proxy (1-7): "))
        proxy_url = proxy_servers.get(proxy_choice)

        if proxy_url is None:
            print("[ERROR] Invalid proxy selected. Exiting.")
            return

        twitch_username = input("> Enter your Twitch username: ")
        proxy_count = int(input("> How many proxy sites do you want to open? "))

        print("[INFO] Starting WebDriver...")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--disable-dev-shm-usage')

        try:
            driver = webdriver.Chrome(options=chrome_options)
            print("[SUCCESS] WebDriver started.")
        except Exception as e:
            print(f"[ERROR] Could not start WebDriver: {e}")
            return

        print(f"[INFO] Opening proxy: {proxy_url}")
        driver.get(proxy_url)

        for i in range(proxy_count):
            print(f"[INFO] Opening proxy window {i+1}/{proxy_count}...")
            driver.execute_script("window.open('" + proxy_url + "')")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)

            try:
                print("[INFO] Looking for input field...")
                text_box = driver.find_element(By.ID, 'url')
                text_box.send_keys(f'www.youtube.com/@{twitch_username}')
                text_box.send_keys(Keys.RETURN)
                print("[SUCCESS] Viewer sent.")
            except Exception as e:
                print(f"[ERROR] Could not send viewer: {e}")

        input("[INFO] Press Enter to close all windows...")
        driver.quit()

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == '__main__':
    main()
