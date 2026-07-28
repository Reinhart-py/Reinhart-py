import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Listen for console messages and page errors
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        
        url = "file:///" + os.path.abspath("dark.svg").replace("\\", "/")
        print(f"Opening local SVG: {url}")
        await page.goto(url)
        await page.wait_for_timeout(2000)
        
        await browser.close()

if __name__ == "__main__":
    import os
    asyncio.run(main())
