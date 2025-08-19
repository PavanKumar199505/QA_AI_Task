import asyncio
import re
import sys
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.saucedemo.com/")

        await page.get_by_role("button", name="login").click()
        await page.get_by_placeholder("Username").fill("standard_user")
        await page.get_by_placeholder("Password").fill("secret_sauce")
        await page.locator("#login-button").click()

        await page.get_by_text("Product catalog").click()

        await page.get_by_text("Sauce Labs Backpack").click()
        await page.locator("#cart_contents_container").click()

        await page.get_by_text("Sauce Labs Backpack").click()
        await page.locator("#remove-sauce-labs-backpack").click()

        await page.get_by_text("Checkout").click()

        await page.get_by_placeholder("First name").fill("John")
        await page.get_by_placeholder("Last name").fill("Doe")
        await page.get_by_placeholder("Postal code").fill("12345")

        await page.get_by_text("Continue").click()
        await page.get_by_text("Finish").click()

        await page.get_by_text("Checkout").click()

        await page.get_by_placeholder("First name").fill("John")
        await page.get_by_placeholder("Last name").fill("Doe")
        await page.get_by_placeholder("Postal code").fill("Invalid ZIP Code")
        await page.get_by_text("Continue").click()

        await page.get_by_text("Finish").click()

asyncio.get_event_loop().run_until_complete(main())