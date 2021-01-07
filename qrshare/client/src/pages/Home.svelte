<script>
    import { Header, HeaderExtension } from "../components/header";
    import Divider from "../components/Divider.svelte";
    import { SizedBox } from "../components/utilities";
</script>

<Header title="~/" subtitle="subtitle">
    <HeaderExtension>
        <button class="u-full-width header-button">Home</button>
        <SizedBox width="2rem" />
        <button class="u-full-width header-button">Home</button>
        <SizedBox width="2rem" />
        <button class="u-full-width header-button">Home</button>
    </HeaderExtension>
</Header>
<Divider />
