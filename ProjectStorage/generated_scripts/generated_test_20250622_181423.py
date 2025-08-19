import asyncio
import json
import time
from datetime import datetime, timezone
from playwright.async_api import async_playwright, expect

async def scenario_login_with_standard_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "standard_user")
        await page.fill("Password", "secret_sauce")
        await page.click("Login")
        return {"scenario": "Login with standard user", "status": "passed"}
    except Exception as e:
        return {"scenario": "Login with standard user", "status": "failed", "error": str(e)}

async def scenario_login_with_locked_out_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "locked_out_user")
        await page.fill("Password", "secret_sauce")
        await page.click("Login")
        await expect(page.locator("text=Sorry, this user has been locked out")).to_be_visible()
        return {"scenario": "Login with locked-out user", "status": "passed"}
    except Exception as e:
        return {"scenario": "Login with locked-out user", "status": "failed", "error": str(e)}

async def scenario_browse_products(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("All Items")
        await expect(page.locator("css=[data-test='product_list']")).to_be_visible()
        return {"scenario": "Browse products", "status": "passed"}
    except Exception as e:
        return {"scenario": "Browse products", "status": "failed", "error": str(e)}

async def scenario_sort_products_by_name(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.select_option("css=[data-test='product_sort_container'] select", "Name (A-Z)")
        await expect(page.locator("css=[data-test='product_list']")).to_be_visible()
        return {"scenario": "Sort products by name", "status": "passed"}
    except Exception as e:
        return {"scenario": "Sort products by name", "status": "failed", "error": str(e)}

async def scenario_sort_products_by_price(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.select_option("css=[data-test='product_sort_container'] select", "Price (Low to High)")
        await expect(page.locator("css=[data-test='product_list']")).to_be_visible()
        return {"scenario": "Sort products by price", "status": "passed"}
    except Exception as e:
        return {"scenario": "Sort products by price", "status": "failed", "error": str(e)}

async def scenario_add_product_to_cart(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("Add to Cart")
        await expect(page.locator("css=[data-test='cart_badge']")).to_be_visible()
        return {"scenario": "Add product to cart", "status": "passed"}
    except Exception as e:
        return {"scenario": "Add product to cart", "status": "failed", "error": str(e)}

async def scenario_view_cart(page):
    try:
        await page.goto("https://www.saucedemo.com/cart.html")
        await expect(page.locator("css=[data-test='cart_list']")).to_be_visible()
        return {"scenario": "View cart", "status": "passed"}
    except Exception as e:
        return {"scenario": "View cart", "status": "failed", "error": str(e)}

async def scenario_remove_product_from_cart(page):
    try:
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.click("Remove")
        await expect(page.locator("css=[data-test='cart_list']")).not_to_be_visible()
        return {"scenario": "Remove product from cart", "status": "passed"}
    except Exception as e:
        return {"scenario": "Remove product from cart", "status": "failed", "error": str(e)}

async def scenario_proceed_to_checkout(page):
    try:
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.click("Proceed to Checkout")
        await expect(page.locator("css=[data-test='checkout_info']")).to_be_visible()
        return {"scenario": "Proceed to checkout", "status": "passed"}
    except Exception as e:
        return {"scenario": "Proceed to checkout", "status": "failed", "error": str(e)}

async def scenario_fill_out_checkout_information(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await page.fill("First Name", "John")
        await page.fill("Last Name", "Doe")
        await page.fill("Postal Code", "12345")
        await expect(page.locator("css=[data-test='order_summary']")).to_be_visible()
        return {"scenario": "Fill out checkout information", "status": "passed"}
    except Exception as e:
        return {"scenario": "Fill out checkout information", "status": "failed", "error": str(e)}

async def scenario_review_order_summary(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-two.html")
        await expect(page.locator("css=[data-test='order_summary']")).to_be_visible()
        return {"scenario": "Review order summary", "status": "passed"}
    except Exception as e:
        return {"scenario": "Review order summary", "status": "failed", "error": str(e)}

async def scenario_submit_order(page):
    try:
        await page.goto("https://www.saucedemo.com/checkout-step-two.html")
        await page.click("Submit Order")
        await expect(page.locator("css=[data-test='order_confirmation']")).to_be_visible()
        return {"scenario": "Submit order", "status": "passed"}
    except Exception as e:
        return {"scenario": "Submit order", "status": "failed", "error": str(e)}

async def scenario_navigate_to_about_page(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("About")
        await expect(page.locator("css=[data-test='about_page']")).to_be_visible()
        return {"scenario": "Navigate to About page", "status": "passed"}
    except Exception as e:
        return {"scenario": "Navigate to About page", "status": "failed", "error": str(e)}

async def scenario_log_out(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("Logout")
        await expect(page.locator("css=[data-test='login_page']")).to_be_visible()
        return {"scenario": "Log out", "status": "passed"}
    except Exception as e:
        return {"scenario": "Log out", "status": "failed", "error": str(e)}

async def scenario_reset_app_state(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("Reset App State")
        await expect(page.locator("css=[data-test='login_page']")).to_be_visible()
        return {"scenario": "Reset app state", "status": "passed"}
    except Exception as e:
        return {"scenario": "Reset app state", "status": "failed", "error": str(e)}

async def scenario_interact_with_social_links(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("Twitter")
        await expect(page.locator("css=[data-test='twitter_page']")).to_be_visible()
        return {"scenario": "Interact with social links", "status": "passed"}
    except Exception as e:
        return {"scenario": "Interact with social links", "status": "failed", "error": str(e)}

async def scenario_invalid_credentials(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "invalid_user")
        await page.fill("Password", "invalid_password")
        await page.click("Login")
        await expect(page.locator("text=Username and password do not match")).to_be_visible()
        return {"scenario": "Invalid credentials", "status": "passed"}
    except Exception as e:
        return {"scenario": "Invalid credentials", "status": "failed", "error": str(e)}

async def scenario_locked_out_user(page):
    try:
        await page.goto("https://www.saucedemo.com/")
        await page.fill("Username", "locked_out_user")
        await page.fill("Password", "secret_sauce")
        await page.click("Login")
        await expect(page.locator("text=Sorry, this user has been locked out")).to_be_visible()
        return {"scenario": "Locked-out user", "status": "passed"}
    except Exception as e:
        return {"scenario": "Locked-out user", "status": "failed", "error": str(e)}

async def scenario_problem_user(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("All Items")
        await expect(page.locator("css=[data-test='product_list']")).to_be_visible()
        return {"scenario": "Problem user", "status": "passed"}
    except Exception as e:
        return {"scenario": "Problem user", "status": "failed", "error": str(e)}

async def scenario_performance_glitch_user(page):
    try:
        await page.goto("https://www.saucedemo.com/inventory.html")
        await page.click("All Items")
        await expect(page.locator("css=[data-test='product_list']")).to_be_visible()
        return {"scenario": "Performance glitch user", "status": "passed"}
    except Exception as e:
        return {"scenario": "Performance glitch user", "status": "failed", "error": str(e)}

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

        report["scenarios"].append(await scenario_login_with_standard_user(page))
        report["scenarios"].append(await scenario_login_with_locked_out_user(page))
        report["scenarios"].append(await scenario_browse_products(page))
        report["scenarios"].append(await scenario_sort_products_by_name(page))
        report["scenarios"].append(await scenario_sort_products_by_price(page))
        report["scenarios"].append(await scenario_add_product_to_cart(page))
        report["scenarios"].append(await scenario_view_cart(page))
        report["scenarios"].append(await scenario_remove_product_from_cart(page))
        report["scenarios"].append(await scenario_proceed_to_checkout(page))
        report["scenarios"].append(await scenario_fill_out_checkout_information(page))
        report["scenarios"].append(await scenario_review_order_summary(page))
        report["scenarios"].append(await scenario_submit_order(page))
        report["scenarios"].append(await scenario_navigate_to_about_page(page))
        report["scenarios"].append(await scenario_log_out(page))
        report["scenarios"].append(await scenario_reset_app_state(page))
        report["scenarios"].append(await scenario_interact_with_social_links(page))
        report["scenarios"].append(await scenario_invalid_credentials(page))
        report["scenarios"].append(await scenario_locked_out_user(page))
        report["scenarios"].append(await scenario_problem_user(page))
        report["scenarios"].append(await scenario_performance_glitch_user(page))

        report["total_duration"] = time.time() - start_time
        report["end_time"] = datetime.now(timezone.utc).isoformat()
        
        print(json.dumps(report, indent=4))
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())