<script>
    import DualDisplay from "../components/DualDisplay.svelte";
    import { RouteList, QR } from "./display";
    import { qrUrl } from "./store";
</script>

<div class="container">
    <DualDisplay>
        <div slot="top">
            <RouteList />
        </div>
        <div slot="bottom">
            <QR url={$qrUrl} />
        </div>
    </DualDisplay>
</div>

<style>
    .container {
        margin-top: 1rem;
    }

    @media (min-width: 550px) {
        .container {
            margin-top: 2rem;
        }
    }
</style>
