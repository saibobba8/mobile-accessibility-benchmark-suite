import os
import json
import csv
from appium import webdriver
from appium.options.android import UiAutomator2Options

def run_benchmark():
    config_path = "apps_config.json"
    builds_dir = "builds"
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "benchmark_results.csv")

    # Initialize CSV header if file doesn't exist
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["app_name", "version", "screen_name", "total_interactive_elements", "violations_under_24px", "failure_rate_pct"])

    if not os.path.exists(config_path):
        print(f"Configuration file {config_path} not found.")
        return

    with open(config_path, "r") as f:
        apps = json.load(f)

    for app in apps:
        apk_filename = f"{app['package_name']}.apk"
        apk_path = os.path.join(builds_dir, apk_filename)

        if not os.path.exists(apk_path):
            print(f"Skipping {app['app_name']}: APK file not found locally at {apk_path}.")
            continue

        print(f"\n[BENCHMARK] Auditing application: {app['app_name']} (v{app['version']})")

        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "Android Emulator"
        options.automation_name = "UiAutomator2"
        options.app = os.path.abspath(apk_path)
        options.no_reset = True

        driver = None
        try:
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            driver.implicitly_wait(10)

            # Query interactive elements for WCAG 2.2 spatial compliance check
            elements = driver.find_elements("xpath", "//*[@clickable='true' or @focusable='true']")
            total_elements = len(elements)
            violations = 0

            for el in elements:
                size = el.size
                if size['width'] < 24 or size['height'] < 24:
                    violations += 1

            failure_rate = (violations / total_elements * 100) if total_elements > 0 else 0.0
            screen_name = "Home_Dashboard"

            # Append empirical results to CSV dataset
            with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([app['app_name'], app['version'], screen_name, total_elements, violations, round(failure_rate, 2)])

            print(f"[SUCCESS] {violations}/{total_elements} elements failed the 24x24px threshold ({round(failure_rate, 2)}% failure rate).")

        except Exception as e:
            print(f"[ERROR] Failed during benchmark execution for {app['app_name']}: {e}")
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

if __name__ == "__main__":
    run_benchmark()
