from pathlib import Path

import asyncio

from playwright.async_api import async_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "screenshots"
URL = "http://127.0.0.1:8507"


async def save_screenshots():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True,
        )
        pages = [("01_operations", ""), ("02_waste_monitor", "Waste Monitor"), ("03_markdown_planner", "Markdown Planner"), ("04_production_review", "Production Review"), ("05_import_data", "Import Data"), ("06_data_notes", "Data Notes")]
        for filename, requested_page in pages:
            page = await browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
            url = URL if not requested_page else f"{URL}/?page={requested_page.replace(' ', '%20')}"
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(3000)
            if not requested_page:
                button = page.get_by_role("button", name="Open dashboard")
                if await button.count():
                    await button.click()
                    await page.wait_for_timeout(2500)
            await page.screenshot(path=str(OUTPUT / f"{filename}.png"), full_page=True)
            await page.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(save_screenshots())
