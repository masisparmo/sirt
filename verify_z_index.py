
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for Setup Modal
        page.wait_for_selector("#modal-setup", state="visible")

        # We need to simulate the condition where progress-modal is open at the same time as modal-setup
        # to verify z-index

        page.evaluate("""() => {
            const p = document.getElementById('progress-modal');
            p.classList.remove('hidden');
            p.classList.add('flex');
        }""")

        # Check if progress modal is visible and ON TOP
        # We can check bounding box or z-index computed style

        progress_z = page.evaluate("window.getComputedStyle(document.getElementById('progress-modal')).zIndex")
        setup_z = page.evaluate("window.getComputedStyle(document.getElementById('modal-setup')).zIndex")

        print(f"Progress Z-Index: {progress_z}")
        print(f"Setup Z-Index: {setup_z}")

        if int(progress_z) > int(setup_z):
            print("PASS: Progress modal is above Setup modal")
        else:
            print("FAIL: Progress modal is below or equal to Setup modal")

        page.screenshot(path="verify_z_index.png")
        browser.close()

if __name__ == "__main__":
    run()
