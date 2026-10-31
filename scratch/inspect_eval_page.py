import os, time
from playwright.sync_api import sync_playwright

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome_path, headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://localhost:5173/eval", wait_until="networkidle")
    time.sleep(2)

    # Capture what's on the page
    text_content = page.inner_text("body")
    print("=== EVAL PAGE TEXT START ===")
    print(text_content[:2000])
    print("=== EVAL PAGE TEXT END ===")

    page.screenshot(path="docs/screenshots/eval_page_inspect.png")
    browser.close()
