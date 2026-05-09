from playwright.sync_api import expect

def test_selinux(page):
    page.goto("http://192.168.1.13")
    print(page.title())
    expect(page).to_have_title("HTTP Server Test Page powered by: Rocky Linux")
    # page.pause()
