<script>
    export let url;
</script>

<div class="qr">
    <object data={url} type="image/svg+xml" title="QR"
        ><img src={url} alt="QR" />
    </object>
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 2rem auto;
    }

    object {
        width: 100%;
        max-width: 40rem;
    }
</style>
