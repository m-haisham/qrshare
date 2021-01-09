<script>
    import { Header, HeaderExtension, Search } from "../components/header";
    import { SizedBox } from "../utilities";
    import Divider from "../components/Divider.svelte";
    import DualDisplay from "../components/DualDisplay.svelte";
    import { RouteList, QR } from "../components/display";
    import { currentRoute as current, qrUrl } from "../store/store";
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
    subtitle={$current.parent ? $current.parent.name : null}>
    <HeaderExtension>
        <Search onClick={(value) => console.log(value)} />
        <!-- <SizedBox width="2rem" /> -->
        <!-- <button class="u-full-width header-button">Home</button> -->
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
