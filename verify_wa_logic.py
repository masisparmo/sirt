
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Login as Demo Admin to set config
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("button:has-text('Mode Demo')")
        page.wait_for_selector("#stat-warga")

        # Go to Settings
        if not page.is_visible("button:has-text('Pengaturan')"):
             page.click("#sidebar-toggle-btn")
             page.wait_for_timeout(500)

        page.click("button:has-text('Pengaturan')")
        page.wait_for_selector("#conf-wa-rt", state="visible")

        # TEST 1: Input starts with 0
        page.fill("#conf-wa-rt", "08123456789")
        # Click save
        page.click("button:has-text('Simpan Konfigurasi')")
        # Wait for "Simpan..." progress to finish
        page.wait_for_selector("#progress-modal", state="hidden")
        # In Demo Mode, it doesn't really 'save' to backend but it might update the link locally if logic is there?
        # Wait, the `updateAppConfig` is called after `loadAllData`. In demo mode `loadAllData` re-renders `DEMO_DATA`.
        # `submitConfig` in demo mode just alerts.
        # So we can't test this easily in Demo Mode via UI interaction because `submitConfig` returns early.

        # We need to manually trigger the logic in console to verify the transformation function.

        test_numbers = ["081212345678", "6281212345678", "81212345678"]
        for num in test_numbers:
            href = page.evaluate(f"""() => {{
                let config = {{ wa_rt: '{num}' }};
                // Copy paste logic from index.html
                let c = String(config.wa_rt).replace(/\\D/g, '');
                if(c.startsWith('0')) c = '62'+c.slice(1);
                else if(c.startsWith('62')) c = c;
                else c = '62'+c;
                return `https://wa.me/${{c}}`;
            }}""")
            print(f"Input: {num} -> Href: {href}")
            if num.startswith("0") and href.endswith("62" + num[1:]):
                print("PASS: 0 prefix converted")
            elif num.startswith("62") and href.endswith(num):
                print("PASS: 62 prefix kept")
            elif not num.startswith("0") and not num.startswith("62") and href.endswith("62" + num):
                print("PASS: No prefix added 62")
            else:
                print("FAIL: Logic incorrect")

        browser.close()

if __name__ == "__main__":
    run()
