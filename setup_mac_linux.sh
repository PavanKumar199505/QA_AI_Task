#!/bin/bash

echo "Setting up Automated QA Assistant for Mac/Linux..."

echo
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo
echo "Installing Playwright browsers..."
playwright install

echo
echo "Creating necessary directories..."
mkdir -p ProjectStorage/uploads
mkdir -p ProjectStorage/extracted
mkdir -p ProjectStorage/reports
mkdir -p ProjectStorage/screenshots
mkdir -p ProjectStorage/logs

echo
echo "Setting up Streamlit configuration..."
mkdir -p .streamlit
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "Creating secrets.toml template..."
    cat > .streamlit/secrets.toml << EOF
# Add your Groq API key here
GROQ_API_KEY = "your_groq_api_key_here"

# Get your API key from: https://console.groq.com/
EOF
fi

echo
echo "Installing system dependencies..."

# Detect OS and install appropriate packages
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS. Installing dependencies with Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install it first: https://brew.sh/"
        exit 1
    fi
    brew install tesseract ffmpeg
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux. Installing dependencies with apt..."
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr ffmpeg
else
    echo "Unsupported OS. Please install Tesseract OCR and FFmpeg manually."
fi

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Get a Groq API key from https://console.groq.com/"
echo "2. Edit .streamlit/secrets.toml and add your API key"
echo "3. Or set environment variable: export GROQ_API_KEY=your_key_here"
echo
echo "To start the application:"
echo "streamlit run ui/app.py"
echo 
