from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('http://172.30.89.158:8000/')
    print(page.title())
    input("Press Enter to close the browser...")
    browser.close()
