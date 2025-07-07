# DOCX to PDF Converter - Cloud Run

This project provides a service to convert DOCX and DOC files to PDF using Flask, LibreOffice, and Docker, deployed on Google Cloud Run.

## 🚀 Features

✅ Converts DOCX and DOC files to PDF
✅ Simple and easy-to-use REST API
✅ Containerized with Docker
✅ Optimized for Google Cloud Run
✅ Health checks included
✅ Detailed logging
✅ Robust error handling

-## 📋 Requirements

- Docker
- Google Cloud SDK (`gcloud`)
- Google Cloud project with billing enabled

## 🏗️ Project Structure

```
convertPDF/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── deploy.sh           # Deployment script
├── .dockerignore       # Docker ignore rules
├── .gitignore          # Git ignore rules
├── .gcloudignore       # Cloud Build ignore rules
└── README.md           # Project documentation
```

## 🛠️ Installation & Deployment

### 1. Configure Google Cloud

```bash
# Install Google Cloud SDK if you haven't already
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project (replace with your PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID
```

### 2. Edit deployment configuration

Edit the `deploy.sh` file and update the following variables:

```bash
PROJECT_ID="your-project-id"     # Replace with your Project ID
SERVICE_NAME="docx-to-pdf-converter"
REGION="us-central1"            # Change if you prefer another region
```

### 3. Deploy

```bash
# Make the script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

## 📡 API Usage

### Available Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `POST /convert` - Convert DOCX or DOC file to PDF

### Convert a file

```bash
# Using curl
curl -X POST \
  -F "file=@document.docx" \
  https://your-service-url/convert \
  --output document.pdf

# Using Python requests
import requests

url = "https://your-service-url/convert"
files = {"file": open("document.docx", "rb")}
response = requests.post(url, files=files)

if response.status_code == 200:
    with open("document.pdf", "wb") as f:
        f.write(response.content)
    print("Conversion successful!")
else:
    print(f"Error: {response.json()}")
```

### JavaScript/HTML Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>DOCX to PDF Converter</title>
</head>
<body>
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" id="fileInput" name="file" accept=".docx,.doc" required>
        <button type="submit">Convert to PDF</button>
    </form>

    <script>
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        const fileInput = document.getElementById('fileInput');
        formData.append('file', fileInput.files[0]);
        
        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'document.pdf';
                a.click();
            } else {
                const error = await response.json();
                alert('Error: ' + error.error);
            }
        } catch (error) {
            alert('Connection error: ' + error.message);
        }
    });
    </script>
</body>
</html>
```

## 🧪 Local Development

docker build -t docx-to-pdf-converter .
docker run -p 8080:8080 docx-to-pdf-converter
### Using Docker

```bash
# Build image
docker build -t docx-to-pdf-converter .

# Run container
docker run -p 8080:8080 docx-to-pdf-converter
```

### Without Docker (requires LibreOffice installed)

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## ⚙️ Configuration

### Environment Variables

* `PORT`: Server port (default: 8080)
* `PYTHONUNBUFFERED`: Enables unbuffered logging

### Cloud Run Resources

The deployment is configured with:
- 2 GB memory
- 2 vCPUs
- 300 seconds timeout
- Maximum 10 instances

## 🔧 Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "libreoffice: command not found"
Asegúrate de que LibreOffice esté instalado:

**Ubuntu/Debian:**
```bash
sudo apt-get install libreoffice
```

**macOS:**
```bash
brew install --cask libreoffice
```

### Error en Cloud Run: "Container failed to start"
Verifica los logs:
```bash
gcloud logs read --service=docx-to-pdf-converter --limit=50
```

## 📊 Monitoring

To monitor the service on Cloud Run:

```bash
# Ver logs
gcloud logs read --service=docx-to-pdf-converter

# Ver métricas
gcloud run services describe docx-to-pdf-converter --region=us-central1
```

## 🔒 Security

* The service validates file types
* Automatically cleans up temporary files
* Uses secure file names
* Implements timeouts to prevent hanging processes

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributions

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 📞 Support

To report bugs or request features, open an issue in the repository.
