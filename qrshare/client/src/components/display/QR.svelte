<script>
    export let url;
</script>

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

    @media (min-width: 550px) {
        div {
            margin: auto;
        }
    }
</style>

<div>
    <object data={url} type="image/svg+xml" title="QR"><img
            src={url}
            alt="QR" />
    </object>
</div>
