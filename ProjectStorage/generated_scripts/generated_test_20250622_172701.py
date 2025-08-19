import asyncio
import re
import sys
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.saucedemo.com/")

        # Successful Login
        await page.get_by_placeholder("Username").fill("standard_user")
        await page.get_by_placeholder("Password").fill("secret_sauce")
        await page.get_by_role("button", name="login-button").click()
        await expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()

        # Add Product to Cart
        await page.get_by_text("Sauce Labs Backpack").click()
        await page.get_by_text("Add to cart").click()
        await expect(page.get_by_text("1 item")).to_be_visible()

        # Remove Product from Cart
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.get_by_text("Remove").click()
        await expect(page.get_by_text("0 items")).to_be_visible()

        # Checkout with Valid Information
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.get_by_role("button", name="checkout-button").click()
        await page.get_by_placeholder("First name").fill("John")
        await page.get_by_placeholder("Last name").fill("Doe")
        await page.get_by_placeholder("postal-code").fill("10001")
        await page.get_by_role("button", name="continue-button").click()
        await expect(page.get_by_text("Order: Success!")).to_be_visible()

        # Submit Order
        await page.goto("https://www.saucedemo.com/checkout-step-two.html")
        await page.get_by_role("button", name="finish-button").click()
        await expect(page.get_by_text("Order: Success!")).to_be_visible()

        # Empty Cart Checkout
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.get_by_role("button", name="checkout-button").click()
        await expect(page.get_by_text("Your cart is empty")).to_be_visible()

        # Invalid ZIP Code
        await page.goto("https://www.saucedemo.com/checkout-step-two.html")
        await page.get_by_placeholder("postal-code").fill("invalid_zip")
        await page.get_by_role("button", name="continue-button").click()
        await expect(page.get_by_text("Error: Postal code is invalid")).to_be_visible()

        # Network Failure During Order Submission
        await page.goto("https://www.saucedemo.com/checkout-step-two.html")
        await page.get_by_role("button", name="finish-button").click()
        await expect(page.get_by_text("Network error occurred")).to_be_visible()

if __name__ == "__main__":
    asyncio.run(main())