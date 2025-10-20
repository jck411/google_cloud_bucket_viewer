# 📦 Google Cloud Storage Bucket Viewer

A modern web application to browse and view images from your Google Cloud Storage buckets. Built with FastAPI backend and Svelte frontend.

![GCS Bucket Viewer](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Svelte](https://img.shields.io/badge/Svelte-5.0+-orange.svg)

## ✨ Features

- 🗂️ **Bucket Selection**: Browse and select from all your GCS buckets
- 🖼️ **Image Gallery**: View all images in a beautiful grid layout
- 🔍 **Search & Filter**: Filter images by prefix/folder
- 🔐 **Secure Access**: Generate signed URLs for private bucket access
- ⚡ **Fast & Async**: Built with async/await for optimal performance
- 🎨 **Modern UI**: Beautiful gradient design with smooth interactions
- 📱 **Responsive**: Works great on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌──────────────────┐
│  Svelte         │         │  FastAPI        │         │  Google Cloud    │
│  Frontend       │ ◄─────► │  Backend        │ ◄─────► │  Storage         │
│  (Port 5173)    │         │  (Port 8000)    │         │                  │
└─────────────────┘         └─────────────────┘         └──────────────────┘
```

### Backend (FastAPI)
- **`src/api.py`**: REST API endpoints for buckets and images
- **`src/gcs_service.py`**: Google Cloud Storage service layer
- **`src/config.py`**: Configuration management with Pydantic
- Automatic CORS handling for frontend communication
- Signed URL generation for secure image access

### Frontend (Svelte)
- **Component-based architecture** with reactive stores
- **BucketSelector**: Display and select GCS buckets
- **ImageGallery**: Grid view of all images with search
- **ImageModal**: Full-size image viewer with metadata
- Axios for API communication

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **uv** package manager ([install guide](https://github.com/astral-sh/uv))
- **Google Cloud Project** with Storage API enabled
- **Service Account JSON** with Storage permissions

### 1. Clone and Setup

```bash
# The repository is already in your workspace
cd /home/human/REPOS/google_cloud_bucket_viewer
```

### 2. Configure Google Cloud Credentials

Place your service account JSON file at:
```
credentials/googlecloud/sa.json
```

Or update the path in `.env`

### 3. Update Environment Variables

Edit `.env` file with your configuration:

```bash
# Google Cloud Storage Configuration
GCS_PROJECT_ID=your-gcp-project-id
GCS_BUCKET_NAME=your-default-bucket-name  # Optional
GOOGLE_APPLICATION_CREDENTIALS=credentials/googlecloud/sa.json
```

### 4. Install Dependencies

```bash
# Install Python dependencies with uv
uv sync

# Install Node dependencies
cd frontend && npm install && cd ..
```

### 5. Run the Application

**Option A: Use the startup script (recommended)**
```bash
./run.sh
```

**Option B: Run manually**
```bash
# Terminal 1: Start backend
uv run python -m src.api

# Terminal 2: Start frontend
cd frontend && npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Usage

1. **Select a Bucket**: Choose from your available GCS buckets
2. **Browse Images**: View all images in a grid layout
3. **Filter Images**: Use the search bar to filter by prefix/folder
4. **View Details**: Click any image to see full size with metadata
5. **Download**: Download images or open in a new tab

## 🔧 Configuration

### Backend Configuration (`.env`)

```bash
# GCS Settings
GCS_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=credentials/googlecloud/sa.json

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True

# CORS Settings
CORS_ORIGINS=["http://localhost:5173"]

# Signed URL expiration (minutes)
SIGNED_URL_EXPIRATION_MINUTES=60
```

### Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- WebP
- BMP

## 🔐 Security

- **Signed URLs**: All image access uses time-limited signed URLs
- **CORS Protection**: Configured CORS prevents unauthorized access
- **Service Account**: Uses least-privilege service account credentials
- **No Public Access**: Images don't need to be publicly accessible

## 📁 Project Structure

```
google_cloud_bucket_viewer/
├── src/
│   ├── __init__.py
│   ├── api.py              # FastAPI application
│   ├── gcs_service.py      # GCS service layer
│   ├── config.py           # Configuration
│   └── main.py            # (legacy)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BucketSelector.svelte
│   │   │   ├── ImageGallery.svelte
│   │   │   └── ImageModal.svelte
│   │   ├── stores/
│   │   │   └── bucket.js
│   │   ├── lib/
│   │   │   └── api.js
│   │   ├── App.svelte
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── credentials/
│   └── googlecloud/
│       └── sa.json         # Your service account key
├── tests/
│   └── test_main.py
├── .env                    # Environment configuration
├── pyproject.toml         # Python dependencies
├── run.sh                 # Startup script
└── README.md
```

## 🛠️ Development

### Backend Development

```bash
# Run with auto-reload
uv run python -m src.api

# Run tests
uv run pytest

# Format code
uv run ruff format src/

# Lint code
uv run ruff check src/
```

### Frontend Development

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🐛 Troubleshooting

### "Failed to list buckets" Error

- Verify your service account JSON is in the correct location
- Check that `GCS_PROJECT_ID` is set correctly in `.env`
- Ensure the service account has `Storage Admin` or `Storage Object Viewer` role

### "No images found" Message

- Verify the bucket contains image files with supported extensions
- Try clearing the prefix filter
- Check bucket permissions

### CORS Errors

- Ensure the frontend URL is in `CORS_ORIGINS` in `.env`
- Restart the backend after changing `.env`

### Import Errors (Python)

The import errors shown are expected before installing dependencies. Run:
```bash
uv sync
```

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/api/health` | Health check |
| GET | `/api/buckets` | List all buckets |
| GET | `/api/images/{bucket}` | List images in bucket |
| GET | `/api/images/{bucket}/{blob}` | Get image with signed URL |
| POST | `/api/signed-url/{bucket}` | Generate signed URL |

## 🤝 Contributing

This project follows the guidelines in `.github/copilot-instructions.md`:
- Python 3.11+ with type hints
- PEP 8 formatting with `ruff`
- Async/await for I/O operations
- Comprehensive error handling
- Tests with `pytest`

## 📝 License

This project is for personal/educational use. Ensure compliance with Google Cloud Platform terms of service.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [Svelte](https://svelte.dev/)
- Google Cloud Storage [Python Client](https://github.com/googleapis/python-storage)
- Package management with [uv](https://github.com/astral-sh/uv)

---

Made with ❤️ for viewing GCS bucket images
