<script>
    import Funnel from "../../../module/icons/Funnel.svelte";
    import { searchCollapsed } from "../store";
</script>

<div class:active={!$searchCollapsed}>
    <Funnel />
</div>

<style>
    div {
        display: flex;
        align-items: center;
    }

    div :global(svg) {
        width: 2rem;
        height: 2rem;
    }

    div.active :global(svg) {
        fill: var(--color-primary);
    }
</style>
