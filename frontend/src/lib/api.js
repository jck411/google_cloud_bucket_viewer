import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = {
    async getBuckets() {
        const response = await axios.get(`${API_BASE_URL}/api/buckets`)
        return response.data
    },

    async getImages(bucketName, prefix = '') {
        const params = prefix ? { prefix } : {}
        const response = await axios.get(`${API_BASE_URL}/api/images/${bucketName}`, { params })
        return response.data
    },

    async getImageWithSignedUrl(bucketName, blobName, expirationMinutes = 60) {
        const encodedBlobName = encodeURIComponent(blobName)
        const response = await axios.get(
            `${API_BASE_URL}/api/images/${bucketName}/${encodedBlobName}`,
            { params: { expiration_minutes: expirationMinutes } }
        )
        return response.data
    },

    async generateSignedUrl(bucketName, blobName, expirationMinutes = 60) {
        const response = await axios.post(`${API_BASE_URL}/api/signed-url/${bucketName}`, {
            blob_name: blobName,
            expiration_minutes: expirationMinutes
        })
        return response.data.signed_url
    }
}
