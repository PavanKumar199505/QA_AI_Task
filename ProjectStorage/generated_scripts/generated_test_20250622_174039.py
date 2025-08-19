import asyncio
import re
import sys
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.saucedemo.com/")

        await page.get_by_role("button", name="login").click()
        await page.get_by_placeholder("Username").fill("standard_user")
        await page.get_by_placeholder("Password").fill("secret_sauce")
        await page.locator("#login-button").click()

        await page.get_by_text("Sauce Labs Backpack").click()
        await page.locator("#add-to-cart-button").click()

        await page.get_by_text("Sauce Labs Backpack").click()
        await page.locator("#remove-sauce-labs-backpack").click()

        await page.get_by_role("button", name="Checkout").click()
        await page.get_by_placeholder("First name").fill("John")
        await page.get_by_placeholder("Last name").fill("Doe")
        await page.get_by_placeholder("Postal code").fill("12345")
        await page.locator("#continue").click()

        await page.get_by_role("button", name="Checkout").click()
        await page.get_by_placeholder("First name").fill("John")
        await page.get_by_placeholder("Last name").fill("Doe")
        await page.get_by_placeholder("Postal code").fill("Invalid ZIP")
        await page.locator("#continue").click()

        await page.get_by_role("button", name="Checkout").click()
        await page.get_by_placeholder("First name").fill("John")
        await page.get_by_placeholder("Last name").fill("Doe")
        await page.get_by_placeholder("Postal code").fill("12345")
        await page.locator("#continue").click()

asyncio.run(main())