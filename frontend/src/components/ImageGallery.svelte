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
    let selectionMode = false;
    let selectedImages = new Set();
    let deleting = false;

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
            if (selectionMode) {
                toggleSelection(image);
            } else {
                openImage(image);
            }
        }
    }

    function toggleSelectionMode() {
        selectionMode = !selectionMode;
        if (!selectionMode) {
            selectedImages.clear();
            selectedImages = selectedImages;
        }
    }

    function toggleSelection(image) {
        if (selectedImages.has(image.name)) {
            selectedImages.delete(image.name);
        } else {
            selectedImages.add(image.name);
        }
        selectedImages = selectedImages;
    }

    function selectAll() {
        selectedImages = new Set(images.map((img) => img.name));
    }

    function deselectAll() {
        selectedImages.clear();
        selectedImages = selectedImages;
    }

    async function deleteSelected() {
        if (selectedImages.size === 0) return;

        const count = selectedImages.size;
        const confirmed = confirm(
            `Are you sure you want to delete ${count} image${count !== 1 ? "s" : ""}?`,
        );

        if (!confirmed) return;

        deleting = true;
        try {
            const result = await api.deleteImages(
                bucket,
                Array.from(selectedImages),
            );

            if (result.deleted > 0) {
                alert(
                    `Successfully deleted ${result.deleted} image${result.deleted !== 1 ? "s" : ""}` +
                        (result.failed > 0
                            ? `. Failed to delete ${result.failed}.`
                            : ""),
                );
                selectedImages.clear();
                selectedImages = selectedImages;
                await loadImages();
            }

            if (result.errors.length > 0) {
                console.error("Delete errors:", result.errors);
            }
        } catch (err) {
            console.error("Failed to delete images:", err);
            alert("Failed to delete images: " + err.message);
        } finally {
            deleting = false;
        }
    }

    function handleCardClick(image, event) {
        if (selectionMode) {
            event.stopPropagation();
            toggleSelection(image);
        } else {
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
            <button
                class="select-btn"
                class:active={selectionMode}
                on:click={toggleSelectionMode}
            >
                {selectionMode ? "Cancel" : "Select"}
            </button>
        </div>
        {#if selectionMode}
            <div class="selection-toolbar">
                <div class="selection-info">
                    {selectedImages.size} selected
                </div>
                <div class="selection-actions">
                    <button class="action-btn" on:click={selectAll}
                        >Select All</button
                    >
                    <button class="action-btn" on:click={deselectAll}
                        >Deselect All</button
                    >
                    <button
                        class="delete-btn"
                        on:click={deleteSelected}
                        disabled={selectedImages.size === 0 || deleting}
                    >
                        {deleting
                            ? "Deleting..."
                            : `Delete (${selectedImages.size})`}
                    </button>
                </div>
            </div>
        {/if}
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
                    class:selected={selectedImages.has(image.name)}
                    class:selection-mode={selectionMode}
                    role="button"
                    tabindex="0"
                    on:click={(e) => handleCardClick(image, e)}
                    on:keydown={(e) => handleImageKeydown(e, image)}
                >
                    {#if selectionMode}
                        <div class="selection-checkbox">
                            <input
                                type="checkbox"
                                checked={selectedImages.has(image.name)}
                                on:change|stopPropagation={() =>
                                    toggleSelection(image)}
                                on:click|stopPropagation
                            />
                        </div>
                    {/if}
                    <div class="image-thumbnail">
                        {#if image.thumbnail_url}
                            <img
                                src={image.thumbnail_url}
                                alt={image.name}
                                loading="lazy"
                            />
                        {:else}
                            <span class="image-icon">🖼️</span>
                        {/if}
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

    .select-btn {
        background: #48bb78 !important;
    }

    .select-btn:hover {
        background: #38a169 !important;
    }

    .select-btn.active {
        background: #e53e3e !important;
    }

    .select-btn.active:hover {
        background: #c53030 !important;
    }

    .selection-toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        padding: 0.75rem 1rem;
        background: #f7fafc;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }

    .selection-info {
        font-weight: 600;
        color: #4a5568;
    }

    .selection-actions {
        display: flex;
        gap: 0.5rem;
    }

    .action-btn {
        padding: 0.5rem 1rem;
        background: white;
        color: #4a5568;
        border: 1px solid #cbd5e0;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }

    .action-btn:hover {
        background: #edf2f7;
        border-color: #a0aec0;
    }

    .delete-btn {
        padding: 0.5rem 1rem;
        background: #e53e3e;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
    }

    .delete-btn:hover:not(:disabled) {
        background: #c53030;
    }

    .delete-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
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
        position: relative;
    }

    .image-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .image-card.selected {
        border: 3px solid #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }

    .selection-checkbox {
        position: absolute;
        top: 0.5rem;
        left: 0.5rem;
        z-index: 10;
        background: white;
        border-radius: 4px;
        padding: 0.25rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .selection-checkbox input[type="checkbox"] {
        width: 1.25rem;
        height: 1.25rem;
        cursor: pointer;
    }

    .image-thumbnail {
        aspect-ratio: 1;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .image-thumbnail img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.2s;
    }

    .image-card:hover .image-thumbnail img {
        transform: scale(1.05);
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
