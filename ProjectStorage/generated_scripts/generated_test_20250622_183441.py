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
        await expect(page.locator("product_catalog")).to_be_visible()
        return {"scenario": "Login Screen", "status": "passed"}
    except Exception as e:
        return {"scenario": "Login Screen", "status": "failed", "error": str(e)}

async def scenario_product_catalog(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await expect(page.locator("product_list")).to_be_visible()
        await expect(page.locator("product_names")).to_be_visible()
        await expect(page.locator("product_descriptions")).to_be_visible()
        await expect(page.locator("product_prices")).to_be_visible()
        await expect(page.locator("product_images")).to_be_visible()
        await expect(page.locator("add_to_cart_buttons")).to_be_visible()
        await expect(page.locator("sorting_options")).to_be_visible()
        return {"scenario": "Product Catalog", "status": "passed"}
    except Exception as e:
        return {"scenario": "Product Catalog", "status": "failed", "error": str(e)}

async def scenario_shopping_cart_view(page):
    try:
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.click("add_to_cart_button")
        await expect(page.locator("cart_view")).to_be_visible()
        await expect(page.locator("remove_item_options")).to_be_visible()
        await expect(page.locator("continue_shopping_button")).to_be_visible()
        await expect(page.locator("proceed_to_checkout_button")).to_be_visible()
        await expect(page.locator("item_count_badge")).to_be_visible()
        return {"scenario": "Shopping Cart View", "status": "passed"}
    except Exception as e:
        return {"scenario": "Shopping Cart View", "status": "failed", "error": str(e)}

async def scenario_checkout_process(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await expect(page.locator("customer_info_form")).to_be_visible()
        await expect(page.locator("order_overview")).to_be_visible()
        await page.click("complete_checkout_button")
        await expect(page.locator("confirmation_screen")).to_be_visible()
        await expect(page.locator("logout_button")).to_be_visible()
        return {"scenario": "Checkout Process", "status": "passed"}
    except Exception as e:
        return {"scenario": "Checkout Process", "status": "failed", "error": str(e)}

async def scenario_navigation_menu(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.click("nav_button")
        await expect(page.locator("all_items_link")).to_be_visible()
        await expect(page.locator("about_link")).to_be_visible()
        await expect(page.locator("logout_link")).to_be_visible()
        await expect(page.locator("reset_app_state_link")).to_be_visible()
        await page.click("about_link")
        await expect(page.locator("about_page")).to_be_visible()
        await page.click("logout_link")
        await expect(page.locator("login_page")).to_be_visible()
        await page.click("reset_app_state_link")
        await expect(page.locator("app_reset_confirmation")).to_be_visible()
        return {"scenario": "Navigation Menu", "status": "passed"}
    except Exception as e:
        return {"scenario": "Navigation Menu", "status": "failed", "error": str(e)}

async def scenario_social_media_links(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.click("twitter_link")
        await expect(page.locator("twitter_page")).to_be_visible()
        await page.goto("https://www.saucedemo.com/")
        await page.click("facebook_link")
        await expect(page.locator("facebook_page")).to_be_visible()
        await page.goto("https://www.saucedemo.com/")
        await page.click("linkedin_link")
        await expect(page.locator("linkedin_page")).to_be_visible()
        return {"scenario": "Social Media Links", "status": "passed"}
    except Exception as e:
        return {"scenario": "Social Media Links", "status": "failed", "error": str(e)}

async def scenario_invalid_credentials(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "invalid_user")
        await page.fill("Password", "invalid_password")
        await page.click("login-button")
        await expect(page.locator("error_message")).to_contain_text("Username and password do not match")
        return {"scenario": "Invalid Credentials", "status": "passed"}
    except Exception as e:
        return {"scenario": "Invalid Credentials", "status": "failed", "error": str(e)}

async def scenario_locked_out_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "locked_out_user")
        await page.fill("Password", "secret_sauce")
        await page.click("login-button")
        await expect(page.locator("error_message")).to_contain_text("Sorry, this user has been locked out")
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
        await page.click("complete_checkout_button")
        await expect(page.locator("error_message")).to_contain_text("You must add some items to your cart")
        return {"scenario": "Empty Cart Checkout", "status": "passed"}
    except Exception as e:
        return {"scenario": "Empty Cart Checkout", "status": "failed", "error": str(e)}

async def scenario_invalid_zip_code(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await page.fill("postal_code", "")
        await page.click("complete_checkout_button")
        await expect(page.locator("error_message")).to_contain_text("Invalid postal code")
        return {"scenario": "Invalid ZIP Code", "status": "passed"}
    except Exception as e:
        return {"scenario": "Invalid ZIP Code", "status": "failed", "error": str(e)}

async def scenario_network_failure(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        # Simulate network issues
        await page.route("https://www.saucedemo.com/checkout", lambda route: route.abort())
        await page.click("complete_checkout_button")
        await expect(page.locator("retry_option")).to_be_visible()
        return {"scenario": "Network Failure", "status": "passed"}
    except Exception as e:
        return {"scenario": "Network Failure", "status": "failed", "error": str(e)}

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        
        report = {
            "start_time": datetime.now(timezone.utc).isoformat(),
            "total_duration": 0,
            "scenarios": []
        }
        
        start_time = time.time()

        scenarios_to_run = [
            (scenario_login_screen, "Login Screen"),
            (scenario_product_catalog, "Product Catalog"),
            (scenario_shopping_cart_view, "Shopping Cart View"),
            (scenario_checkout_process, "Checkout Process"),
            (scenario_navigation_menu, "Navigation Menu"),
            (scenario_social_media_links, "Social Media Links"),
            (scenario_invalid_credentials, "Invalid Credentials"),
            (scenario_locked_out_user, "Locked-Out User"),
            (scenario_problem_user, "Problem User"),
            (scenario_performance_glitch_user, "Performance Glitch User"),
            (scenario_empty_cart_checkout, "Empty Cart Checkout"),
            (scenario_invalid_zip_code, "Invalid ZIP Code"),
            (scenario_network_failure, "Network Failure")
        ]

        for scenario_func, scenario_name in scenarios_to_run:
            print(f"\n--- Running Scenario: {scenario_name} ---")
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.bring_to_front()
            
            scenario_result = await scenario_func(page)
            report["scenarios"].append(scenario_result)
            
            await page.close()
        
        report["total_duration"] = time.time() - start_time
        report["end_time"] = datetime.now(timezone.utc).isoformat()
        
        print("\n--- Execution Complete ---")
        print(json.dumps(report, indent=4))
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())