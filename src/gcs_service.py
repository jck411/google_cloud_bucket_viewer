"""Google Cloud Storage service for listing and accessing images."""

import os
from datetime import timedelta
from typing import Any

from google.cloud import storage
from google.cloud.storage import Bucket


class GCSService:
    """Service for interacting with Google Cloud Storage."""

    def __init__(
        self, project_id: str | None = None, credentials_path: str | None = None
    ):
        """Initialize GCS client.

        Args:
            project_id: GCP project ID
            credentials_path: Path to service account JSON file
        """
        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = storage.Client(project=project_id)

    def list_buckets(self) -> list[dict[str, str]]:
        """List all buckets in the project.

        Returns:
            List of bucket information dictionaries
        """
        buckets = self.client.list_buckets()
        return [
            {"name": bucket.name, "location": bucket.location} for bucket in buckets
        ]

    def get_bucket(self, bucket_name: str) -> Bucket:
        """Get a bucket by name.

        Args:
            bucket_name: Name of the bucket

        Returns:
            Bucket object

        Raises:
            Exception: If bucket not found
        """
        return self.client.bucket(bucket_name)

    def list_images(
        self,
        bucket_name: str,
        prefix: str = "",
        extensions: tuple[str, ...] = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
        ),
        include_signed_urls: bool = True,
        expiration_minutes: int = 60,
    ) -> list[dict[str, Any]]:
        """List all image files in a bucket.

        Args:
            bucket_name: Name of the bucket
            prefix: Optional prefix to filter blobs
            extensions: Tuple of valid image extensions
            include_signed_urls: Whether to generate signed URLs for thumbnails
            expiration_minutes: URL expiration time in minutes

        Returns:
            List of image metadata dictionaries
        """
        bucket = self.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        images = []
        for blob in blobs:
            if blob.name.lower().endswith(extensions):
                image_data = {
                    "name": blob.name,
                    "size": blob.size,
                    "content_type": blob.content_type,
                    "updated": blob.updated.isoformat() if blob.updated else None,
                    "public_url": blob.public_url if blob.public_url else None,
                    "thumbnail_url": None,
                }

                if include_signed_urls:
                    try:
                        image_data["thumbnail_url"] = self.generate_signed_url(
                            bucket_name, blob.name, expiration_minutes
                        )
                    except Exception:
                        # If signed URL generation fails, continue without it
                        pass

                images.append(image_data)

        return images

    def generate_signed_url(
        self, bucket_name: str, blob_name: str, expiration_minutes: int = 60
    ) -> str:
        """Generate a signed URL for accessing a private blob.

        Args:
            bucket_name: Name of the bucket
            blob_name: Name of the blob
            expiration_minutes: URL expiration time in minutes

        Returns:
            Signed URL string
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
        )

        return url

    def get_image_with_signed_url(
        self, bucket_name: str, blob_name: str, expiration_minutes: int = 60
    ) -> dict[str, Any]:
        """Get image metadata with a signed URL.

        Args:
            bucket_name: Name of the bucket
            blob_name: Name of the blob
            expiration_minutes: URL expiration time in minutes

        Returns:
            Dictionary with image metadata and signed URL
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Reload to get latest metadata
        if blob.exists():
            blob.reload()

            return {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "updated": blob.updated.isoformat() if blob.updated else None,
                "signed_url": self.generate_signed_url(
                    bucket_name, blob_name, expiration_minutes
                ),
            }

        raise ValueError(f"Blob {blob_name} not found in bucket {bucket_name}")

    def delete_image(self, bucket_name: str, blob_name: str) -> bool:
        """Delete an image from a bucket.

        Args:
            bucket_name: Name of the bucket
            blob_name: Name of the blob to delete

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If blob not found
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        if not blob.exists():
            raise ValueError(f"Blob {blob_name} not found in bucket {bucket_name}")

        blob.delete()
        return True

    def delete_images(self, bucket_name: str, blob_names: list[str]) -> dict[str, Any]:
        """Delete multiple images from a bucket.

        Args:
            bucket_name: Name of the bucket
            blob_names: List of blob names to delete

        Returns:
            Dictionary with success count and any errors
        """
        bucket = self.get_bucket(bucket_name)
        results = {"deleted": 0, "failed": 0, "errors": []}

        for blob_name in blob_names:
            try:
                blob = bucket.blob(blob_name)
                if blob.exists():
                    blob.delete()
                    results["deleted"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(
                        {"blob_name": blob_name, "error": "Blob not found"}
                    )
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({"blob_name": blob_name, "error": str(e)})

        return results
