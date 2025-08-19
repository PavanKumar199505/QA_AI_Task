
You are a senior QA automation engineer. Convert this Gherkin feature file into a structured, reportable Python test script using Playwright.

Gherkin Content:
Feature: SauceDemo Functional Requirements
Scenario: Login Screen
Given the user is on the login page
When the user fills in the "Username" field with "standard_user"
And the user fills in the "Password" field with "secret_sauce"
Then the user should see the product catalog on the page
And the user should be logged in successfully

Scenario: Product Catalog
Given the user is logged in
When the user is on the product catalog page
Then the user should see a list of products with names, descriptions, prices, and images
And the user should see "Add to Cart" buttons for each product
And the user should see sorting options by name (A-Z, Z-A) and price (low to high, high to low)

Scenario: Shopping Cart View
Given the user is logged in
When the user adds a product to the cart
Then the user should see the product in the cart view
And the user should see options to remove items, continue shopping, or proceed to checkout
And the user should see a badge showing the item count

Scenario: Checkout Process
Given the user is logged in
When the user proceeds to checkout
Then the user should see the customer information form
And the user should see the order overview summarizing items, prices, and total
And the user should see a confirmation screen displaying a success message
And the user should be logged out after completing the checkout

Scenario: Navigation Menu
Given the user is logged in
When the user navigates to the navigation menu
Then the user should see links for "All Items", "About", "Logout", and "Reset App State"
And the user should be able to access the About page
And the user should be able to log out
And the user should be able to reset the application state

Scenario: Social Media Links
Given the user is logged in
When the user clicks on the social media links
Then the user should be redirected to the corresponding social media page
And the user should be able to interact with the social media links

Scenario: Edge Cases
Given the user is on the login page
When the user fills in the "Username" field with "locked_out_user"
And the user fills in the "Password" field with "secret_sauce"
Then the user should see a locked-out error message
And the user should be denied access

Given the user is on the login page
When the user fills in the "Username" field with "problem_user"
And the user fills in the "Password" field with "secret_sauce"
Then the user should experience UI or functional issues
And the user should be able to interact with the affected UI elements

Given the user is on the login page
When the user fills in the "Username" field with "performance_glitch_user"
And the user fills in the "Password" field with "secret_sauce"
Then the user should experience slow response times
And the user should be able to interact with the UI elements after the delay

**CRITICAL REQUIREMENTS:**

1. **Structured Test Framework**: Create a test script with:
   - Individual functions for each scenario
   - A main test runner that executes all scenarios
   - Comprehensive reporting for each scenario

2. **Browser Setup**: Use `browser = await p.firefox.launch(headless=False)` to ensure the browser is visible during testing.

3. **Selector Strategy**: Use Playwright's built-in locators for maximum reliability:
   - If a Gherkin step mentions an element name with a **hyphen** (e.g., "user-name" or "login-button"), it is a **CSS ID**. You MUST use the `page.locator("#...")` selector.
   - Example: `When the user clicks the "login-button"` becomes `await page.locator("#login-button").click()`.
   - For other elements, use: `page.get_by_role()`, `page.get_by_text()`, `page.get_by_placeholder()`, etc.

4. **Scenario Structure**: Each scenario should be a separate async function with:
   - Clear scenario name as function name
   - Try-catch blocks for error handling
   - Return True for pass, False for fail
   - Detailed logging of steps

5. **Reporting**: Include comprehensive reporting that tracks:
   - Scenario name
   - Step-by-step execution
   - Pass/fail status
   - Error messages if any
   - Execution time

6. **Complete Script**: The output MUST be a single, runnable Python file with:
   - All necessary imports: `asyncio`, `re`, `sys`, `time`, `json`, `datetime` and `from playwright.async_api import async_playwright, expect`
   - Use the modern `asyncio.run(main())` pattern
   - A main function that runs all scenarios and generates a detailed report

7. **No Explanations**: Do NOT include any comments, markdown, or text other than the Python code itself. Your entire response must be only code.

Generate the complete automation script now:
