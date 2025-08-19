import asyncio
import json
import time
from datetime import datetime, timezone
from playwright.async_api import async_playwright, expect

async def scenario_successful_order_placement(page):
    try:
        await page.goto("https://example.com/login")
        await page.wait_for_load_state('networkidle')
        await page.fill("input[name='username']", "username")
        await page.fill("input[name='password']", "password")
        await page.click("text=Login")
        await page.wait_for_load_state('networkidle')
        await page.click("text=Veg")
        await page.wait_for_load_state('networkidle')
        await page.click("text=Potato")
        await page.fill("input[name='quantity']", "10")
        await page.click("text=Add to Cart")
        await page.wait_for_load_state('networkidle')
        await page.click("text=View Cart")
        await page.wait_for_load_state('networkidle')
        await page.click("text=Proceed to Checkout")
        await page.wait_for_load_state('networkidle')
        await page.fill("input[name='first_name']", "Pavan")
        await page.fill("input[name='last_name']", "Kumar")
        await page.fill("input[name='delivery_address']", "Test Address")
        await page.fill("input[name='landmark']", "Test Landmark")
        await page.fill("input[name='city']", "Noida")
        await page.fill("input[name='zip_code']", "201301")
        await page.fill("input[name='phone_number']", "9876543210")
        await page.fill("input[name='email_address']", "test@gmail.com")
        await page.fill("input[name='delivery_slot']", "Test Slot")
        await page.click("text=Place Order")
        await page.wait_for_load_state('networkidle')
        confirmation_text = await page.text_content("text=Order placed successfully")
        if confirmation_text:
            return {"scenario": "Successful Order Placement", "status": "passed"}
        else:
            return {"scenario": "Successful Order Placement", "status": "failed"}
    except Exception as e:
        return {"scenario": "Successful Order Placement", "status": "failed", "error": str(e)}

async def scenario_leaving_required_fields_empty(page):
    try:
        await page.goto("https://example.com/billing-and-shipping")
        await page.wait_for_load_state('networkidle')
        await page.click("text=Place Order")
        await page.wait_for_load_state('networkidle')
        validation_messages = await page.text_content("text=Please fill in this field")
        if validation_messages:
            return {"scenario": "Leaving Required Fields Empty", "status": "passed"}
        else:
            return {"scenario": "Leaving Required Fields Empty", "status": "failed"}
    except Exception as e:
        return {"scenario": "Leaving Required Fields Empty", "status": "failed", "error": str(e)}

async def scenario_entering_invalid_email_or_phone(page):
    try:
        await page.goto("https://example.com/billing-and-shipping")
        await page.wait_for_load_state('networkidle')
        await page.fill("input[name='email_address']", "invalid_email")
        await page.fill("input[name='phone_number']", "invalid_phone")
        await page.click("text=Place Order")
        await page.wait_for_load_state('networkidle')
        error_messages = await page.text_content("text=Invalid email or phone number")
        if error_messages:
            return {"scenario": "Entering Invalid Email or Phone", "status": "passed"}
        else:
            return {"scenario": "Entering Invalid Email or Phone", "status": "failed"}
    except Exception as e:
        return {"scenario": "Entering Invalid Email or Phone", "status": "failed", "error": str(e)}

async def scenario_placing_order_with_zero_quantity(page):
    try:
        await page.goto("https://example.com/cart")
        await page.wait_for_load_state('networkidle')
        await page.fill("input[name='quantity']", "0")
        await page.click("text=Proceed to Checkout")
        await page.wait_for_load_state('networkidle')
        error_message = await page.text_content("text=Quantity cannot be zero")
        if error_message:
            return {"scenario": "Placing Order with Zero Quantity", "status": "passed"}
        else:
            return {"scenario": "Placing Order with Zero Quantity", "status": "failed"}
    except Exception as e:
        return {"scenario": "Placing Order with Zero Quantity", "status": "failed", "error": str(e)}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=False)
        
        report = {
            "start_time": datetime.now(timezone.utc).isoformat(),
            "total_duration": 0,
            "scenarios": []
        }
        
        start_time = time.time()

        scenarios_to_run = [
            (scenario_successful_order_placement, "Successful Order Placement"),
            (scenario_leaving_required_fields_empty, "Leaving Required Fields Empty"),
            (scenario_entering_invalid_email_or_phone, "Entering Invalid Email or Phone"),
            (scenario_placing_order_with_zero_quantity, "Placing Order with Zero Quantity")
        ]

        for scenario_func, scenario_name in scenarios_to_run:
            print(f"\n--- Running Scenario: {scenario_name} ---")
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.bring_to_front()
            
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