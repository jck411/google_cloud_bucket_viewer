<script>
    import { createEventDispatcher } from "svelte";

    export let image;

    const dispatch = createEventDispatcher();

    function close() {
        dispatch("close");
    }

    function handleBackdropClick(e) {
        if (e.target === e.currentTarget) {
            close();
        }
    }

    function handleBackdropKeydown(e) {
        if (e.key === "Escape") {
            close();
        }
    }

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
        return (bytes / (1024 * 1024)).toFixed(2) + " MB";
    }

    function formatDate(dateString) {
        if (!dateString) return "N/A";
        const date = new Date(dateString);
        return date.toLocaleString();
    }
</script>

<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<div
    class="modal-backdrop"
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    on:click={handleBackdropClick}
    on:keydown={handleBackdropKeydown}
>
    <div class="modal-content">
        <button class="close-button" on:click={close}>✕</button>

        <div class="image-container">
            <img src={image.signed_url} alt={image.name} />
        </div>

        <div class="image-details">
            <h3>{image.name.split("/").pop()}</h3>
            <div class="details-grid">
                <div class="detail-item">
                    <span class="label">Full Path:</span>
                    <span class="value">{image.name}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Size:</span>
                    <span class="value">{formatSize(image.size)}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Type:</span>
                    <span class="value">{image.content_type || "Unknown"}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Last Modified:</span>
                    <span class="value">{formatDate(image.updated)}</span>
                </div>
            </div>
            <a
                href={image.signed_url}
                target="_blank"
                rel="noopener noreferrer"
                class="download-link"
            >
                ⬇️ Download / Open in New Tab
            </a>
        </div>
    </div>
</div>

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: 2rem;
        backdrop-filter: blur(4px);
    }

    .modal-content {
        background: white;
        border-radius: 12px;
        max-width: 900px;
        max-height: 90vh;
        overflow: auto;
        position: relative;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    .close-button {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 40px;
        height: 40px;
        background: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        z-index: 10;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .close-button:hover {
        background: rgba(0, 0, 0, 0.8);
        transform: scale(1.1);
    }

    .image-container {
        background: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 300px;
        max-height: 60vh;
    }

    .image-container img {
        width: 100%;
        height: auto;
        max-height: 60vh;
        object-fit: contain;
    }

    .image-details {
        padding: 1.5rem;
    }

    h3 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        color: #333;
        word-break: break-word;
    }

    .details-grid {
        display: grid;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .detail-item {
        display: grid;
        grid-template-columns: 150px 1fr;
        gap: 1rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e0e0e0;
    }

    .label {
        font-weight: 600;
        color: #666;
    }

    .value {
        color: #333;
        word-break: break-all;
    }

    .download-link {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background: #667eea;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        transition: background 0.2s;
    }

    .download-link:hover {
        background: #5568d3;
    }
</style>
