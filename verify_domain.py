
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Login as Demo Admin to access Help page
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("button:has-text('Mode Demo')")
        page.wait_for_selector("#stat-warga")

        # Go to Help Page
        if not page.is_visible("button:has-text('Panduan & Code')"):
             page.click("#sidebar-toggle-btn")
             page.wait_for_timeout(500)

        page.click("button:has-text('Panduan & Code')")
        page.wait_for_selector("#page-help", state="visible")

        # Check for new domain text
        content = page.content()
        if "sirt.isparmo.com" in content:
            print("PASS: New domain found in Help Page")
        else:
            print("FAIL: New domain not found")

        if "rt08-royal2" in content:
            print("PASS: Example RT found in Help Page")
        else:
            print("FAIL: Example RT not found")

        page.screenshot(path="verify_domain_update.png")
        browser.close()

if __name__ == "__main__":
    run()
