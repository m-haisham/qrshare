<script>
    import DualDisplay from "../components/DualDisplay.svelte";
    import { RouteList, QR } from "./display";
    import { qrUrl } from "./store";
</script>

<DualDisplay>
    <div slot="top">
        <RouteList />
    </div>
    <div slot="bottom">
        <QR url={$qrUrl} />
    </div>
</DualDisplay>
