
import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.saucedemo.com/login")

        await page.fill('[placeholder*="Username" i]', 'standard_user')
        await page.fill('[placeholder*="Password" i]', 'secret_sauce')
        await page.get_by_role("button", name="login").click()

        await page.goto("https://www.saucedemo.com/inventory.html")

        await page.get_by_text("Sauce Labs Backpack").click()

        await page.goto("https://www.saucedemo.com/cart.html")

        await page.get_by_role("button", name="remove-sauce-labs-backpack").click()

        await page.goto("https://www.saucedemo.com/cart.html")

        await page.fill('[placeholder*="First Name" i]', 'John')
        await page.fill('[placeholder*="Last Name" i]', 'Doe')
        await page.fill('[placeholder*="Postal Code" i]', '12345')

        await page.goto("https://www.saucedemo.com/cart.html")

        await page.get_by_role("button", name="continue").click()
        await page.get_by_role("button", name="finish").click()

        await page.goto("https://www.saucedemo.com/cart.html")

        await page.get_by_role("button", name="checkout").click()

        await page.goto("https://www.saucedemo.com/checkout-step-one.html")

        await page.fill('[placeholder*="Postal Code" i]', 'Invalid ZIP Code')
        await page.get_by_role("button", name="continue").click()

        await page.goto("https://www.saucedemo.com/checkout-step-one.html")

        await page.get_by_role("button", name="finish").click()

if __name__ == "__main__":
    asyncio.run(main())
