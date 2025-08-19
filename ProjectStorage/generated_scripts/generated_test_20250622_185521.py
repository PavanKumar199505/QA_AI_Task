import asyncio
import json
import time
from datetime import datetime, timezone
from playwright.async_api import async_playwright, expect

async def login(page, username, password):
    await page.goto("https://www.saucedemo.com/")
    await page.wait_for_load_state('networkidle')
    await page.locator("#user-name").fill(username)
    await page.locator("#password").fill(password)
    await page.locator("#login-button").click()
    await page.wait_for_load_state('networkidle')

async def scenario_successful_login(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        expect(page.locator("div.inventory_list")).to_be_visible()
        return {"scenario": "Successful Login", "status": "passed"}
    except Exception as e:
        return {"scenario": "Successful Login", "status": "failed", "error": str(e)}

async def scenario_login_with_invalid_credentials(page):
    try:
        await login(page, "invalid_user", "invalid_password")
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        return {"scenario": "Login with Invalid Credentials", "status": "passed"}
    except Exception as e:
        return {"scenario": "Login with Invalid Credentials", "status": "failed", "error": str(e)}

async def scenario_login_with_locked_out_user(page):
    try:
        await login(page, "locked_out_user", "secret_sauce")
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        return {"scenario": "Login with Locked-Out User", "status": "passed"}
    except Exception as e:
        return {"scenario": "Login with Locked-Out User", "status": "failed", "error": str(e)}

async def scenario_product_catalog(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        expect(page.locator("div.inventory_list")).to_be_visible()
        return {"scenario": "Product Catalog", "status": "passed"}
    except Exception as e:
        return {"scenario": "Product Catalog", "status": "failed", "error": str(e)}

async def scenario_add_item_to_cart(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        await page.locator("button.inventory_item_button").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("span.shopping_cart_badge")).to_be_visible()
        return {"scenario": "Add Item to Cart", "status": "passed"}
    except Exception as e:
        return {"scenario": "Add Item to Cart", "status": "failed", "error": str(e)}

async def scenario_remove_item_from_cart(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        await page.locator("button.inventory_item_button").click()
        await page.wait_for_load_state('networkidle')
        await page.locator("button.remove_button").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("span.shopping_cart_badge")).to_be_visible()
        return {"scenario": "Remove Item from Cart", "status": "passed"}
    except Exception as e:
        return {"scenario": "Remove Item from Cart", "status": "failed", "error": str(e)}

async def scenario_checkout_with_empty_cart(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        await page.locator("button.checkout_button").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        return {"scenario": "Checkout with Empty Cart", "status": "passed"}
    except Exception as e:
        return {"scenario": "Checkout with Empty Cart", "status": "failed", "error": str(e)}

async def scenario_checkout_with_valid_item(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        await page.locator("button.inventory_item_button").click()
        await page.wait_for_load_state('networkidle')
        await page.locator("button.checkout_button").click()
        await page.wait_for_load_state('networkidle')
        await page.locator("#first-name").fill("first name")
        await page.locator("#last-name").fill("last name")
        await page.locator("#postal-code").fill("12345")
        await page.locator("input.checkout_button").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("h2[data-test='complete-header']")).to_be_visible()
        return {"scenario": "Checkout with Valid Item", "status": "passed"}
    except Exception as e:
        return {"scenario": "Checkout with Valid Item", "status": "failed", "error": str(e)}

async def scenario_checkout_with_invalid_zip_code(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        await page.locator("button.inventory_item_button").click()
        await page.wait_for_load_state('networkidle')
        await page.locator("button.checkout_button").click()
        await page.wait_for_load_state('networkidle')
        await page.locator("#first-name").fill("first name")
        await page.locator("#last-name").fill("last name")
        await page.locator("#postal-code").fill("invalid")
        await page.locator("input.checkout_button").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        return {"scenario": "Checkout with Invalid ZIP Code", "status": "passed"}
    except Exception as e:
        return {"scenario": "Checkout with Invalid ZIP Code", "status": "failed", "error": str(e)}

async def scenario_navigation(page):
    try:
        await login(page, "standard_user", "secret_sauce")
        await page.locator("button.burger_menu_button").click()
        await page.wait_for_load_state('networkidle')
        await page.locator("a#logout_sidebar_link").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("button.login_button")).to_be_visible()
        return {"scenario": "Navigation", "status": "passed"}
    except Exception as e:
        return {"scenario": "Navigation", "status": "failed", "error": str(e)}

async def scenario_social_links(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.wait_for_load_state('networkidle')
        await page.locator("a.twitter").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("title=Twitter")).to_be_visible()
        await page.goto("https://www.saucedemo.com/")
        await page.wait_for_load_state('networkidle')
        await page.locator("a.facebook").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("title=Facebook")).to_be_visible()
        await page.goto("https://www.saucedemo.com/")
        await page.wait_for_load_state('networkidle')
        await page.locator("a.linkedin").click()
        await page.wait_for_load_state('networkidle')
        expect(page.locator("title=LinkedIn")).to_be_visible()
        return {"scenario": "Social Links", "status": "passed"}
    except Exception as e:
        return {"scenario": "Social Links", "status": "failed", "error": str(e)}

async def main():
    async with async_playwright() as p:
        browser = await p.edge.launch(headless=False)
        
        report = {
            "start_time": datetime.now(timezone.utc).isoformat(),
            "total_duration": 0,
            "scenarios": []
        }
        
        start_time = time.time()

        scenarios_to_run = [
            (scenario_successful_login, "Successful Login"),
            (scenario_login_with_invalid_credentials, "Login with Invalid Credentials"),
            (scenario_login_with_locked_out_user, "Login with Locked-Out User"),
            (scenario_product_catalog, "Product Catalog"),
            (scenario_add_item_to_cart, "Add Item to Cart"),
            (scenario_remove_item_from_cart, "Remove Item from Cart"),
            (scenario_checkout_with_empty_cart, "Checkout with Empty Cart"),
            (scenario_checkout_with_valid_item, "Checkout with Valid Item"),
            (scenario_checkout_with_invalid_zip_code, "Checkout with Invalid ZIP Code"),
            (scenario_navigation, "Navigation"),
            (scenario_social_links, "Social Links")
        ]

        for scenario_func, scenario_name in scenarios_to_run:
            print(f"\n--- Running Scenario: {scenario_name} ---")
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.bring_to_front()
            await page.wait_for_load_state('networkidle')
            
            scenario_result = await scenario_func(page)
            report["scenarios"].append(scenario_result)
            
            await page.close()
        # -------------------------

        report["total_duration"] = time.time() - start_time
        report["end_time"] = datetime.now(timezone.utc).isoformat()
        
        print("\n--- Execution Complete ---")
        print(json.dumps(report, indent=4))
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())