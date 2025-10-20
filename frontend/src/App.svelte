<script>
    import "./App.css";
    import BucketSelector from "./components/BucketSelector.svelte";
    import ImageGallery from "./components/ImageGallery.svelte";
    import { selectedBucket } from "./stores/bucket.js";

    let bucketName = null;

    selectedBucket.subscribe((value) => {
        bucketName = value;
    });
</script>

<main>
    <header>
        <h1>📦 Google Cloud Storage Bucket Viewer</h1>
        <p>View and browse images from your GCS buckets</p>
    </header>

    <div class="container">
        <BucketSelector />
        {#if bucketName}
            <ImageGallery bucket={bucketName} />
        {:else}
            <div class="empty-state">
                <p>👆 Select a bucket to view images</p>
            </div>
        {/if}
    </div>
</main>

<style>
    main {
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }

    header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }

    header h1 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }

    .container {
        max-width: 1400px;
        margin: 0 auto;
    }

    .empty-state {
        background: white;
        border-radius: 12px;
        padding: 4rem 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .empty-state p {
        font-size: 1.5rem;
        color: #666;
        margin: 0;
    }
</style>
