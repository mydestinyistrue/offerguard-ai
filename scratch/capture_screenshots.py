import os
import time
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath("docs/screenshots")
os.makedirs(output_dir, exist_ok=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome_path, headless=True)
    # Use standard 16:9 1280x760 viewport, device scale factor 2
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        device_scale_factor=2,
    )
    page = context.new_page()

    print("Navigating to http://localhost:5173...")
    page.goto("http://localhost:5173", wait_until="networkidle")
    time.sleep(1.5)

    # Click on 'Try Sample Scams' in Hero
    print("Clicking 'Try Sample Scams'...")
    try_btn = page.query_selector("button:has-text('Try Sample Scams')")
    if try_btn:
        try_btn.click()
        time.sleep(0.5)

    # Click Run Check
    print("Clicking 'Run Check'...")
    run_btn = page.query_selector("button:has-text('Run Check')")
    if run_btn:
        run_btn.click()
    else:
        page.click("button:has-text('Check an Offer Free')")

    # Wait for the Result Dialog
    print("Waiting for Verification Result dialog...")
    page.wait_for_selector("text=Verification Result", timeout=25000)
    time.sleep(1.5)

    # Screenshot 1: Result Dialog (centered modal with Risk Gauge & Verdict)
    path1 = os.path.join(output_dir, "screenshot1_verdict_gauge.png")
    page.screenshot(path=path1)
    print("Saved Screenshot 1:", path1)

    # Click 'View Detailed Report'
    print("Clicking 'View Detailed Report'...")
    page.click("button:has-text('View Detailed Report')")
    time.sleep(1.5)

    # Screenshot 2: Stage Timeline & Next Move Card
    print("Capturing Stage Radar & Next Move Card...")
    # Scroll slightly down so Stage Radar and Next Move card are in optimal view
    page.evaluate("window.scrollTo(0, 380)")
    time.sleep(1)
    path2 = os.path.join(output_dir, "screenshot2_stage_radar.png")
    page.screenshot(path=path2)
    print("Saved Screenshot 2:", path2)

    # Screenshot 3: Report Pack (1930 Cybercrime complaint draft)
    print("Capturing 1930 Cybercrime Report Pack...")
    # Scroll further down to ReportPack
    page.evaluate("window.scrollTo(0, 1100)")
    time.sleep(1)
    path3 = os.path.join(output_dir, "screenshot3_1930_fir_pack.png")
    page.screenshot(path=path3)
    print("Saved Screenshot 3:", path3)

    browser.close()
    print("SUCCESS: All 3 screenshots captured!")
