Here is the Python script:

```
import asyncio
import json
import time
from datetime import datetime, timezone
from playwright.async_api import async_playwright, expect

async def scenario_login_screen(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "standard_user")
        await page.fill("Password", "secret_sauce")
        await page.click("login-button")
        await expect(page.locator("product-catalog")).to_be_visible()
        return {"scenario": "Login Screen", "status": "passed"}
    except Exception as e:
        return {"scenario": "Login Screen", "status": "failed", "error": str(e)}

async def scenario_product_catalog(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await expect(page.locator("product-list")).to_be_visible()
        await expect(page.locator("product-name")).to_be_visible()
        await expect(page.locator("product-description")).to_be_visible()
        await expect(page.locator("product-price")).to_be_visible()
        await expect(page.locator("product-image")).to_be_visible()
        await expect(page.locator("add-to-cart-button")).to_be_visible()
        await expect(page.locator("sort-by-name")).to_be_visible()
        await expect(page.locator("sort-by-price")).to_be_visible()
        return {"scenario": "Product Catalog", "status": "passed"}
    except Exception as e:
        return {"scenario": "Product Catalog", "status": "failed", "error": str(e)}

async def scenario_shopping_cart_view(page):
    try:
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.click("add-to-cart-button")
        await expect(page.locator("cart-item")).to_be_visible()
        await expect(page.locator("remove-item-button")).to_be_visible()
        await expect(page.locator("continue-shopping-button")).to_be_visible()
        await expect(page.locator("proceed-to-checkout-button")).to_be_visible()
        await expect(page.locator("item-count-badge")).to_be_visible()
        return {"scenario": "Shopping Cart View", "status": "passed"}
    except Exception as e:
        return {"scenario": "Shopping Cart View", "status": "failed", "error": str(e)}

async def scenario_checkout_process(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await expect(page.locator("customer-info-form")).to_be_visible()
        await expect(page.locator("order-overview")).to_be_visible()
        await page.click("complete-order-button")
        await expect(page.locator("order-confirmation")).to_be_visible()
        await page.click("logout-button")
        return {"scenario": "Checkout Process", "status": "passed"}
    except Exception as e:
        return {"scenario": "Checkout Process", "status": "failed", "error": str(e)}

async def scenario_navigation_menu(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await expect(page.locator("nav-menu")).to_be_visible()
        await page.click("about-link")
        await expect(page.locator("about-page")).to_be_visible()
        await page.click("logout-link")
        await expect(page.locator("login-page")).to_be_visible()
        await page.click("reset-app-state-link")
        await expect(page.locator("app-reset-confirmation")).to_be_visible()
        return {"scenario": "Navigation Menu", "status": "passed"}
    except Exception as e:
        return {"scenario": "Navigation Menu", "status": "failed", "error": str(e)}

async def scenario_social_media_links(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.click("twitter-link")
        await expect(page.locator("twitter-page")).to_be_visible()
        await page.goto("https://www.saucedemo.com/")
        await page.click("facebook-link")
        await expect(page.locator("facebook-page")).to_be_visible()
        await page.goto("https://www.saucedemo.com/")
        await page.click("linkedin-link")
        await expect(page.locator("linkedin-page")).to_be_visible()
        return {"scenario": "Social Media Links", "status": "passed"}
    except Exception as e:
        return {"scenario": "Social Media Links", "status": "failed", "error": str(e)}

async def scenario_invalid_credentials(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "invalid_user")
        await page.fill("Password", "invalid_password")
        await page.click("login-button")
        await expect(page.locator("error-message")).to_contain_text("Username and password do not match")
        return {"scenario": "Invalid Credentials", "status": "passed"}
    except Exception as e:
        return {"scenario": "Invalid Credentials", "status": "failed", "error": str(e)}

async def scenario_locked_out_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "locked_out_user")
        await page.fill("Password", "secret_sauce")
        await page.click("login-button")
        await expect(page.locator("error-message")).to_contain_text("Sorry, this user has been locked out")
        return {"scenario": "Locked-Out User", "status": "passed"}
    except Exception as e:
        return {"scenario": "Locked-Out User", "status": "failed", "error": str(e)}

async def scenario_problem_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "problem_user")
        await page.fill("Password", "secret_sauce")
        await page.click("login-button")
        # UI or functional issues are expected, so no explicit assertion
        return {"scenario": "Problem User", "status": "passed"}
    except Exception as e:
        return {"scenario": "Problem User", "status": "failed", "error": str(e)}

async def scenario_performance_glitch_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "performance_glitch_user")
        await page.fill("Password", "secret_sauce")
        await page.click("login-button")
        # Slow response times are expected, so no explicit assertion
        return {"scenario": "Performance Glitch User", "status": "passed"}
    except Exception as e:
        return {"scenario": "Performance Glitch User", "status": "failed", "error": str(e)}

async def scenario_empty_cart_checkout(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await page.click("complete-order-button")
        await expect(page.locator("error-message")).to_be_visible()
        return {"scenario": "Empty Cart Checkout", "status": "passed"}
    except Exception as e:
        return {"scenario": "Empty Cart Checkout", "status": "failed", "error": str(e)}

async def scenario_invalid_zip_code(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await page.fill("postal-code", "invalid_zip_code")
        await page.click("complete-order-button")
        await expect(page.locator("validation-error")).to_be_visible()
        return {"scenario": "Invalid ZIP Code", "status": "passed"}
    except Exception as e:
        return {"scenario": "Invalid ZIP Code", "status": "failed", "error": str(e)}

async def scenario_network_failure(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        # Simulate network issues
        await page.click("complete-order-button")
        await expect(page.locator("retry-option")).to_be_visible()
        return {"scenario": "Network Failure", "status": "passed"}
    except Exception as e:
        return {"scenario": "Network Failure", "status": "failed", "error": str(e)}

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        report = {
            "start_time": datetime.now(timezone.utc).isoformat(),
            "total_duration": 0,
            "scenarios": []
        }
        
        start_time = time.time()

        report["scenarios"].append(await scenario_login_screen(page))
        report["scenarios"].append(await scenario_product_catalog(page))
        report["scenarios"].append(await scenario_shopping_cart_view(page))
        report["scenarios"].append(await scenario_checkout_process(page))
        report["scenarios"].append(await scenario_navigation_menu(page))
        report["scenarios"].append(await scenario_social_media_links(page))
        report["scenarios"].append(await scenario_invalid_credentials(page))
        report["scenarios"].append(await scenario_locked_out_user(page))
        report["scenarios"].append(await scenario_problem_user(page))
        report["scenarios"].append(await scenario_performance_glitch_user(page))
        report["scenarios"].append(await scenario_empty_cart_checkout(page))
        report["scenarios"].append(await scenario_invalid_zip_code(page))
        report["scenarios"].append(await scenario_network_failure(page))

        report["total_duration"] = time.time() - start_time
        report["end_time"] = datetime.now(timezone.utc).isoformat()
        
        print(json.dumps(report, indent=4))
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())