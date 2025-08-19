@echo off
echo Setting up Automated QA Assistant for Windows...

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing Playwright browsers...
playwright install

echo.
echo Creating necessary directories...
if not exist "ProjectStorage" mkdir ProjectStorage
if not exist "ProjectStorage\uploads" mkdir ProjectStorage\uploads
if not exist "ProjectStorage\extracted" mkdir ProjectStorage\extracted
if not exist "ProjectStorage\reports" mkdir ProjectStorage\reports
if not exist "ProjectStorage\screenshots" mkdir ProjectStorage\screenshots
if not exist "ProjectStorage\logs" mkdir ProjectStorage\logs

echo.
echo Setting up Streamlit configuration...
if not exist ".streamlit" mkdir .streamlit
if not exist ".streamlit\secrets.toml" (
    echo Creating secrets.toml template...
    echo # Add your Groq API key here > .streamlit\secrets.toml
    echo GROQ_API_KEY = "your_groq_api_key_here" >> .streamlit\secrets.toml
    echo. >> .streamlit\secrets.toml
    echo # Get your API key from: https://console.groq.com/ >> .streamlit\secrets.toml
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Get a Groq API key from https://console.groq.com/
echo 2. Edit .streamlit\secrets.toml and add your API key
echo 3. Install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki
echo 4. Install FFmpeg from: https://ffmpeg.org/download.html
echo 5. Add Tesseract and FFmpeg to your system PATH
echo.
echo To start the application:
echo streamlit run ui/app.py
echo.
pause 
