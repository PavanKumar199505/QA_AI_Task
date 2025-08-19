import streamlit as st
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import json
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from logic.extraction import extract_text_from_file
from logic.llm import summarize_text, generate_test_cases, generate_automation_script
from logic.reporting import generate_pdf_report, generate_txt_report, generate_json_report
from logic.util import setup_storage, get_project_root, setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize storage directories
setup_storage()

# --- Helper Functions ---
def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.resolve()

def initialize_session_state():
    """Initializes session state variables if they don't exist."""
    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "test_cases" not in st.session_state:
        st.session_state.test_cases = ""
    if "test_results" not in st.session_state:
        st.session_state.test_results = None
    if "automation_script" not in st.session_state:
        st.session_state.automation_script = ""

# --- Main App ---
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Automated QA Assistant", layout="wide")

    # Initialize session state variables
    initialize_session_state()
    
    # --- Sidebar ---
    st.sidebar.title("Navigation")
    
    # Load and display logo
    try:
        logo_path = Path(get_project_root()) / "ui" / "logo.png"
        if logo_path.exists():
            st.sidebar.image(str(logo_path), use_column_width=True)
        else:
            logger.warning(f"Logo not found at {logo_path}")
    except Exception as e:
        logger.error(f"Error loading logo: {e}")

    # Simplified navigation
    page = st.sidebar.radio("Go to", ["File Analysis", "Automated Tests"])

    # Load API key from .env file
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        st.sidebar.warning("GROQ_API_KEY not found in environment variables. Please set it in a .env file.")
    # --- End Sidebar ---

    if page == "File Analysis":
        display_file_analysis()
    elif page == "Automated Tests":
        display_automated_tests()

def display_home():
    """Displays the home page content."""
    st.title("Welcome to the Automated QA Assistant! 👋")
    st.markdown("---")
    st.markdown("""
    This tool is designed to revolutionize your QA workflow by leveraging the power of Large Language Models (LLMs).
    
    ### How It Works:
    1.  **File Analysis:** Upload your requirement documents in any format (PDF, DOCX, TXT, or even audio files). The tool will automatically extract the text content.
    2.  **AI-Powered Insights:** The extracted text is sent to an LLM to generate a concise summary and a comprehensive set of test cases in Gherkin format.
    3.  **Dynamic Test Automation:** With a single click, convert the Gherkin test cases into a fully runnable Playwright automation script.
    4.  **Execute & Review:** Run the generated script directly from the app and review the detailed, scenario-by-scenario results.
    
    Navigate to the **File Analysis** page to get started!
    """)
    st.info("Ensure your Groq API key is set in your environment to enable AI features.")

def display_file_analysis():
    """Handles the file analysis page."""
    st.title("📄 File Analysis & AI Insights")
    st.markdown("Upload a requirements document (PDF, DOCX, TXT, MP3, MP4) to extract text and generate test cases.")
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx", "txt", "mp3", "mp4", "png", "jpg"]
    )

    if uploaded_file:
        # When a new file is uploaded, reset the entire session state related to analysis and tests
        st.session_state.extracted_text = ""
        st.session_state.summary = ""
        st.session_state.test_cases = ""
        st.session_state.automation_script = ""
        st.session_state.test_results = None
        logger.info("New file uploaded. Session state has been reset.")

        # Save uploaded file
        upload_dir = Path(get_project_root()) / "ProjectStorage" / "uploads"
        file_path = upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logger.info(f"Uploaded file saved to {file_path}")

        # Automatically trigger analysis after upload
        with st.spinner("Analyzing file... This may take a moment."):
            try:
                # Extract text
                logger.info(f"Starting analysis for {uploaded_file.name}")
                extracted_text = extract_text_from_file(file_path)
                st.session_state.extracted_text = extracted_text
                
                # Save extracted text
                extracted_dir = Path(get_project_root()) / "ProjectStorage" / "extracted"
                extracted_file = extracted_dir / f"{uploaded_file.name}.txt"
                with open(extracted_file, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                logger.info(f"Extracted text saved to {extracted_file}")

                # Check for API key before calling LLM
                if not os.getenv("GROQ_API_KEY"):
                    st.error("Groq API key not configured. Cannot generate summary and test cases.")
                    st.session_state.summary = "Analysis skipped: API key missing."
                    st.session_state.test_cases = "Analysis skipped: API key missing."
                else:
                    # Generate summary and test cases
                    summary = summarize_text(st.session_state.extracted_text)
                    st.session_state.summary = summary
                    logger.info("Text summarized successfully")

                    test_cases = generate_test_cases(st.session_state.extracted_text)
                    st.session_state.test_cases = test_cases
                    logger.info("Test cases generated successfully.")
            
            except Exception as e:
                st.error(f"Failed during analysis: {str(e)}")
                logger.error(f"Analysis error: {str(e)}", exc_info=True)
                st.session_state.test_results = {"error": str(e)} # Store error for debugging
                return

        st.markdown("---")

        # Display extracted text
        st.subheader("Extracted Text")
        st.text_area("Extracted Content", st.session_state.extracted_text, height=150)

        # Display summary
        st.subheader("AI-Generated Summary")
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
        else:
            st.warning("No summary was generated.")

        # Display test cases
        st.subheader("AI-Generated Test Cases")
        if st.session_state.test_cases:
            st.markdown(f"```gherkin\\n{st.session_state.test_cases}\\n```")
        else:
            st.warning("No test cases were generated.")

def display_automated_tests():
    st.title("🤖 Dynamic Test Automation")
    st.markdown("Generate and run Playwright automation scripts directly from your test cases.")

    # Check if test cases exist
    if not st.session_state.test_cases:
        st.warning("Please analyze a file on the 'File Analysis' page first to generate test cases.")
        return

    st.markdown("### 1. Review Your Gherkin Test Cases")
    st.markdown(f"```gherkin\\n{st.session_state.test_cases}\\n```")
    st.markdown("---")

    st.markdown("### 2. Generate the Automation Script")
    if st.button("✨ Generate Playwright Script", use_container_width=True):
        if not os.getenv("GROQ_API_KEY"):
            st.error("Groq API key not configured. Please add it in the sidebar.")
        else:
            with st.spinner("AI is writing the automation script..."):
                script = generate_automation_script(st.session_state.test_cases)
                st.session_state.automation_script = script

    if st.session_state.automation_script:
        st.markdown("### 3. Review and Execute the Script")
        st.code(st.session_state.automation_script, language="python")

        if st.button("▶️ Execute Automated Script", use_container_width=True):
            with st.spinner("Running the generated script..."):
                try:
                    # Save the generated script to a file
                    scripts_dir = Path(get_project_root()) / "ProjectStorage" / "generated_scripts"
                    scripts_dir.mkdir(exist_ok=True)
                    script_path = scripts_dir / f"generated_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write(st.session_state.automation_script)
                    
                    logger.info(f"Executing generated script: {script_path}")
                    # Run the script via subprocess
                    result = subprocess.run(
                        [sys.executable, str(script_path)], # Use sys.executable to ensure it's the right python
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    logger.info("Generated script executed.")

                    # Store results for display
                    st.session_state.test_results = {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
                except subprocess.TimeoutExpired:
                    st.error("Tests timed out after 5 minutes.")
                    logger.error("Generated script execution timed out")
                except Exception as e:
                    st.error(f"Failed to run the generated script: {str(e)}")
                    logger.error(f"Execution error: {str(e)}", exc_info=True)
    
    # Display test results from the generated script
    if st.session_state.test_results:
        st.markdown("---")
        st.markdown("### 4. Execution Results")
        results = st.session_state.test_results
        
        # Determine status and message
        if results["returncode"] == 0:
            status = "success"
            message = "✅ Script executed successfully!"
        else:
            status = "error"
            message = "❌ Script failed during execution."
            
        if status == "success":
            st.success(message)
        else:
            st.error(message)

        # Parse and display structured results
        stdout = results["stdout"] or ""
        stderr = results["stderr"] or ""
        
        # Look for JSON report in stdout
        try:
            # Try to find JSON report in the output
            import re
            json_match = re.search(r'\{.*"scenarios":.*\}', stdout, re.DOTALL)
            if json_match:
                import json
                report_data = json.loads(json_match.group())
                
                # Display scenario results
                st.markdown("#### 📊 Scenario Results")
                
                total_scenarios = len(report_data.get("scenarios", []))
                passed_scenarios = sum(1 for s in report_data.get("scenarios", []) if s.get("status", "").lower() == "passed")
                failed_scenarios = total_scenarios - passed_scenarios
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Scenarios", total_scenarios)
                with col2:
                    st.metric("Passed", passed_scenarios, delta=f"{passed_scenarios}")
                with col3:
                    st.metric("Failed", failed_scenarios, delta=f"-{failed_scenarios}")
                with col4:
                    success_rate = (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                
                # Detailed scenario breakdown
                st.markdown("#### 📋 Scenario Details")
                for i, scenario in enumerate(report_data.get("scenarios", []), 1):
                    scenario_name = scenario.get("scenario", f"Scenario {i}")
                    status = scenario.get("status", "UNKNOWN").upper()
                    duration = scenario.get("duration", 0)
                    error = scenario.get("error", "")
                    
                    # Create expander for each scenario
                    status_icon = "✅" if status == "PASSED" else "❌"
                    expander_title = f"{status_icon} {scenario_name} ({duration:.2f}s)"
                    
                    with st.expander(expander_title, expanded=(status != "PASSED")):
                        st.markdown(f"**Status:** {status}")
                        st.markdown(f"**Duration:** {duration:.2f} seconds")
                        
                        if scenario.get("steps"):
                            st.markdown("**Steps:**")
                            for step in scenario["steps"]:
                                step_status = "✅" if step.get("status", "").lower() == "passed" else "❌"
                                st.markdown(f"- {step_status} {step.get('description', 'Unknown step')}")
                        
                        if error:
                            st.error(f"**Error:** {error}")
                
                # Overall execution summary
                st.markdown("#### 📈 Execution Summary")
                st.markdown(f"**Total Execution Time:** {report_data.get('total_duration', 0):.2f} seconds")
                st.markdown(f"**Started:** {report_data.get('start_time', 'Unknown')}")
                st.markdown(f"**Completed:** {report_data.get('end_time', 'Unknown')}")
                
            else:
                # Fallback to simple output display
                st.markdown("#### 📄 Raw Output")
                with st.expander("View Raw Output", expanded=(status == "error")):
                    st.subheader("Standard Output")
                    st.code(stdout or "No standard output.", language="log")
                    
                    if stderr:
                        st.subheader("Standard Error")
                        st.code(stderr, language="log")
                    else:
                        st.subheader("Standard Error")
                        st.code("No standard error.", language="log")
                        
        except Exception as e:
            # Fallback to simple output display if JSON parsing fails
            st.markdown("#### 📄 Raw Output")
            with st.expander("View Raw Output", expanded=(status == "error")):
                st.subheader("Standard Output")
                st.code(stdout or "No standard output.", language="log")
                
                if stderr:
                    st.subheader("Standard Error")
                    st.code(stderr, language="log")
                else:
                    st.subheader("Standard Error")
                    st.code("No standard error.", language="log")
                
        st.info("📷 If the script includes screenshots, they will be saved based on its logic.")

if __name__ == "__main__":
    main()
