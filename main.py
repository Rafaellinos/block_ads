import os
import shutil
import urllib.request
from datetime import datetime
import sys
import subprocess

# URL of the hosts file
hosts_url = "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt"

# Path to the hosts file
hosts_path = "/etc/hosts"

def download_hosts_file(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print("Error downloading the hosts file:", e)
        return None

def append_to_hosts_file(content, path):
    try:
        with open(path, "a") as file:
            file.write("\n" + content)
            print("Hosts file updated successfully.")
    except Exception as e:
        print("Error appending to hosts file:", e)

def backup_hosts_file(path):
    try:
        backup_folder = os.path.dirname(path)
        backup_filename = "hosts_bpk_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_folder, backup_filename)
        shutil.copy2(path, backup_path)
        print("Backup created successfully:", backup_path)
    except Exception as e:
        print("Error creating backup:", e)

def restart_systemd_hostnamed():
    try:
        subprocess.run(["systemctl", "restart", "systemd-hostnamed"])
        print("systemd-hostnamed restarted successfully.")
    except Exception as e:
        print("Error restarting systemd-hostnamed:", e)

def main():
    # Create a backup of the hosts file
    backup_hosts_file(hosts_path)

    # Download the hosts file
    hosts_content = download_hosts_file(hosts_url)
    if hosts_content:
        # Append to the hosts file
        append_to_hosts_file(hosts_content, hosts_path)
        restart_systemd_hostnamed()

if __name__ == "__main__":
    # Check if running as root
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit()
    main()

