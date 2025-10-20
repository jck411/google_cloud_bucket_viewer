"""FastAPI application for Google Cloud Storage bucket viewer."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import settings
from src.gcs_service import GCSService

# Initialize FastAPI app
app = FastAPI(
    title="GCS Bucket Viewer API",
    description="API for viewing images from Google Cloud Storage buckets",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GCS service
gcs_service = GCSService(
    project_id=settings.gcs_project_id,
    credentials_path=settings.google_application_credentials,
)


# Pydantic models
class BucketInfo(BaseModel):
    """Bucket information model."""

    name: str
    location: str


class ImageInfo(BaseModel):
    """Image information model."""

    name: str
    size: int
    content_type: str | None
    updated: str | None
    public_url: str | None = None


class ImageWithSignedUrl(BaseModel):
    """Image with signed URL model."""

    name: str
    size: int
    content_type: str | None
    updated: str | None
    signed_url: str


class SignedUrlRequest(BaseModel):
    """Request model for generating signed URL."""

    blob_name: str
    expiration_minutes: int = 60


# API endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "GCS Bucket Viewer API",
        "version": "0.1.0",
        "endpoints": {
            "buckets": "/api/buckets",
            "images": "/api/images/{bucket_name}",
            "signed_url": "/api/signed-url/{bucket_name}",
        },
    }


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/buckets", response_model=list[BucketInfo])
async def list_buckets():
    """List all buckets in the project."""
    try:
        buckets = gcs_service.list_buckets()
        return buckets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list buckets: {str(e)}")


@app.get("/api/images/{bucket_name}", response_model=list[ImageInfo])
async def list_images(bucket_name: str, prefix: str = ""):
    """List all images in a bucket.

    Args:
        bucket_name: Name of the bucket
        prefix: Optional prefix to filter images
    """
    try:
        images = gcs_service.list_images(bucket_name, prefix=prefix)
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list images: {str(e)}")


@app.get(
    "/api/images/{bucket_name}/{blob_name:path}", response_model=ImageWithSignedUrl
)
async def get_image_with_signed_url(
    bucket_name: str, blob_name: str, expiration_minutes: int = 60
):
    """Get image with a signed URL.

    Args:
        bucket_name: Name of the bucket
        blob_name: Name of the blob (image)
        expiration_minutes: URL expiration time in minutes
    """
    try:
        image = gcs_service.get_image_with_signed_url(
            bucket_name, blob_name, expiration_minutes
        )
        return image
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get image: {str(e)}")


@app.post("/api/signed-url/{bucket_name}", response_model=dict[str, str])
async def generate_signed_url(bucket_name: str, request: SignedUrlRequest):
    """Generate a signed URL for a blob.

    Args:
        bucket_name: Name of the bucket
        request: Request with blob name and expiration time
    """
    try:
        url = gcs_service.generate_signed_url(
            bucket_name,
            request.blob_name,
            request.expiration_minutes,
        )
        return {"signed_url": url}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate signed URL: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
