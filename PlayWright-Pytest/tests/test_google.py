import re
from playwright.sync_api import expect

def test_youtube_search(page):
    page.wait_for_timeout(2000) 
    page.goto("https://www.google.com/ncr")

    try:
        page.get_by_role("button", name="Accept all").click(timeout=3000)
    except:
        print("No PopUp to accept")

    page.get_by_role("combobox", name="search").fill("Playwright Python")
    page.keyboard.press("Enter")
    expect(page).to_have_title(re.compile("Playwright", re.IGNORECASE))
    
    # page.pause() 
