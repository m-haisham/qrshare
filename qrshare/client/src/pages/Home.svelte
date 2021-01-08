<script>
    import { Header, HeaderExtension, Search } from "../components/header";
    import Divider from "../components/Divider.svelte";
    import { SizedBox } from "../components/utilities";
</script>

<Header title="~/" subtitle="subtitle">
    <HeaderExtension>
        <Search onClick={(value) => console.log(value)} />
        <SizedBox width="2rem" />
        <button class="u-full-width header-button">Adv</button>
        <SizedBox width="2rem" />
        <button class="u-full-width header-button">Home</button>
    </HeaderExtension>
</Header>
<Divider />
