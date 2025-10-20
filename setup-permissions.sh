#!/bin/bash
# Script to grant Storage permissions to your service account

PROJECT_ID="pihome123"
SERVICE_ACCOUNT="openrouter-agent@pihome123.iam.gserviceaccount.com"

echo "🔐 Granting Storage Admin role to service account..."

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/storage.admin"

echo "✅ Done! You can now run the application."
