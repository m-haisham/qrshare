<script>
    export let data;

    import { Header, HeaderExtension, Search } from "../components/header";
    import { SizedBox } from "../components/utilities";
    import Divider from "../components/Divider.svelte";
    import DualDisplay from "../components/DualDisplay.svelte";
    import { RouteList, QR } from "../components/display";
</script>

<Header title={data.name} subtitle={data.parent ? data.parent.name : null}>
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
            <RouteList parent={data.parent} routes={data.routes} />
        </div>
        <div slot="bottom">
            <QR />
        </div>
    </DualDisplay>
</div>
