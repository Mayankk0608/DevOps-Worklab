from playwright.sync_api import expect

def test_selinux_template(page):
    page.goto("http://100.72.14.56")
    expect(page.locator("h1")).to_contain_text("This page is served from")