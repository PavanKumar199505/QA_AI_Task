import logging
import os
import re
from typing import List
from groq import Groq
from logic.util import get_project_root

logger = logging.getLogger(__name__)


def get_groq_client():
    """Initialize Groq client with API key from environment or secrets."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        secrets_path = get_project_root() / ".streamlit" / "secrets.toml"
        if secrets_path.exists():
            with open(secrets_path, "r") as f:
                import toml
                secrets = toml.load(f)
                api_key = secrets.get("GROQ_API_KEY")
    if api_key:
        return Groq(api_key=api_key)
    return None


def summarize_text(text: str) -> str:
    """
    Summarize the input text using Groq LLM.

    Args:
        text: Text to summarize.

    Returns:
        Summary as a string, or error message if LLM is unavailable.
    """
    client = get_groq_client()
    if not client:
        logger.warning("No Groq API key provided; summarization skipped.")
        return "Summarization unavailable: Please configure a Groq API key."

    try:
        prompt = f"Summarize the following text for key points and relevant details:\n{text}\n"
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip()
        logger.info("Text summarized successfully")
        return summary
    except Exception as e:
        logger.error(f"LLM summarization error: {str(e)}", exc_info=True)
        return f"Summarization failed: {str(e)}"


def generate_test_cases(text_content: str) -> str:
    """Generate comprehensive, BDD-style Gherkin test cases from text."""
    
    system_prompt = """
You are a senior QA automation engineer specializing in Behavior-Driven Development (BDD). Your task is to analyze the provided application description and create a comprehensive Gherkin feature file for it.

**CRITICAL REQUIREMENTS:**

1.  **Full Coverage:** Generate `Scenario` blocks covering the primary features and potential edge cases described in the text.
2.  **Atomic Steps:** Each `Given`, `When`, `Then` step must describe a single, clear user action or verification.
3.  **Reference UI Elements:** When referring to buttons, input fields, or links, use double quotes to name the element (e.g., `"Login" button`). This is essential for automation.
4.  **Preconditions:** Use the `Given` step to establish the initial state (e.g., `Given the user is on the login page`).
5.  **Gherkin Format:** The final output must be a single, valid Gherkin `Feature` block. You MUST place a blank line between each `Scenario` block for readability. Do not include any other text, comments, or explanations.
"""

    user_prompt = f"""
Please generate a Gherkin feature file based on the following application description. Ensure the output is a single block of Gherkin text, with blank lines between scenarios.

Application Description:
---
{text_content}
---
"""

    client = get_groq_client()
    if not client:
        return "Error: Groq API key not configured."

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=4096,
            temperature=0.0,
        )
        gherkin_text = response.choices[0].message.content.strip()
        logger.info("Comprehensive Gherkin test cases generated successfully.")
        return gherkin_text
    except Exception as e:
        logger.error(f"Gherkin generation failed: {str(e)}", exc_info=True)
        return f"Error: Failed to generate test cases. Details: {str(e)}"


def generate_automation_script(gherkin_content: str) -> str:
    """Generate a structured, BDD-style automation script from Gherkin."""
    
    system_prompt = """
You are a senior QA automation engineer specializing in BDD. Your task is to convert a Gherkin feature file into a single, runnable Python test script using Playwright, following a strict template.

**CRITICAL REQUIREMENTS:**

1.  **Template Adherence**: Your output MUST follow the exact Python structure provided below. You will fill in the sections marked "<<<...>>>".

    ```python
    import asyncio
    import json
    import time
    from datetime import datetime, timezone
    from playwright.async_api import async_playwright, expect

    # <<< ALL SCENARIO FUNCTIONS WILL BE GENERATED HERE >>>
    # Each Gherkin Scenario must be a separate async Python function.

    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel="msedge", headless=False)
            
            report = {
                "start_time": datetime.now(timezone.utc).isoformat(),
                "total_duration": 0,
                "scenarios": []
            }
            
            start_time = time.time()

            # --- Execute Scenarios ---
            scenarios_to_run = [
                # <<< A TUPLE FOR EACH SCENARIO: (function_name, "Scenario Name from Gherkin") >>>
            ]

            for scenario_func, scenario_name in scenarios_to_run:
                print(f"\\n--- Running Scenario: {scenario_name} ---")
                page = await browser.new_page()
                await page.set_viewport_size({"width": 1920, "height": 1080})
                await page.bring_to_front()
                
                scenario_result = await scenario_func(page)
                report["scenarios"].append(scenario_result)
                
                await page.close()
            # -------------------------

            report["total_duration"] = time.time() - start_time
            report["end_time"] = datetime.now(timezone.utc).isoformat()
            
            print("\\n--- Execution Complete ---")
            print(json.dumps(report, indent=4))
            
            await browser.close()

    if __name__ == "__main__":
        asyncio.run(main())
    ```

2.  **Scenario Functions**: For each `Scenario` in the Gherkin, create a corresponding `async def` function.
    *   The function name must be derived from the scenario name (e.g., `async def scenario_successful_login(...)`).
    *   Each function must accept `page` as an argument and contain the Playwright code to execute the Gherkin steps.
    *   Use `try/except` to catch errors and return a report dictionary.

3.  **Selector Strategy**:
    *   If a Gherkin step mentions an element with a **hyphen** in its quoted name (e.g., "login-button"), it is a **CSS ID**. You MUST use the `page.locator("#...")` selector.
    *   Otherwise, use semantic locators like `page.get_by_role()`, `page.get_by_text()`, etc.

4.  **Code Only**: Your entire response MUST be only the raw Python code. Do NOT include any explanations or markdown.
"""

    user_prompt = f"""
Please convert the following Gherkin content into a complete Python Playwright script, strictly following the template and rules defined in your system prompt. For any navigation action (`page.goto` or a `click` that changes page), you MUST add `await page.wait_for_load_state('networkidle')` immediately after.

Gherkin Content:
{gherkin_content}
"""
    client = get_groq_client()
    if not client:
        logger.warning("No Groq API key provided; script generation skipped.")
        return "# Groq API key not configured. Cannot generate script."

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192", # Using a more powerful model for this complex task
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4096,
            temperature=0.0,
        )
        
        script_text = response.choices[0].message.content.strip()
        
        if script_text.startswith("```python"):
            script_text = script_text[9:].strip()
        
        if script_text.endswith("```"):
            script_text = script_text[:-3].strip()

        # Find the start of the actual code block
        if "import" in script_text:
            script_text = script_text[script_text.find("import"):]

        logger.info("Generated BDD-style automation script.")
        return script_text
        
    except Exception as e:
        logger.error(f"Automation script generation error: {str(e)}", exc_info=True)
        return f"# Error generating script: {str(e)}"
