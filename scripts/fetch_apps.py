import json
import os
import urllib.request

def fetch_apks(config_path="apps_config.json", output_dir="builds"):
    os.makedirs(output_dir, exist_ok=True)
    with open(config_path, "r") as f:
        apps = json.load(f)
        
    for app in apps:
        target_path = os.path.join(output_dir, f"{app['package_name']}.apk")
        if not os.path.exists(target_path):
            print(f"Downloading {app['app_name']}...")
            urllib.request.urlretrieve(app['apk_download_url'], target_path)
            print(f"Saved to {target_path}")

if __name__ == "__main__":
    fetch_apks()
