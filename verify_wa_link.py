
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # 1. Verify "Hubungi Admin Pusat" link in Setup Modal
        # This modal appears on load if no DB is configured.
        page.wait_for_selector("#modal-setup", state="visible")

        # Check href
        link_selector = "#modal-setup a[href*='wa.me']"
        if page.is_visible(link_selector):
            href = page.get_attribute(link_selector, "href")
            print(f"Setup Modal Link Href: {href}")
            if "628121083060" in href:
                print("PASS: Setup Modal link contains correct number")
            else:
                print("FAIL: Setup Modal link incorrect")
        else:
            print("FAIL: WhatsApp link not found in Setup Modal")

        page.screenshot(path="verify_wa_modal.png")

        # 2. Verify Help Page Link
        # Enter Demo Mode first to navigate
        page.click("button:has-text('Mode Demo')")
        page.on("dialog", lambda dialog: dialog.accept())
        page.wait_for_selector("#stat-warga")

        # Go to Help Page
        # Click "Panduan & Code" button in sidebar (or toggle sidebar first)
        if not page.is_visible("button:has-text('Panduan & Code')"):
             page.click("#sidebar-toggle-btn")
             page.wait_for_timeout(500)

        page.click("button:has-text('Panduan & Code')")
        page.wait_for_selector("#page-help", state="visible")

        # Check for WA link in Help
        help_wa_selector = "#page-help a[href*='wa.me']"
        if page.is_visible(help_wa_selector):
            href_help = page.get_attribute(help_wa_selector, "href")
            text_help = page.inner_text(help_wa_selector)
            print(f"Help Page Link Href: {href_help}, Text: {text_help}")
            if "628121083060" in href_help:
                 print("PASS: Help Page link contains correct number")
            else:
                 print("FAIL: Help Page link incorrect")
        else:
            print("FAIL: WhatsApp link not found in Help Page")

        page.screenshot(path="verify_wa_help.png")

        browser.close()

if __name__ == "__main__":
    run()
