<script>
    import { Header, HeaderExtension, Search } from "../components/header";
    import { SizedBox } from "../utilities";
    import Divider from "../components/Divider.svelte";
    import DualDisplay from "../components/DualDisplay.svelte";
    import { RouteList, QR } from "./display";
    import { currentRoute as current, qrUrl } from "./store";
    import { createLink } from "../helper";

    function currentZip() {
        createLink($current.zip).click();
    }
</script>

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

<Header
    title={$current.name}
    subtitle={$current.parent ? '~' + $current.parent.href : null}>
    <HeaderExtension>
        <Search on:submit={(e) => console.log(e.detail.query)} />
        <SizedBox width="2rem" />
        <button
            class="u-full-width header-button"
            on:click={currentZip}>Zip</button>
    </HeaderExtension>
</Header>
<Divider />
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
