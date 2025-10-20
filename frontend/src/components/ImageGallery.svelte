<script>
    import { api } from "../lib/api.js";
    import ImageModal from "./ImageModal.svelte";

    export let bucket;

    let images = [];
    let loading = true;
    let error = null;
    let prefix = "";
    let selectedImage = null;
    let showModal = false;

    $: if (bucket) {
        loadImages();
    }

    async function loadImages() {
        loading = true;
        error = null;
        try {
            images = await api.getImages(bucket, prefix);
        } catch (err) {
            error = err.message;
            console.error("Failed to load images:", err);
        } finally {
            loading = false;
        }
    }

    async function openImage(image) {
        try {
            const imageWithUrl = await api.getImageWithSignedUrl(
                bucket,
                image.name,
            );
            selectedImage = imageWithUrl;
            showModal = true;
        } catch (err) {
            console.error("Failed to get signed URL:", err);
            alert("Failed to load image: " + err.message);
        }
    }

    function closeModal() {
        showModal = false;
        selectedImage = null;
    }

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
        return (bytes / (1024 * 1024)).toFixed(2) + " MB";
    }

    function handleSearch() {
        loadImages();
    }

    function handleImageKeydown(event, image) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openImage(image);
        }
    }
</script>

<div class="image-gallery">
    <div class="gallery-header">
        <h2>📸 Images in {bucket}</h2>
        <div class="search-bar">
            <input
                type="text"
                placeholder="Filter by prefix (e.g., folder/)"
                bind:value={prefix}
                on:keypress={(e) => e.key === "Enter" && handleSearch()}
            />
            <button on:click={handleSearch}>Search</button>
        </div>
    </div>

    {#if loading}
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading images...</p>
        </div>
    {:else if error}
        <div class="error">
            <p>❌ Error: {error}</p>
        </div>
    {:else if images.length === 0}
        <div class="empty">
            <p>📭 No images found in this bucket</p>
            {#if prefix}
                <p class="hint">Try clearing the search filter</p>
            {/if}
        </div>
    {:else}
        <div class="image-count">
            Found {images.length} image{images.length !== 1 ? "s" : ""}
        </div>
        <div class="image-grid">
            {#each images as image}
                <div
                    class="image-card"
                    role="button"
                    tabindex="0"
                    on:click={() => openImage(image)}
                    on:keydown={(e) => handleImageKeydown(e, image)}
                >
                    <div class="image-placeholder">
                        <span class="image-icon">🖼️</span>
                    </div>
                    <div class="image-info">
                        <div class="image-name" title={image.name}>
                            {image.name.split("/").pop()}
                        </div>
                        <div class="image-meta">
                            <span class="image-size"
                                >{formatSize(image.size)}</span
                            >
                            {#if image.content_type}
                                <span class="image-type"
                                    >{image.content_type.split("/")[1]}</span
                                >
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

{#if showModal && selectedImage}
    <ImageModal image={selectedImage} on:close={closeModal} />
{/if}

<style>
    .image-gallery {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .gallery-header {
        margin-bottom: 1.5rem;
    }

    h2 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        color: #333;
    }

    .search-bar {
        display: flex;
        gap: 0.5rem;
    }

    .search-bar input {
        flex: 1;
        padding: 0.75rem;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 1rem;
        transition: border-color 0.2s;
    }

    .search-bar input:focus {
        outline: none;
        border-color: #667eea;
    }

    .search-bar button {
        padding: 0.75rem 1.5rem;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
    }

    .search-bar button:hover {
        background: #5568d3;
    }

    .loading {
        text-align: center;
        padding: 3rem;
        color: #666;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #e0e0e0;
        border-top-color: #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .error,
    .empty {
        text-align: center;
        padding: 2rem;
        color: #666;
    }

    .error {
        background: #fee;
        border-radius: 8px;
        color: #c33;
    }

    .hint {
        font-size: 0.9rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }

    .image-count {
        margin-bottom: 1rem;
        color: #666;
        font-size: 0.95rem;
    }

    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }

    .image-card {
        background: #f9f9f9;
        border-radius: 8px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s;
    }

    .image-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .image-placeholder {
        aspect-ratio: 1;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .image-icon {
        font-size: 3rem;
        opacity: 0.7;
    }

    .image-info {
        padding: 0.75rem;
    }

    .image-name {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .image-meta {
        display: flex;
        gap: 0.5rem;
        font-size: 0.85rem;
        color: #888;
    }

    .image-type {
        text-transform: uppercase;
    }
</style>
