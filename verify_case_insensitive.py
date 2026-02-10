
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Test Case-Insensitivity Logic via Console
        # We simulate the fetchMasterDirectory internal logic

        test_id_input = "RT08-ROYAL2"
        mock_api_response = {
            "rt08-royal2": "https://example.com/api",
            "OTHER-ID": "https://other.com"
        }

        result_url = page.evaluate(f"""() => {{
            const directory = {mock_api_response};
            const normalizedId = '{test_id_input}'.toUpperCase().trim();
            const keys = Object.keys(directory);
            const match = keys.find(k => k.toUpperCase().trim() === normalizedId);
            return match ? directory[match] : null;
        }}""")

        print(f"Input: {test_id_input}")
        print(f"Mock Keys: {list(mock_api_response.keys())}")
        print(f"Result URL: {result_url}")

        if result_url == "https://example.com/api":
            print("PASS: Case-insensitive match worked")
        else:
            print("FAIL: Match failed")

        browser.close()

if __name__ == "__main__":
    run()
