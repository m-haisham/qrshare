<script>
    import { qrMarkup } from "../store";
</script>

<div class="qr">
    {@html $qrMarkup}
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 2rem auto;
    }

    div :global(svg) {
        width: auto;
        height: auto;
        max-width: 40rem;
    }
</style>
