<script>
    import CaretLeftSquare from "../../../module/icons/CaretLeftSquare.svelte";
    import { navigateHome } from "../utils/navigation";
    import { currentRoute } from "../store";

    const click = () => navigateHome();
</script>

<button
    class="back-home"
    on:click={click}
    disabled={$currentRoute.path === "/"}
>
    <CaretLeftSquare />
</button>

<style>
    .back-home {
        border: none;

        display: flex;
        align-items: center;

        margin: 0;
        padding: auto 1rem;
    }

    button[disabled] :global(svg) {
        fill: var(--color-secondary-background);
    }
</style>
