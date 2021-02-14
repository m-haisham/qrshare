<script>
    import { QR } from "../display";
    import { meta, qrUrl } from "../store";
</script>

<svelte:head>
    <title>QR - qrshare</title>
</svelte:head>

<div class="container">
    <QR url={$qrUrl} />
    <div class="manual">
        <h4>Manual</h4>
        <p>Enter the following in your favourite browser</p>
        <code>{$meta.ip}</code>
    </div>
</div>

<style>
    .manual {
        text-align: center;

        padding-top: 1rem;
        padding-bottom: 2rem;
        border-top: 1px solid var(--color-divider);
    }

    p {
        margin-bottom: 1rem;
    }
</style>
