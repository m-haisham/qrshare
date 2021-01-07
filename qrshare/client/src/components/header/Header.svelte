<script>
    export let title;
    export let subtitle = null;

    import { Title, Subtitle } from "../typography";
</script>

<style>
    header {
        display: flex;
        flex-direction: column;
    }

    @media (min-width: 550px) {
        header {
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
        }
    }
</style>

<header class="container">
    <div>
        <Title>{title}</Title>
        {#if subtitle}
            <Subtitle>{subtitle}</Subtitle>
        {/if}
    </div>
    <slot ref="no-bottom" />
</header>
