<script>
    export let title;
    export let subtitle = null;

    import { Title, Subtitle } from "../../typography";
    import Divider from "../Divider.svelte";
</script>

<header>
    <div class="container">
        <div>
            <Title>{title}</Title>
            {#if subtitle}
                <Subtitle>{subtitle}</Subtitle>
            {/if}
        </div>
        <slot />
    </div>
    <Divider />
</header>

<style>
    header > div {
        display: flex;
        flex-direction: column;
    }

    @media (min-width: 550px) {
        header > div {
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
        }
    }
</style>
