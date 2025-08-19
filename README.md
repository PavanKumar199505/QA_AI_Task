# Automated QA Assistant

A comprehensive QA automation tool that helps engineers and developers analyze files, generate test cases, and Genarate automation scripts using AI-powered analysis.

## Features

### 📁 File Analysis
- **Multi-format Support**: Upload audio (MP3, WAV), video (MP4), images, PDFs, DOCX, or text files
- **AI-powered Summarization**: Uses Groq LLM to analyze and summarize extracted content
- **Automated Test Case Generation**: Generate comprehensive test cases based on content analysis
- **Export Options**: Download results in PDF, TXT, and JSON formats

### Automated Tests
- **Playwright Integration**: Run pre-built tests on SauceDemo.com(Scripts running part its not working properly due AI API Key which I used is free version)
- **Local Execution**: All tests run locally with no external dependencies
- **Result Tracking**: View detailed test results and screenshots

### 💾 Local Storage
- **Project-based Organization**: All data stored locally in `ProjectStorage/` directory
- **Privacy-focused**: No data sent to external servers (except for AI features)
- **Structured Output**: Organized project folders with main documentation

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR (for image text extraction)
- FFmpeg (for audio/video processing)

### Installation
1. Add folder in VS code then activate the .venv 
  1.  python -m venv .venv                                                                                                                                               
  2.  .venv\Scripts\activate                                                                                                                                                  

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

4. **Set up Tesseract OCR**
   - **Windows**: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

### Configuration

#### For AI Features (Optional)
1. Get a Groq API key from [Groq Console](https://console.groq.com/)
2. Set the API key in one of these ways:
   - **Environment variable**: `export GROQ_API_KEY=your_key_here`
   - **Streamlit secrets**: Create `.streamlit/secrets.toml` with `GROQ_API_KEY = "your_key_here"`
   - **UI Configuration**: Enter the key in the app's sidebar

#### For Basic Features
- No API key required! File extraction and automated tests work immediately.

## Usage

### Starting the Application
```bash
streamlit run ui/app.py
```

### File Analysis Workflow
1. Navigate to "File Analysis" in the sidebar
2. Upload a supported file (MP3, WAV, MP4, PDF, DOCX)
3. The system will automatically:
   - Extract text from the file
   - Generate AI-powered summary (if API key configured)
   - Create test cases (if API key configured)
4. Download results in your preferred format

### Automated Testing
1. Navigate to "Automated Tests" in the sidebar
2. Click "Run Automated Tests"
3. View results and screenshots

## Project Structure

```
AutomatedQA/
├── automation/          # Playwright test scripts
├── logic/              # Core business logic
│   ├── extraction.py   # File text extraction
│   ├── llm.py         # Groq LLM integration
│   ├── reporting.py   # Report generation
│   └── util.py        # Utility functions
├── ui/                 # Streamlit user interface
├── ProjectStorage/     # Local data storage
│   ├── uploads/        # Uploaded files
│   ├── extracted/      # Extracted text
│   ├── reports/        # Generated reports
│   └── screenshots/    # Test screenshots
└── requirements.txt    # Python dependencies
```

## Supported File Types

| Type | Extensions | Features |
|------|------------|----------|
| Audio | MP3, WAV | Speech-to-text transcription |
| Video | MP4 | Audio extraction + transcription |
| Documents | PDF, DOCX | Text extraction + OCR fallback |
| Images | PNG, JPG, JPEG | OCR text extraction |

## AI Models Used

- **Groq LLM**: Uses `llama3-8b-8192` model for:
  - Text summarization
  - Test case generation
  - Content analysis

## Troubleshooting

### Common Issues

1. **"No API key configured"**
   - Get a Groq API key from [console.groq.com](https://console.groq.com/)
   - Enter it in the sidebar configuration

2. **PDF extraction fails**
   - Ensure the PDF is not encrypted
   - Try a different PDF file
   - Check if Tesseract OCR is installed

3. **Audio transcription issues**
   - Ensure audio quality is good
   - Check if FFmpeg is installed
   - Verify the audio language is supported

4. **Playwright tests fail**
   - Run `playwright install` to install browsers
   - Check internet connection for SauceDemo.com

### Environment Setup

For Windows users, you may need to add these to your PATH:
- Tesseract installation directory
- FFmpeg installation directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `ProjectStorage/logs/`
3. Create an issue in the repository 
