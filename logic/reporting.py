import logging
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
import json
from logic.util import get_project_root

logger = logging.getLogger(__name__)

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Automated QA Assistant Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_pdf_report(data):
    """Generate a PDF report from the analysis data"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Set margins to ensure proper spacing
        pdf.set_margins(20, 20, 20)
        
        # Set title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Automated QA Analysis Report", ln=True, align='C')
        pdf.ln(10)
        
        # Add content with Unicode support
        pdf.set_font("Arial", "", 12)
        
        # Clean text to remove problematic Unicode characters
        clean_text = clean_text_for_pdf(data.get("extracted_text", ""))
        
        # Safely get filename with fallback
        filename = data.get("filename", "Unknown File")
        timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Add file information with proper spacing
        try:
            pdf.cell(0, 5, f"File: {filename}", ln=True)
            pdf.cell(0, 5, f"Analysis Date: {timestamp}", ln=True)
            pdf.ln(5)
        except Exception as e:
            logging.warning(f"Error adding file info to PDF: {str(e)}")
            # Fallback to simpler text
            pdf.cell(0, 5, "File Analysis Report", ln=True)
        
        # Add extracted text with better error handling
        try:
            pdf.cell(0, 5, "Extracted Text:", ln=True)
            
            # Use a more conservative approach for text rendering
            if clean_text:
                # Limit text length and split into very small chunks
                limited_text = clean_text[:500]  # Reduced from 1000 to 500
                text_chunks = split_text_for_pdf(limited_text, max_chunk_size=100)  # Reduced chunk size
                
                for chunk in text_chunks:
                    if chunk.strip():
                        try:
                            # Use cell instead of multi_cell for better control
                            pdf.cell(0, 5, chunk, ln=True)
                        except Exception as chunk_error:
                            logging.warning(f"Error rendering chunk: {chunk_error}")
                            # Skip problematic chunks
                            continue
                
                if len(clean_text) > 500:
                    pdf.cell(0, 5, "...", ln=True)
            else:
                pdf.cell(0, 5, "No text content available", ln=True)
                
        except Exception as e:
            logging.warning(f"Error adding extracted text to PDF: {str(e)}")
            pdf.cell(0, 5, "Text content could not be displayed due to formatting issues.", ln=True)
        
        # Add summary if available
        summary = data.get("summary", "")
        if summary and summary != "Summarization unavailable: Please configure an OpenAI API key.":
            try:
                pdf.ln(5)
                pdf.cell(0, 5, "Summary:", ln=True)
                clean_summary = clean_text_for_pdf(summary)
                summary_chunks = split_text_for_pdf(clean_summary, max_chunk_size=100)
                for chunk in summary_chunks:
                    if chunk.strip():
                        pdf.cell(0, 5, chunk, ln=True)
            except Exception as e:
                logging.warning(f"Error adding summary to PDF: {str(e)}")
        
        # Add test cases if available
        test_cases = data.get("test_cases", [])
        if test_cases:
            try:
                pdf.ln(5)
                pdf.cell(0, 5, "Suggested Test Cases:", ln=True)
                for i, test_case in enumerate(test_cases, 1):
                    clean_test_case = clean_text_for_pdf(test_case)
                    pdf.cell(0, 5, f"{i}. {clean_test_case}", ln=True)
            except Exception as e:
                logging.warning(f"Error adding test cases to PDF: {str(e)}")
        
        # Save the report
        report_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"ProjectStorage/reports/analysis_report_{report_timestamp}.pdf"
        pdf.output(report_path)
        
        return report_path
        
    except Exception as e:
        logging.error(f"PDF report generation error: {str(e)}")
        raise

def split_text_for_pdf(text, max_chunk_size=100):
    """Split text into smaller chunks to avoid PDF layout issues"""
    if not text:
        return [""]
    
    # Clean the text first
    text = str(text).strip()
    if not text:
        return [""]
    
    # Split by sentences first, then by words if needed
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # If we still have chunks that are too long, split by words
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_chunk_size:
            words = chunk.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 < max_chunk_size:
                    temp_chunk += word + " "
                else:
                    if temp_chunk:
                        final_chunks.append(temp_chunk.strip())
                    temp_chunk = word + " "
            if temp_chunk:
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)
    
    # If we still have issues, split by character count
    if not final_chunks:
        final_chunks = [text]
    
    # Final safety check - ensure no chunk is too long
    safe_chunks = []
    for chunk in final_chunks:
        if len(chunk) > max_chunk_size:
            # Split by character count
            for i in range(0, len(chunk), max_chunk_size):
                safe_chunks.append(chunk[i:i + max_chunk_size])
        else:
            safe_chunks.append(chunk)
    
    return safe_chunks if safe_chunks else [text[:max_chunk_size]]

def clean_text_for_pdf(text):
    """Clean text to remove problematic Unicode characters for PDF generation"""
    if not text:
        return ""
    
    # Remove or replace problematic Unicode characters
    import re
    
    # Replace common emojis and special characters with text equivalents
    replacements = {
        '🔧': '[TOOL]',
        '📋': '[CLIPBOARD]',
        '✅': '[CHECK]',
        '❌': '[X]',
        '⚠️': '[WARNING]',
        '💡': '[IDEA]',
        '🚀': '[ROCKET]',
        '🎯': '[TARGET]',
        '⚡': '[LIGHTNING]',
        '🔍': '[SEARCH]',
        '📝': '[NOTE]',
        '🔄': '[REFRESH]',
        '📊': '[CHART]',
        '🔗': '[LINK]',
        '📱': '[MOBILE]',
        '💻': '[COMPUTER]',
        '🌐': '[WEB]',
        '🔒': '[LOCK]',
        '🔓': '[UNLOCK]',
        '📈': '[TREND_UP]',
        '📉': '[TREND_DOWN]',
    }
    
    # Apply replacements
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    
    # Remove any remaining non-ASCII characters that might cause issues
    # Keep basic punctuation and common symbols
    text = re.sub(r'[^\x00-\x7F\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF]+', '', text)
    
    # Remove any control characters that might cause issues
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    return text

def generate_txt_report(data: dict) -> Path:
    """Generate a TXT report from analysis data."""
    try:
        reports_dir = Path(get_project_root()) / "ProjectStorage" / "reports"
        txt_path = reports_dir / f"QA_Report_{data['timestamp']}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"Automated QA Assistant Report\n")
            f.write(f"Generated: {data['timestamp']}\n\n")
            if data["extracted_text"]:
                f.write("Extracted Text:\n")
                f.write(data["extracted_text"][:1000] + ("...\n" if len(data["extracted_text"]) > 1000 else "\n"))
                f.write("\n")
            if data["summary"]:
                f.write("Summary:\n")
                f.write(data["summary"] + "\n\n")
            if data["test_cases"]:
                f.write("Suggested Test Cases:\n")
                for i, test_case in enumerate(data["test_cases"], 1):
                    f.write(f"{i}. {test_case}\n")
        logger.info(f"TXT report generated at {txt_path}")
        return txt_path
    except Exception as e:
        logger.error(f"TXT report generation error: {str(e)}", exc_info=True)
        raise

def generate_json_report(data: dict) -> Path:
    """Generate a JSON report from analysis data."""
    try:
        reports_dir = Path(get_project_root()) / "ProjectStorage" / "reports"
        json_path = reports_dir / f"QA_Report_{data['timestamp']}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"JSON report generated at {json_path}")
        return json_path
    except Exception as e:
        logger.error(f"JSON report generation error: {str(e)}", exc_info=True)
        raise
