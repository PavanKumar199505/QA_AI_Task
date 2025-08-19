import playwright
import json
import time

browser = playwright.firefox.launch(headless=False)
context = browser.new_context()
page = context.new_page()

def login(username, password):
    page.goto("https://www.saucedemo.com/")
    page.fill("input[name='user-name']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")

def product_catalog():
    page.goto("https://www.saucedemo.com/inventory.html")
    assert page.locator("text='Products'").is_visible()
    assert page.locator("text='Add to Cart'").is_visible()
    assert page.locator("text='Product name'").is_visible()
    assert page.locator("text='Product description'").is_visible()
    assert page.locator("text='Product price'").is_visible()
    assert page.locator("text='Product image'").is_visible()

def shopping_cart_view():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/cart.html")
    assert page.locator("text='Shopping cart'").is_visible()
    assert page.locator("text='Remove'").is_visible()
    assert page.locator("text='Continue shopping'").is_visible()
    assert page.locator("text='Proceed to checkout'").is_visible()
    assert page.locator("text='1 item'").is_visible()

def checkout_process():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/checkout-step-one.html")
    assert page.locator("text='First name'").is_visible()
    assert page.locator("text='Last name'").is_visible()
    assert page.locator("text='Postal code'").is_visible()
    assert page.locator("text='Order overview'").is_visible()
    assert page.locator("text='Order total'").is_visible()

def navigation_menu():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/")
    assert page.locator("text='All items'").is_visible()
    assert page.locator("text='About'").is_visible()
    assert page.locator("text='Logout'").is_visible()
    assert page.locator("text='Reset app state'").is_visible()

def social_media_links():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/")
    page.click("text='Facebook'")
    page.wait_for_url("https://www.facebook.com/")
    page.click("text='Twitter'")
    page.wait_for_url("https://www.twitter.com/")

def invalid_credentials():
    login("invalid_user", "invalid_password")
    assert page.locator("text='Username and password do not match'").is_visible()

def locked_out_user():
    login("locked_out_user", "secret_sauce")
    assert page.locator("text='Sorry, this user has been locked out'").is_visible()

def problem_user():
    login("problem_user", "secret_sauce")
    assert page.locator("text='Broken images or incorrect product data'").is_visible()

def performance_glitch_user():
    login("performance_glitch_user", "secret_sauce")
    time.sleep(5)
    assert page.locator("text='Product catalog'").is_visible()

def empty_cart_checkout():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/cart.html")
    page.click("button[type='submit']")
    assert page.locator("text='Your cart is empty'").is_visible()

def invalid_zip_code():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/checkout-step-one.html")
    page.fill("input[name='postal-code']", "12345")
    page.click("button[type='submit']")
    assert page.locator("text='Error: Postal code is invalid'").is_visible()

def network_failure():
    login("standard_user", "secret_sauce")
    page.goto("https://www.saucedemo.com/checkout-step-one.html")
    page.set_request_interceptor(lambda request: request.abort())
    page.click("button[type='submit']")
    assert page.locator("text='Error: Network failure'").is_visible()

def run_scenarios():
    scenarios = [
        {"name": "Login Screen", "function": login, "args": ["standard_user", "secret_sauce"]},
        {"name": "Product Catalog", "function": product_catalog},
        {"name": "Shopping Cart View", "function": shopping_cart_view},
        {"name": "Checkout Process", "function": checkout_process},
        {"name": "Navigation Menu", "function": navigation_menu},
        {"name": "Social Media Links", "function": social_media_links},
        {"name": "Edge Cases - Invalid Credentials", "function": invalid_credentials},
        {"name": "Edge Cases - Locked-Out User", "function": locked_out_user},
        {"name": "Edge Cases - Problem User", "function": problem_user},
        {"name": "Edge Cases - Performance Glitch User", "function": performance_glitch_user},
        {"name": "Edge Cases - Empty Cart Checkout", "function": empty_cart_checkout},
        {"name": "Edge Cases - Invalid ZIP Code", "function": invalid_zip_code},
        {"name": "Edge Cases - Network Failure", "function": network_failure},
    ]
    results = []
    for scenario in scenarios:
        try:
            scenario["function"](*scenario["args"])
            results.append({"name": scenario["name"], "status": "passed"})
        except Exception as e:
            results.append({"name": scenario["name"], "status": "failed", "error": str(e)})
    print(json.dumps({"status": "passed" if all(result["status"] == "passed" for result in results) else "failed", "duration": time.time(), "scenarios": results}))
    browser.close()

run_scenarios()