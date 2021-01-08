<script>
    import { Header, HeaderExtension, Search } from "../components/header";
    import { SizedBox } from "../components/utilities";
    import Divider from "../components/Divider.svelte";
    import DualDisplay from "../components/DualDisplay.svelte";
</script>

<Header title="ad" subtitle="~/Subtitle">
    <HeaderExtension>
        <Search onClick={(value) => console.log(value)} />
        <SizedBox width="2rem" />
        <button class="u-full-width header-button">Adv</button>
        <SizedBox width="2rem" />
        <button class="u-full-width header-button">Home</button>
    </HeaderExtension>
</Header>
<Divider />
<div class="container">
    <DualDisplay>
        <div slot="top">top</div>
        <div slot="bottom">bottom</div>
    </DualDisplay>
</div>
