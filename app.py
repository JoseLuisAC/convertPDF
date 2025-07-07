import os
import subprocess
import tempfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Configuration
UPLOAD_FOLDER = '/tmp/uploads'
CONVERTED_FOLDER = '/tmp/converted'
ALLOWED_EXTENSIONS = {'docx', 'doc'}

os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Create required directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_docx_to_pdf(input_path, output_dir):
    """Convert DOCX file to PDF using LibreOffice"""
    try:
        # LibreOffice command for conversion
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]
        logger.info(f"Running command: {' '.join(cmd)}")
        # Run the conversion
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # 60 seconds timeout
        )
        if result.returncode == 0:
            logger.info("Conversion successful")
            return True
        else:
            logger.error(f"Conversion error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Conversion timeout")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during conversion: {str(e)}")
        return False

def health_check():

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({"status": "healthy", "service": "docx-to-pdf-converter"}), 200
@app.route('/convert', methods=['POST'])

@app.route('/convert', methods=['POST'])
            pass
    """Main endpoint to convert DOCX files to PDF"""
    try:
        # Check if a file was sent
        if 'file' not in request.files:
            return jsonify({"error": "No file found"}), 400
        file = request.files['file']
        # Check if a file was selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed. Only .docx and .doc files are accepted."}), 400
        # Generate safe file names
        original_filename = secure_filename(file.filename)
        filename_without_ext = os.path.splitext(original_filename)[0]
        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(input_path)
        logger.info(f"File saved: {input_path}")
        # Convert to PDF
        if convert_docx_to_pdf(input_path, CONVERTED_FOLDER):
            # Generate PDF file name
            pdf_filename = f"{filename_without_ext}.pdf"
            pdf_path = os.path.join(CONVERTED_FOLDER, pdf_filename)
            # Check that the PDF file was created
            if os.path.exists(pdf_path):
                logger.info(f"PDF generated: {pdf_path}")
                # Send PDF file
                response = send_file(
                    pdf_path,
                    as_attachment=True,
                    download_name=pdf_filename,
                    mimetype='application/pdf'
                )
                # Clean up temporary files
                try:
                    os.remove(input_path)
                    os.remove(pdf_path)
                except:
                    pass
                return response
            else:
                logger.error("PDF file was not generated correctly")
                return jsonify({"error": "Error converting file"}), 500
        else:
            return jsonify({"error": "Error converting file"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        # Clean up input file in case of error
        try:
            if 'input_path' in locals():
                os.remove(input_path)
        except:
            pass

def index():

@app.route('/', methods=['GET'])
def index():
    """Main page with service information"""
    return jsonify({
        "service": "DOCX to PDF Converter",
        "version": "1.0.0",
        "endpoints": {
            "convert": "/convert (POST) - Converts DOCX files to PDF",
            "health": "/health (GET) - Health check"
        },
        "supported_formats": ["docx", "doc"],
        "usage": "Send a file via POST to /convert with the field 'file'"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
