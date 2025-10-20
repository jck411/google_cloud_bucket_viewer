<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";
    import { selectedBucket } from "../stores/bucket.js";

    let buckets = [];
    let loading = true;
    let error = null;
    let currentBucket = null;

    selectedBucket.subscribe((value) => {
        currentBucket = value;
    });

    onMount(async () => {
        try {
            buckets = await api.getBuckets();
        } catch (err) {
            error = err.message;
            console.error("Failed to load buckets:", err);
        } finally {
            loading = false;
        }
    });

    function selectBucket(bucketName) {
        selectedBucket.set(bucketName);
    }
</script>

<div class="bucket-selector">
    <h2>Select a Bucket</h2>

    {#if loading}
        <div class="loading">Loading buckets...</div>
    {:else if error}
        <div class="error">
            <p>❌ Error: {error}</p>
            <p class="hint">
                Make sure your GCS credentials are configured correctly.
            </p>
        </div>
    {:else if buckets.length === 0}
        <div class="empty">No buckets found</div>
    {:else}
        <div class="bucket-list">
            {#each buckets as bucket}
                <button
                    class="bucket-item"
                    class:active={currentBucket === bucket.name}
                    on:click={() => selectBucket(bucket.name)}
                >
                    <span class="bucket-icon">🗂️</span>
                    <div class="bucket-info">
                        <div class="bucket-name">{bucket.name}</div>
                        <div class="bucket-location">{bucket.location}</div>
                    </div>
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
    .bucket-selector {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    h2 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        color: #333;
    }

    .loading,
    .error,
    .empty {
        padding: 1rem;
        text-align: center;
        color: #666;
    }

    .error {
        background: #fee;
        border-radius: 8px;
        color: #c33;
    }

    .error .hint {
        font-size: 0.9rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }

    .bucket-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1rem;
    }

    .bucket-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: #f9f9f9;
        border: 2px solid transparent;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
        text-align: left;
    }

    .bucket-item:hover {
        background: #f0f0f0;
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .bucket-item.active {
        border-color: #667eea;
        background: #f0f4ff;
    }

    .bucket-icon {
        font-size: 2rem;
    }

    .bucket-info {
        flex: 1;
    }

    .bucket-name {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.25rem;
    }

    .bucket-location {
        font-size: 0.85rem;
        color: #888;
    }
</style>
